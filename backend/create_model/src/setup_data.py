import os
import shutil
import random
import sys

# srcフォルダ内のconfigを正しく読み込むためにプロジェクトルートをパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.config import Config

def split_dataset(train_ratio=0.8):
    """
    data/row_data 内のカテゴリ別画像を、学習用(train)と検証用(val)に分割コピーします。
    """
    config = Config()
    raw_dir = os.path.join(config.BASE_DIR, "data", "row_data")
    train_root = config.TRAIN_DIR
    val_root = config.VAL_DIR

    if not os.path.exists(raw_dir):
        print(f"エラー: 元データディレクトリが見つかりません: {raw_dir}")
        return

    # row_data内のサブフォルダ（カテゴリ名）を取得
    categories = [d for d in os.listdir(raw_dir) if os.path.isdir(os.path.join(raw_dir, d))]
    
    for category in categories:
        src_cat_path = os.path.join(raw_dir, category)
        # 再帰的にすべての画像ファイルを取得 (.jpg, .jpeg, .png)
        all_images = []
        for root, dirs, files in os.walk(src_cat_path):
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    all_images.append(os.path.join(root, f))
        
        if not all_images:
            print(f"警告: {category} 内に画像ファイルが見つかりません。スキップします。")
            continue

        # データをシャッフルして分割点を決定
        random.shuffle(all_images)
        split_point = int(len(all_images) * train_ratio)
        
        train_files = all_images[:split_point]
        val_files = all_images[split_point:]

        # 各カテゴリの保存先フォルダを作成
        os.makedirs(os.path.join(train_root, category), exist_ok=True)
        os.makedirs(os.path.join(val_root, category), exist_ok=True)

        # ファイルのコピー
        for f_path in train_files:
            dest_path = os.path.join(train_root, category, os.path.basename(f_path))
            shutil.copy(f_path, dest_path)
        for f_path in val_files:
            dest_path = os.path.join(val_root, category, os.path.basename(f_path))
            shutil.copy(f_path, dest_path)
            
        print(f"完了: {category} (学習用: {len(train_files)}枚, 検証用: {len(val_files)}枚)")

    print("\n[成功] データの振り分けが完了しました。学習を開始できます。")

if __name__ == "__main__":
    split_dataset()