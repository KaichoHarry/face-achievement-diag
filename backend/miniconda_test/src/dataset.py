import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import train_test_split
import os

def get_dataloaders(data_dir, batch_size=32, train_ratio=0.8):
    """
    データセットを読み込み、学習用と検証用のDataLoaderを返します。
    """
    
    # 1. 前処理の定義
    # 300枚と少ないため、RandomHorizontalFlipなどでデータを水増し（Augmentation）します
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5), # 左右反転
        transforms.RandomRotation(degrees=10),  # 少し回転
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # ImageNetの統計値
    ])

    # 2. ImageFolderを使って読み込み
    # フォルダ構成：data/ノーベル受賞者/ノーベル科学賞/ノーベル1.jpg ...
    full_dataset = datasets.ImageFolder(root=data_dir, transform=transform)
    
    # クラス名（賞の種類）を保存
    class_names = full_dataset.classes
    print(f"Detected classes: {class_names}")

    # 3. 学習用と検証用に分割 (8:2)
    indices = list(range(len(full_dataset)))
    train_indices, val_indices = train_test_split(
        indices, 
        test_size=1 - train_ratio, 
        stratify=full_dataset.targets, # 各クラスの比率を維持
        random_state=42
    )

    train_dataset = Subset(full_dataset, train_indices)
    val_dataset = Subset(full_dataset, val_indices)

    # 4. DataLoaderの作成
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, class_names

if __name__ == "__main__":
    # テスト実行用
    # miniconda_test フォルダから見て data/ノーベル受賞者 にデータがある想定
    data_path = os.path.join("data", "ノーベル受賞者")
    if os.path.exists(data_path):
        train_loader, val_loader, classes = get_dataloaders(data_path)
        print(f"Train size: {len(train_loader.dataset)}")
        print(f"Val size: {len(val_loader.dataset)}")
    else:
        print(f"Directory not found: {data_path}")