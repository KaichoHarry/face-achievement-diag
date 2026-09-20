---
title: Face Achievement Diag
emoji: 📈
colorFrom: green
colorTo: green
sdk: docker
app_port: 8000
pinned: false
license: mit
short_description: 顔面偉業診断
---

# 顔面偉業診断 (Face Achievement Diagnosis)

**〜ビジネスAIシステム開発 グループワーク「顔ガチャで人生決め隊」〜**

顔画像をアップロードすると、AI（PyTorch / EfficientNetV2-S）がその人物の顔から「将来成し遂げそうな偉業」を12カテゴリの中から予測する、ジョーク・エンタメ寄りのWebアプリケーションです。

<p>
  <a href="https://face-achievement-diag.vercel.app/">🌐 デモを試す (Vercel)</a> ・
  <a href="https://huggingface.co/spaces/KaichoHarry/face-achievement-diag">🤗 バックエンドAPI (Hugging Face Spaces)</a>
</p>

<p>
  <img src="docs/images/screenshot_top.jpg" width="420" alt="トップ画面" />
  <img src="docs/images/screenshot_diagnosis.jpg" width="420" alt="診断画面" />
</p>

> ⚠️ 本アプリは研究・学習目的のデモです。予測結果は参考情報であり、人物の価値・能力・将来を断定するものではありません。

---

## 目次

- [1. プロジェクト概要](#1-プロジェクト概要)
- [2. 開発メンバー](#2-開発メンバー)
- [3. デモ・公開URL](#3-デモ公開url)
- [4. システム構成](#4-システム構成)
- [5. 予測できる12カテゴリ](#5-予測できる12カテゴリ)
- [6. 技術スタック](#6-技術スタック)
- [7. API仕様](#7-api仕様)
- [8. ディレクトリ構成](#8-ディレクトリ構成)
- [9. 開発環境のセットアップ](#9-開発環境のセットアップ)
- [10. モデルの学習](#10-モデルの学習)
- [11. 現状の制約・今後の展望](#11-現状の制約今後の展望)
- [12. 関連ドキュメント](#12-関連ドキュメント)
- [13. ライセンス](#13-ライセンス)

---

## 1. プロジェクト概要

### 目的
様々な偉業を残した偉人たちの顔画像データにラベリングを行い、その顔画像をもとに「その人物が将来どのような偉業を成し遂げるか」を予測するWebアプリケーションを作成する。

### 背景
世間には、顔から万引きを行いそうな人物を予想したり健康状態を推測するといった「現状」にフォーカスしたAIは多く見受けられる。占いのように「未来」にフォーカスしたAIがあったら面白いのではないか、というアイデアから本プロジェクトが生まれた。

### 想定シーン
飲み会やアイスブレイク、友人との交流、SNS投稿など、エンタメとして気軽に楽しむことを想定している。

---

## 2. 開発メンバー

チーム名: **顔ガチャで人生決め隊**

| 氏名 | 担当 |
| :--- | :--- |
| 南口遼河 | バックエンド開発 / インフラ（API・モデル推論・デプロイ） |
| 澁谷悠希 | フロントエンド開発（画面UI/UX） |
| 峯澤晃也 | 学習データの収集・ラベリング |
| 梅本奈成 | 学習データの収集・ラベリング |

---

## 3. デモ・公開URL

| 役割 | URL |
| :--- | :--- |
| フロントエンド（本番） | https://face-achievement-diag.vercel.app/ |
| バックエンドAPI（Hugging Face Spaces） | https://kaichoharry-backend-face-achievement.hf.space |
| GitHubリポジトリ | https://github.com/KaichoHarry/face-achievement-diag |

---

## 4. システム構成

フロントエンドとバックエンドを分離し、それぞれ独立してホスティングしている。

```text
[ User ] ─┐
          │ アクセス
          ▼
[ Frontend : HTML/CSS/JS (Vercel) ]
          │ POST /predict (画像バイナリ, multipart/form-data)
          ▼
[ Backend : FastAPI + PyTorch (Docker, Hugging Face Spaces) ]
          │ 推論
          ▼
[ 学習済みモデル (EfficientNet_V2_S, best_model.pth) ]
          │ 結果 (JSON)
          ▼
[ Frontend ] ─▶ [ User ]
```

* **フロントエンド:** 静的HTML/CSS/JSとして [Vercel](https://vercel.com/) にデプロイ
* **バックエンド:** FastAPIアプリケーションをDockerコンテナ化し、[Hugging Face Spaces](https://huggingface.co/spaces) にデプロイ
* **推論モデル:** PyTorch (torchvision `efficientnet_v2_s`) を用いた自作の画像分類モデル。学習データは合計約1000枚（1カテゴリあたり60枚以上）を独自収集・ラベリング
* **データベース:** 設計段階ではPostgreSQL（学習データ管理用、ER図は[backend/ER.md](backend/ER.md)参照）を予定していたが、現バージョンの本番環境では未接続。ローカル開発用の`docker-compose.yml`にのみ定義が残っている（[11. 現状の制約](#11-現状の制約今後の展望)参照）

処理シーケンスの詳細は以下を参照:
* [backend/sequence_user.md](backend/sequence_user.md) — ユーザーが画像をアップロードしてから結果を受け取るまでの流れ
* [backend/sequence_model.md](backend/sequence_model.md) — モデル学習時の流れ

---

## 5. 予測できる12カテゴリ

顔画像をアップロードすると、以下12カテゴリの中から最も可能性の高いものと、その確信度（%）が返される。

| | | | |
| :--- | :--- | :--- | :--- |
| ノーベル賞受賞者 | ミシュラン料理人 | オリンピックメダリスト | ギネス記録獲得者 |
| 受賞作家 | 億万長者 | 宇宙飛行士 | 教授 |
| 建国者 | 芸能人 | 政治家 | 凶悪犯 |

---

## 6. 技術スタック

### フロントエンド
* HTML / CSS / JavaScript（フレームワークなし・素の実装）
* デプロイ: Vercel

### バックエンド
* Python 3.10 / [FastAPI](https://fastapi.tiangolo.com/) / Uvicorn
* [PyTorch](https://pytorch.org/) + torchvision（EfficientNet_V2_S をファインチューニング）
* Pillow（画像前処理）
* デプロイ: Docker（Hugging Face Spaces, `sdk: docker`）

### インフラ・ツール
* コンテナ化: Docker / Docker Compose
* バージョン管理: Git / GitHub
* モデル配布: Git LFS（`*.pth`）

---

## 7. API仕様

### `POST /predict`

顔画像を送信し、予測結果を取得する。

**Request**

```
Content-Type: multipart/form-data
```

```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);

fetch("https://kaichoharry-backend-face-achievement.hf.space/predict", {
  method: "POST",
  body: formData,
});
```

**Response**

```json
{
  "prediction": "ノーベル賞受賞者",
  "probability": 0.873,
  "category_id": 1
}
```

| フィールド | 型 | 説明 |
| :--- | :--- | :--- |
| `prediction` | string | 予測された偉業カテゴリ（日本語） |
| `probability` | float | 予測の確信度（0〜1） |
| `category_id` | int | カテゴリID（1〜12） |

実装は [backend/app/main.py](backend/app/main.py) / [backend/app/model_utils.py](backend/app/model_utils.py) / [backend/app/schemas.py](backend/app/schemas.py) を参照。Hugging Face Spaces上で稼働中は `/docs` にSwagger UIが自動生成される。

---

## 8. ディレクトリ構成

```text
face-achievement-diag/
├── backend/
│   ├── app/                    # FastAPIアプリケーション本体
│   │   ├── main.py             # エンドポイント定義（/predict）
│   │   ├── model_utils.py      # モデルのロード・前処理・推論
│   │   └── schemas.py          # レスポンスのPydanticスキーマ
│   ├── create_model/           # モデル学習用コード
│   │   ├── src/
│   │   │   ├── config.py       # 学習ハイパーパラメータ
│   │   │   ├── dataset.py      # DataLoader定義
│   │   │   ├── model.py        # EfficientNet_V2_Sベースのモデル定義
│   │   │   └── setup_data.py   # 収集データをtrain/valに分割
│   │   ├── models/best_model.pth  # 学習済みモデル重み（Git LFS）
│   │   └── train.py            # 学習スクリプト
│   ├── requirements.txt        # バックエンド実行用の依存パッケージ
│   ├── ER.md                   # 学習データ管理用ER図（設計時点）
│   ├── sequence_user.md / .png # 推論時のシーケンス図
│   └── sequence_model.md / .png# 学習時のシーケンス図
├── frontend/
│   ├── index.html / diagnosis.html / result.html
│   ├── css/style.css
│   └── js/index.js / diagnosis.js / result.js
├── docker-compose.yml           # ローカル開発用（backend + PostgreSQL）
├── Dockerfile                   # Hugging Face Spaces用ビルド設定
└── README.md
```

---

## 9. 開発環境のセットアップ

本プロジェクトでは、誰のPCでも同じ環境で動くように **Docker** を使用する。

### 前提
* Docker / Docker Compose がインストールされていること

### 手順

```bash
# 1. リポジトリをクローン
git clone https://github.com/KaichoHarry/face-achievement-diag.git
cd face-achievement-diag

# 2. コンテナをビルド・起動
docker compose up --build
```

起動後、以下にアクセスするとフロントエンドとAPIをローカルで確認できる。

* API本体: http://localhost:8000
* APIドキュメント (Swagger UI): http://localhost:8000/docs
* フロントエンド（静的ファイル配信）: http://localhost:8000/frontend/index.html

※ `docker-compose.yml` にはPostgreSQLコンテナ（`db`）も定義されているが、現状の`backend`アプリケーションからは接続していない（[11. 現状の制約](#11-現状の制約今後の展望)参照）。

---

## 10. モデルの学習

学習用コードは [backend/create_model](backend/create_model) にまとまっている。

```bash
cd backend/create_model
pip install -r requirements.txt

# 1. 収集した生データ(data/row_data/カテゴリ名/*.jpg)を train/val に分割
python -m src.setup_data

# 2. 学習を実行し、最良モデルを models/best_model.pth に保存
python train.py
```

* ベースモデル: `torchvision.models.efficientnet_v2_s`（全層ファインチューニング）
* 1カテゴリあたり60枚以上、合計約1000枚の画像を独自に収集・ラベリング
* 画像枚数が少ないため、`RandomHorizontalFlip` / `RandomRotation` / `ColorJitter` による強めのData Augmentationを適用（[backend/create_model/src/dataset.py](backend/create_model/src/dataset.py)）
* 学習は大学の計算機サーバー（Linux環境）上で実施

---

## 11. 現状の制約・今後の展望

企画段階の仕様（[backend/ER.md](backend/ER.md) の大分類・小分類の二段階予測、PostgreSQLでの学習データ管理、大学サーバーでの本番稼働など）と、実際にリリースした内容には以下の差分がある。

* **小分類（サブカテゴリ）予測は未実装** — 現行モデルは大分類12カテゴリのみを予測する
* **PostgreSQLは本番未接続** — `docker-compose.yml`にはDB定義があるが、`backend/app`のコードからは利用していない
* **デプロイ先の変更** — 企画時は「フロントエンド: GitHub Pages」「バックエンド: 大学サーバー」を想定していたが、最終的に「フロントエンド: Vercel」「バックエンド: Hugging Face Spaces」に変更した

### 今後の展望
* 学習データの増加による分類精度の向上
* 小分類（サブカテゴリ）予測の実装
* 結果表示画面の演出強化
* SNS共有機能の追加

---

## 12. 関連ドキュメント

企画段階で作成した仕様書・計画書・設計資料をMarkdown化して`docs/`配下にまとめている。

| ドキュメント | 内容 |
| :--- | :--- |
| [docs/spec.md](docs/spec.md) | 仕様書（目的・背景・機能要件・非機能要件・API設計） |
| [docs/design.md](docs/design.md) | 設計書（システム構成図・ER図・画面構成案、企画時点） |
| [docs/plan.md](docs/plan.md) | 計画書（チーム体制・開発スケジュール） |
| [backend/ER.md](backend/ER.md) | 学習データ管理用ER図（実装コードと同期） |
| [backend/sequence_user.md](backend/sequence_user.md) | 推論時のシーケンス図 |
| [backend/sequence_model.md](backend/sequence_model.md) | モデル学習時のシーケンス図 |

> `docs/`配下の仕様書・計画書・設計書は企画時点（2026年4月〜6月）の内容であり、実装との差分は [11. 現状の制約・今後の展望](#11-現状の制約今後の展望) にまとめている。

---

## 13. ライセンス

MIT License
