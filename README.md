# 513bot

<img src="README.drawio.svg" width="100%" height="auto">

## コンテナ

| 名前 | 機能 | 必須 |
| :---: | :---: | :---: |
| [core-receiver](/core) | ボットにメンションされたメッセージを受信 | ◯ |
| [core-sender](/core) | チャンネルにメッセージを送信 | ◯ |
| [app-arxivreporter](/app-arxivreporter) | arXiv論文をGPT-3で毎朝要約 | × |
| [app-forecaster](/app-forecaster) | その日の天気予報を毎朝通知 | × |
| [app-info](/app-info) | メンションされたチャンネルのIDを通知（デバッグ用） | × |
| [app-shuffle](/app-shuffle) | 指定されたグループのメンバーをシャッフルして通知 | × |
