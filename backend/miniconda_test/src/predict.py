import torch
from torchvision import transforms
from PIL import Image
import os
import sys

# 自身の作成したmodel.pyから構造をインポート
from model import create_model

def predict(image_path):
    # 1. デバイス設定 (Mac/Linux/GPU対応)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 2. モデルのロード
    model_path = os.path.join("models", "nobel_classifier.pth")
    if not os.path.exists(model_path):
        print(f"Error: {model_path} が見つかりません。先に学習を行ってください。")
        return None

    # 保存時のデータをロード (map_locationでCPU/GPU間の差異を吸収)
    checkpoint = torch.load(model_path, map_location=device)
    class_names = checkpoint['class_names']
    
    # モデル構造を定義して重みを流し込む
    model = create_model(num_classes=len(class_names))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval() # 推論モードに切り替え

    # 3. 画像の前処理 (学習時と同じ設定)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    try:
        image = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error: 画像を開けませんでした。 {e}")
        return None

    input_tensor = transform(image).unsqueeze(0).to(device) # (1, 3, 224, 224) に変換

    # 4. 予測実行
    with torch.no_grad():
        outputs = model(input_tensor)
        # ソフトマックス関数で確率(0.0~1.0)に変換
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        # 最も高い確率のインデックスを取得
        confidence, predicted_idx = torch.max(probabilities, 0)

    result = {
        "award": class_names[predicted_idx.item()],
        "confidence": confidence.item() * 100, # %表示用
        "all_probs": {class_names[i]: prob.item() * 100 for i, prob in enumerate(probabilities)}
    }
    return result

if __name__ == "__main__":
    # 実行方法: python src/predict.py test.jpg
    if len(sys.argv) > 1:
        target_image = sys.argv[1]
        res = predict(target_image)
        if res:
            print(f"\n--- 判定結果 ---")
            print(f"受賞しそうな賞: {res['award']}")
            print(f"確信度: {res['confidence']:.2f}%")
            print("\n--- 各賞の確率詳細 ---")
            for name, prob in res['all_probs'].items():
                print(f"{name}: {prob:.2f}%")
    else:
        print("使い方: python src/predict.py [画像パス]")