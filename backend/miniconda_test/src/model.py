import torch
import torch.nn as nn
from torchvision import models

def create_model(num_classes):
    """
    学習済みResNet18をベースに、出力層を今回のクラス数に適合させたモデルを返します。
    """
    # 1. すでに大量の画像(ImageNet)で学習済みの重みをロード
    # 2026年現在のtorchvisionでは weights=モデル名_Weights.DEFAULT が推奨されます
    weights = models.ResNet18_Weights.DEFAULT
    model = models.resnet18(weights=weights)
    
    # 2. 全ての層のパラメータを一旦フリーズ（固定）
    # 特徴抽出部分（顔のパーツを見分ける力）は既存の知識をそのまま使います
    for param in model.parameters():
        param.requires_grad = False
        
    # 3. 最終層（全結合層）を差し替える
    # ResNet18の最終層への入力次元数は model.fc.in_features で取得可能
    num_ftrs = model.fc.in_features
    
    # 今回の賞の数（6クラス）に合わせて新しい層を追加
    # ここだけ requires_grad = True （学習対象）になります
    model.fc = nn.Linear(num_ftrs, num_classes)
    
    return model

if __name__ == "__main__":
    # テスト用：6クラス（ノーベル賞の数）でモデルを作成
    num_classes = 6
    model = create_model(num_classes)
    
    # モデルの構造を確認（最後だけ 512 -> 6 になっているはず）
    print(model.fc)
    
    # ダミーデータ（バッチサイズ1、3チャンネル、224x224）を流してチェック
    dummy_input = torch.randn(1, 3, 224, 224)
    output = model(dummy_input)
    print(f"Output shape: {output.shape}") # torch.Size([1, 6]) になればOK