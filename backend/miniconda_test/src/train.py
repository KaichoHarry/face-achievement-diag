import torch
import torch.nn as nn
import torch.optim as optim
from dataset import get_dataloaders
from model import create_model
import os

def train():
    # 1. 設定
    data_dir = os.path.join("data", "ノーベル受賞者")
    model_save_path = os.path.join("models", "nobel_classifier.pth")
    num_epochs = 10
    batch_size = 16
    learning_rate = 0.001

    # フォルダ作成
    os.makedirs("models", exist_ok=True)

    # 2. デバイス設定 (GPU or CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 3. データとモデルの準備
    train_loader, val_loader, class_names = get_dataloaders(data_dir, batch_size=batch_size)
    model = create_model(num_classes=len(class_names)).to(device)

    # 4. 損失関数と最適化手法
    criterion = nn.CrossEntropyLoss()
    # 転移学習なので、最後の層(fc)だけを更新するように設定
    optimizer = optim.Adam(model.fc.parameters(), lr=learning_rate)

    # 5. 学習ループ
    print("Starting training...")
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        # 検証 (Validation)
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}, Val Acc: {100 * correct / total:.2f}%")

    # 6. モデルの保存
    # state_dict（重みデータ）とクラス名を一緒に保存しておくと後で便利です
    torch.save({
        'model_state_dict': model.state_dict(),
        'class_names': class_names
    }, model_save_path)
    print(f"Model saved to {model_save_path}")

if __name__ == "__main__":
    train()