# 顔面偉業診断 (Face Achievement Diagnosis)
## [cite_start]〜ビジネス AI システム開発プロジェクト〜 [cite: 4]

[cite_start]様々な偉業を残した偉人たちの顔画像データを用いて、その人物が将来どのような偉業を成し遂げるかをAIが予測・診断するWebアプリケーションです。[cite: 7]

---

## 1. プロジェクト概要
### 目的
[cite_start]既存のAIは「現状（万引き検知や健康状態）」にフォーカスしたものが多いですが、本プロジェクトでは占いや予言のように「未来」にフォーカスしたAIの面白さを提案します。[cite: 9]

### 開発メンバー
* [cite_start]**バックエンド / インフラ担当:** 南口 遼河（学籍番号: NK240006）[cite: 5, 6, 21]
* [cite_start]**フロントエンド担当:** 澁谷 [cite: 18, 26]

---

## 2. システム構成
[cite_start]システムは、手軽に利用できるフロントエンドと、強力な計算資源を持つバックエンドを分離した構成になっています。[cite: 13]

* [cite_start]**フロントエンド:** GitHub Pages にデプロイ [cite: 14, 37]
* [cite_start]**バックエンド:** 大学のLinuxサーバーにて稼働 [cite: 17, 38]
* [cite_start]**データベース:** 大学サーバー内の PostgreSQL [cite: 34, 39]

---

## 3. 技術スタック
### [cite_start]フロントエンド [cite: 24]
* [cite_start]**言語:** HTML / CSS / JavaScript [cite: 25]
* [cite_start]**フレームワーク/ライブラリ:** 澁谷の任意で選択可能 [cite: 26, 27]

### [cite_start]バックエンド [cite: 28]
* [cite_start]**言語:** Python + PyTorch (AIモデル) [cite: 29]
* [cite_start]**フレームワーク:** FastAPI [cite: 30]
* [cite_start]**データベース:** PostgreSQL [cite: 34]

### インフラ・ツール
* [cite_start]**コンテナ化:** Docker 
* [cite_start]**バージョン管理:** Git / GitHub [cite: 100]

---

## 4. 主な機能と予測カテゴリ
### [cite_start]ユーザー機能 [cite: 41]
1. [cite_start]**画像のアップロード:** 顔写真を送信します。[cite: 42]
2. [cite_start]**予測結果の表示:** 以下のカテゴリからAIが可能性を算出します。[cite: 43]

| 分類例 | | | |
| :--- | :--- | :--- | :--- |
| [cite_start]ノーベル賞受賞者 [cite: 45] | [cite_start]ミシュラン料理人 [cite: 45] | [cite_start]オリンピックメダリスト [cite: 45] | [cite_start]ギネス記録獲得者 [cite: 45] |
| [cite_start]受賞作家 [cite: 45] | [cite_start]億万長者 [cite: 45] | [cite_start]宇宙飛行士 [cite: 45] | [cite_start]教授 [cite: 45] |
| [cite_start]建国者 [cite: 45] | [cite_start]芸能人 [cite: 45] | [cite_start]政治家 [cite: 45] | [cite_start]凶悪犯 [cite: 45] |

---

## 5. 開発環境のセットアップ (澁谷くんへ)
[cite_start]本プロジェクトでは、誰のPCでも同じ環境が動くように **Docker** を使用します。

### 手順
1. **リポジトリをクローン:**
   ```bash
   git clone [GitHubのURL]