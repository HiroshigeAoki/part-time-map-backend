# part-time-map-backend

タウンワークなどのバイト情報をGoogle Map上にプロットして探しやすくするWebサイトです。

URL: https://part-time-map-355016.web.app/ (今の所、利用可能範囲は静岡大学周辺・富塚エリアのみです（拡大予定）)

# コード
* [frontend](https://github.com/HiroshigeAoki/part-time-map-frontend)
* [backend](https://github.com/HiroshigeAoki/part-time-map-backend)
* [crawler](https://github.com/HiroshigeAoki/part-time-map-crawler)

# 画面（改善予定）
## 検索画面
<img width="1260" alt="Screen Shot 2022-07-19 at 16 32 23" src="https://user-images.githubusercontent.com/58395317/179693631-c91c3b70-3e06-4e59-943d-db9e2b400bf8.png">

## 検索結果
<img width="1260" alt="Screen Shot 2022-07-19 at 16 33 14" src="https://user-images.githubusercontent.com/58395317/179693983-d0e135e3-8404-4b91-ae1f-03bb09982592.png">


## 検索結果（詳細情報表示）
<img width="1260" alt="Screen Shot 2022-07-19 at 16 33 57" src="https://user-images.githubusercontent.com/58395317/179693701-3ece1d83-dba2-4aae-805d-3ee301f90e9d.png">

# 使用技術
* frontend: node.js → vue.jsに移行予定
* backend: FastAPI
* crawler: scrapy

# 公開方法
* frontend: firebase hosting
* backend: Cloud Run
* DB: MongoDB Atlas Database

# 処理の流れ
## バイト情報取得・管理機能(crawler)
![バイト情報管理機能 (4)](https://user-images.githubusercontent.com/58395317/179741790-c276f76d-e28e-4e1d-9a5e-c3b4797faf19.jpg)

## 条件検索機能(backend, frontend)
![条件検索機能 (3)](https://user-images.githubusercontent.com/58395317/179779783-a4b80ade-6386-4572-b2c8-eca9822ad252.jpg)
