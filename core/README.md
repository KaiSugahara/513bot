# 513bot/core-*

## How to Start

### Create New Slack App

1. Slack API (https://api.slack.com/apps) を開く
1. 「Create New App」をクリック
    1. 「From scratch」を選択
    1. 「App Name」に任意の名前を入力（メンションするときのボット名になります）
    1. 「Pick a workspace to develop your app in」でボットを追加するワークスペースを選択
    1. 「Create App」をクリック
1. サイドバーの「Basic Information」をクリック
    1. 「App-Level Tokens」の「Generate Token and Scopes」をクリック
    1. 「Token Name」に任意の名前を入力
    1. 「Add Scope」で「connections:write」のみ選択
    1. 「Generate」をクリック
    1. 発行されたToken（App-Level Token）をコピー
1. サイドバーの「Socket Mode」をクリック
    1. 「Enable Socket Mode」を有効化
    1. 「Event Subscriptions」をクリック
    1. 「Enable Events」をOnに変更
    1. 「Subscribe to bot events」タブで「Add Bot User Event」をクリック
    1. 「app_mention」のみ選択
    1. 「Save Changes」をクリック
1. サイドバーの「OAuth & Permissions」をクリック
    1. 「Bot Token Scopes」の「Add an OAuth Scope」をクリック
    1. 「chat:write」のみ選択
1. サイドバーの「OAuth & Permissions」をクリック
    1. 「Install to Workspace」をクリック
    1. 発行されたBot User OAuth Tokenをコピー
  
### Make .env

1. `.env.example` から `.env` を作成．
```bash
$ cp .env.example .env
```

2. コピーした「Bot User OAuth Token」をSLACK_BOT_TOKENに，「App-Level Token」をSLACK_APP_TOKENに入力
```bash
$ code .env
```

```python:.env
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxx-xxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-x-xxxxxxxxxxx-xxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Start the Container

```bash
$ docker-compose up -d
```
