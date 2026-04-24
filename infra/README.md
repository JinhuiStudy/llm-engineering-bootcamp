# infra/ — 로컬 개발 인프라 (Docker Compose)

14일 부트캠프에서 쓰는 self-host 인프라. **Day 6 이후 Qdrant, Day 12 이후 Langfuse**.

## 📅 언제 뭐 켜나

| 서비스 | 언제부터 | 명령 | 리소스 |
|---|---|---|---|
| Qdrant | Day 6 | `make qdrant-up` | RAM ~500MB, 디스크 수백MB |
| Langfuse | Day 12 | `make langfuse-up` | RAM 2-3GB, 컨테이너 5개 |
| Phoenix (선택) | Day 12 | `make phoenix-up` | RAM ~500MB |
| 둘 다 | Day 12-14 | `make infra-up` | RAM 3-4GB |

> 💡 **Mac M2 16GB 기준**: Langfuse + app 동시 구동 시 타 앱 닫는 게 안전. 발열/배터리 감소 체감.

## 🔌 포트 맵

| Port | 서비스 | 용도 |
|---|---|---|
| 6333 | Qdrant | REST API + Dashboard |
| 6334 | Qdrant | gRPC |
| 3000 | Langfuse | Web UI |
| 9090 | Langfuse MinIO | S3 API |
| 9091 | Langfuse MinIO | Console UI |
| 8123 | Clickhouse | HTTP (internal, 노출 X) |
| 5432 | Postgres | DB (internal, 노출 X) |
| 6006 | Phoenix | Web UI (선택) |
| 4317 | Phoenix | OTLP gRPC (선택) |
| 11434 | Ollama | OpenAI-compat (네이티브 설치) |

**포트 충돌 체크**:
```bash
lsof -i :6333  # 이미 쓰이면 docker-compose.yml 에서 6334:6333 등으로 변경
lsof -i :3000
```

## 💾 데이터 영속성

- `infra/qdrant/storage/` — Qdrant 컬렉션 (기본 `.gitignore`)
- `infra/langfuse/volumes/{postgres,clickhouse,minio}/` — Langfuse 전체 데이터

## 🔄 인프라 명령 치트시트

```bash
# 시작 / 중지
make qdrant-up          make qdrant-down
make langfuse-up        make langfuse-down
make infra-up           make infra-down

# 상태
make status             # 실행 중인지 + .env / Python / Docker / Ollama

# 완전 초기화 (데이터 삭제 주의)
make clean-docker       # 5초 유예 후 volumes 삭제

# 개별 초기화
rm -rf infra/qdrant/storage
rm -rf infra/langfuse/volumes
```

## 🐛 자주 발생하는 이슈

| 증상 | 원인 | 해결 |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop 미실행 | 앱 시작 후 재시도 |
| `port is already allocated` | 포트 충돌 | `lsof -i :PORT` → kill 또는 compose 포트 변경 |
| Langfuse 컨테이너 계속 재시작 | RAM 부족 | Docker Desktop 설정에서 RAM 할당 ↑ |
| `relation does not exist` (langfuse) | postgres 초기화 실패 | `rm -rf volumes/postgres && up -d` |
| Apple Silicon 경고 | 이미지 arch 미스매치 | compose에 `platform: linux/arm64` 또는 latest 이미지 |
| Clickhouse 디스크 폭발 | TTL 없음 | Langfuse env에 `CLICKHOUSE_TRACES_DAYS=30` 추가 |

## 🔒 보안 주의 (production 사용 시)

이 compose 파일들은 **로컬 개발 전용**. Production에는:

- Langfuse `SALT`, `ENCRYPTION_KEY`, `NEXTAUTH_SECRET` 반드시 교체
  ```bash
  # SALT 32자
  openssl rand -hex 16
  # ENCRYPTION_KEY 64자 (hex 32bytes)
  openssl rand -hex 32
  ```
- MinIO `MINIO_ROOT_PASSWORD` / Postgres `POSTGRES_PASSWORD` 강한 비밀번호
- 모든 포트를 외부에 노출하지 말고 reverse proxy + TLS
- `TELEMETRY_ENABLED: false` 유지 (Langfuse 익명 사용 통계)

## 📂 세부 문서

- [`qdrant/README.md`](qdrant/README.md) — Qdrant 전용
- [`langfuse/README.md`](langfuse/README.md) — Langfuse 전용 (세부 설정 + 트러블슈팅)

## 🌐 Cloud 대안 (Self-host 불가 시)

| Service | Cloud 옵션 | 무료 tier |
|---|---|---|
| Qdrant | [Qdrant Cloud](https://cloud.qdrant.io/) | 1GB storage |
| Langfuse | [Cloud](https://cloud.langfuse.com) | 50k observations/mo |
| Phoenix | [Arize AX](https://arize.com) | 10M events/mo 무료 tier |

`.env`에서 `QDRANT_URL` / `LANGFUSE_HOST` 만 바꾸면 대부분 코드 그대로 동작.
