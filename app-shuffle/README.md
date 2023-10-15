# 513bot/app-shuffle

## How to Start
  
### Make members.yaml

1. `members.yaml.example` から `members.yaml` を作成
```bash
$ cp .env.example .env
```

2. グループ名とグループ構成メンバーをyaml形式で入力
```bash
$ code members.yaml
```

```members.yaml
all:
    - Mr. A
    - Mr. B
    - Mr. C
    - Mr. D
team0:
    - Mr. A
    - Mr. B
team1:
    - Mr. C
    - Mr. D
```

### Start the Container

```bash
$ docker-compose up -d
```
