import torch
import torch.nn as nn
import torch.optim as optim
from src.config import Config
from src.dataset import get_dataloaders
from src.model import create_achievement_model
from tqdm import tqdm
import os

def main():
    config = Config()
    train_loader, val_loader, num_classes = get_dataloaders(config)
    
    model = create_achievement_model(num_classes).to(config.DEVICE)
    criterion = nn.CrossEntropyLoss()
    # 全層チューニングを行うためAdamを使用。学習率は低めに。
    optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    
    best_acc = 0.0
    os.makedirs(config.MODEL_SAVE_DIR, exist_ok=True)

    for epoch in range(config.NUM_EPOCHS):
        model.train()
        train_loss = 0
        for images, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}"):
            images, labels = images.to(config.DEVICE), labels.to(config.DEVICE)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        # Validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(config.DEVICE), labels.to(config.DEVICE)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        acc = 100 * correct / total
        print(f"Accuracy: {acc:.2f}% (Best: {best_acc:.2f}%)")
        
        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), os.path.join(config.MODEL_SAVE_DIR, "best_model.pth"))

if __name__ == "__main__":
    main()