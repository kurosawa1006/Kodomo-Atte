# Kodomo-Atte（コドモアッテ）

こども園向けの出欠・連絡サポートアプリです。

## 起動

```bash
docker compose up -d
```

アプリは以下で起動します。

- Django API: `http://localhost:8000`
- Next.js フロント: `http://localhost:3000`

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
| Next.js フロント | http://localhost:3000/ |
| 保護者ダッシュボード（Next.js） | http://localhost:3000/parent/dashboard?parent=1 |

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

## Web API（Next.js 連携用）

Django REST Framework ベースの API です。CORS で `http://localhost:3000` を許可しています。

ベースURL: `http://localhost:8000/api/v1/`

| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| GET | `/api/v1/me/?role=parent&id=1` | プロファイル・権限（保護者） |
| GET | `/api/v1/me/?role=staff&id=1` | プロファイル・権限（スタッフ） |
| GET | `/api/v1/children/` | 園児一覧（`?class=` で絞り込み可） |
| GET | `/api/v1/children/{id}/` | 園児詳細 |
| GET | `/api/v1/staff/` | スタッフ一覧 |
| GET | `/api/v1/parents/` | 保護者一覧 |
| GET | `/api/v1/attendances/` | 本日の出欠一覧（`?date=` `?class=` `?is_confirmed=`） |
| POST | `/api/v1/attendances/` | 出欠登録（同一 child+date は upsert） |
| PATCH | `/api/v1/attendances/{id}/` | 出欠更新 |
| POST | `/api/v1/attendances/{id}/confirm/` | スタッフ確認済 |

### 出欠登録の例（POST）

```json
{
  "child": 4,
  "date": "2026-08-14",
  "attendance_status": 3,
  "reason": "発熱"
}
```

`attendance_status`: `1`=遅刻 / `2`=早退 / `3`=欠席

### 依存パッケージの反映

```bash
docker compose build web
docker compose up -d
```

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
