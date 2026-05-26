import os

def setup_directories():
    base_path = "data"
    categories = [
        "01_nobel_winner", "02_michelin_chef", "03_olympic_medalist", "04_guinness_holder",
        "05_awarded_author", "06_billionaire", "07_astronaut", "08_professor",
        "09_founder", "10_celebrity", "11_politician", "12_criminal"
    ]
    
    subsets = ["train", "val"]
    
    for subset in subsets:
        for category in categories:
            path = os.path.join(base_path, subset, category)
            os.makedirs(path, exist_ok=True)
            print(f"Created: {path}")

    print("\n[Done] フォルダ作成が完了しました。")
    print("各カテゴリの画像を train (80%) と val (20%) に分けて配置してください。")

if __name__ == "__main__":
    setup_directories()