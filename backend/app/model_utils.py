import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import io
import gc
import sys
import os

# create_model/src/model.py をインポートできるようにパスを追加
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

try:
    from create_model.src.model import create_achievement_model
except ImportError:
    # 異なる実行環境（ローカル実行等）へのフォールバック
    from create_model.src.model import create_achievement_model

# カテゴリ一覧（フォルダ名の順番と一致させる必要があります）
CATEGORIES = [
    "01_nobel_winner", "02_michelin_chef", "03_olympic_medalist", "04_guinness_holder",
    "05_awarded_author", "06_billionaire", "07_astronaut", "08_professor",
    "09_founder", "10_celebrity", "11_politician", "12_criminal"
]

# 日本語表示用のマッピング
CATEGORY_NAMES_JP = {
    "01_nobel_winner": "ノーベル賞受賞者",
    "02_michelin_chef": "ミシュラン料理人",
    "03_olympic_medalist": "オリンピックメダリスト",
    "04_guinness_holder": "ギネス記録獲得者",
    "05_awarded_author": "受賞作家",
    "06_billionaire": "億万長者",
    "07_astronaut": "宇宙飛行士",
    "08_professor": "教授",
    "09_founder": "建国者",
    "10_celebrity": "芸能人",
    "11_politician": "政治家",
    "12_criminal": "凶悪犯"
}

class Predictor:
    def __init__(self, model_path: str):
        # メモリ節約のためスレッド数を制限
        torch.set_num_threads(1)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # 推論時はImageNetの重みをロードせず、自作の重みのみをロードする
        model = create_achievement_model(num_classes=len(CATEGORIES), pretrained=False)
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        
        # 動的量子化を適用 (メモリ削減と高速化)
        self.model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.qint8
        )
        
        self.model.to(self.device)
        self.model.eval()
        
        # メモリの強制解放
        gc.collect()

        # 学習時と同じ正規化パラメータを使用
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    @torch.inference_mode()
    def predict(self, image_bytes: bytes):
        # 画像の読み込みと前処理
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(tensor)
            # ソフトマックスで確率を算出
            probabilities = F.softmax(outputs, dim=1)
            confidence, index = torch.max(probabilities, 1)

        cat_tag = CATEGORIES[index.item()]
        prediction_jp = CATEGORY_NAMES_JP.get(cat_tag, cat_tag)

        # フロントエンドが使いやすいように数値や綺麗な名前も返せるようにします
        return {
            "prediction": prediction_jp,
            "probability": float(confidence.item()),
            "category_id": index.item() + 1
        }

# インスタンス化 (パスは実際の場所に合わせて調整)
model_weight_path = os.path.join(os.path.dirname(__file__), "../create_model/models/best_model.pth")
predictor = Predictor(model_weight_path)