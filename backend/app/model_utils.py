import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import io
import sys
import os

# create_model/src/model.py をインポートできるようにパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from create_model.src.model import create_achievement_model

# カテゴリ一覧（フォルダ名の順番と一致させる必要があります）
CATEGORIES = [
    "01_nobel_winner", "02_michelin_chef", "03_olympic_medalist", "04_guinness_holder",
    "05_awarded_author", "06_billionaire", "07_astronaut", "08_professor",
    "09_founder", "10_celebrity", "11_politician", "12_criminal"
]

class Predictor:
    def __init__(self, model_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = create_achievement_model(num_classes=len(CATEGORIES))
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        # 学習時と同じ正規化パラメータを使用
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, image_bytes: bytes):
        # 画像の読み込みと前処理
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(tensor)
            # ソフトマックスで確率を算出
            probabilities = F.softmax(outputs, dim=1)
            confidence, index = torch.max(probabilities, 1)

        cat_name = CATEGORIES[index.item()]
        # フロントエンドが使いやすいように数値や綺麗な名前も返せるようにします
        return {
            "prediction": cat_name,
            "probability": float(confidence.item()),
            "category_id": index.item() + 1
        }

# インスタンス化 (パスは実際の場所に合わせて調整)
model_weight_path = os.path.join(os.path.dirname(__file__), "../create_model/models/best_model.pth")
predictor = Predictor(model_weight_path)