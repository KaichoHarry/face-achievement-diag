import torch
import os

class Config:
    # srcフォルダから一つ上のルートディレクトリを取得
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TRAIN_DIR = os.path.join(BASE_DIR, "data/train")
    VAL_DIR = os.path.join(BASE_DIR, "data/val")
    MODEL_SAVE_DIR = os.path.join(BASE_DIR, "models")
    
    # ハイパーパラメータ (枚数が少ないためData Augmentationと低学習率が鍵)
    IMAGE_SIZE = 224
    BATCH_SIZE = 32
    NUM_EPOCHS = 100
    LEARNING_RATE = 5e-5
    
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    NUM_WORKERS = 4