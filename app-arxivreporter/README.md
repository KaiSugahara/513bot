# 513bot/app-arxivreporter

## How to Start
  
### Make .env

1. `.env.example` から `.env` を作成
```bash
$ cp .env.example .env
```

2. 通知したいチャンネル名（#を含む）をCHANNEL，OpenAIのAPI KeyをOPENAI_API_KEYに入力
```bash
$ code .env
```

```python:.env
CHANNEL=#random
OPENAI_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Start the Container

```bash
$ docker-compose up -d
```
