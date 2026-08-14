# Kodomo-Atte（コドモアッテ）

こども園向けの出欠・連絡サポートアプリです。

## 起動

```bash
docker compose up -d
```

アプリは `http://localhost:8000` で起動します。

## アクセスURL

| 画面 | URL |
|------|-----|
| TOP | http://localhost:8000/ |
| 園児一覧（全体） | http://localhost:8000/children/ |
| 園児一覧（クラス絞り込み） | http://localhost:8000/children/?class=1 |
| スタッフダッシュボード（SP） | http://localhost:8000/staff/dashboard/ |
| 保護者ダッシュボード（SP） | http://localhost:8000/parent/dashboard/ |
| 保護者ダッシュボード（特定保護者） | http://localhost:8000/parent/dashboard/?parent=1 |
| 管理画面 | http://localhost:8000/admin/ |

### クラス絞り込みの例

| `class` | クラス |
|---------|--------|
| 1 | ひよこ（0歳） |
| 2 | ひばり（1歳） |
| 3 | つばめ（2歳） |
| 4 | はと（3歳） |
| 5 | かもめ（4歳） |
| 6 | くじゃく（5歳） |

例: http://localhost:8000/staff/dashboard/?class=2

## 兄弟児（初期データ）

5家庭に兄弟児が設定されています。園児一覧で名前をタップすると詳細モーダルに兄弟児が表示され、名前リンクから兄弟の詳細へ切り替えできます。

| 世帯 | 保護者 pk | 園児 | クラス |
|------|-----------|------|--------|
| 田中家 | 5（父）・6（母） | 田中 陽菜（pk4） / 田中 結翔（pk11） | ひよこ / くじゃく |
| 山田家 | 15（父）・16（母） | 山田 凛（pk12） / 山田 結菜（pk20） | ひばり / はと |
| 伊藤家 | 50（父）・51（母） | 伊藤 翔（pk35） / 伊藤 楓（pk36） | ひばり / つばめ |
| 阿部家 | 72（父）・73（母） | 阿部 海斗（pk55） / 阿部 なな（pk56） | かもめ / はと |
| 松本家 | 96（父）・97（母） | 松本 颯真（pk75） / 松本 真由（pk76） | くじゃく / かもめ |

## 初期データ投入

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py loaddata initial_data
```
