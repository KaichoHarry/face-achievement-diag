miniconda_test/
├── data/                 # 学習用データ（300枚の画像）
│   ├── raw/              # 届いたままのデータ
│   │   ├── physics/      # 物理学賞
│   │   ├── peace/        # 平和賞
│   │   └── ...           # 各フォルダに画像が格納されている
│   └── processed/        # 前処理済み（リサイズ後など）のデータ
├── models/               # 学習済みモデル（.pthファイル）の保存先
├── src/                  # メインのソースコード
│   ├── dataset.py        # PyTorchのDataset/DataLoader定義
│   ├── model.py          # CNN（学習モデル）のネットワーク構造定義
│   ├── train.py          # 学習実行用スクリプト
│   └── predict.py        # 学習済みモデルを使った推論用ロジック
├── notebooks/            # 実験用（Jupyter Notebookなどを使う場合）
└── main.py               # FastAPIの起動エントリーポイント（app/直下と連携）