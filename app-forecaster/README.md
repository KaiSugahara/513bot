# 513bot/app-forecaster

## How to Start
  
### Make .env

1. `.env.example` から `.env` を作成
```bash
$ cp .env.example .env
```

2. 通知したいチャンネル名（#を含む）をCHANNEL，地域ID（6桁）をCITYに入力
※地域IDは[地域定義表](https://weather.tsukumijima.net/primary_area.xml)を参照
```bash
$ code .env
```

```python:.env
CHANNEL=#random
CITY=130010
```

### Start the Container

```bash
$ docker-compose up -d
```
