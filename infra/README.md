# infra/

로컬 개발 인프라 Docker compose.

## 언제 뭐 켜나

| 서비스 | 언제부터 | 명령 |
|---|---|---|
| Qdrant | Day 6 | `make qdrant-up` |
| Langfuse | Day 12 | `make langfuse-up` |
| 둘 다 | Day 12+ | `make infra-up` |

## 포트 충돌 확인

| Port | 서비스 |
|---|---|
| 6333 | Qdrant REST / Dashboard |
| 6334 | Qdrant gRPC |
| 3000 | Langfuse Web |
| 9090 | Langfuse MinIO S3 |
| 9091 | Langfuse MinIO Console |
| 11434 | Ollama (네이티브 설치) |

이미 쓰이는 포트 있으면 `docker-compose.yml`에서 수정.

## 데이터 영속성

- `infra/qdrant/storage/` — Qdrant 컬렉션
- `infra/langfuse/volumes/` — Langfuse 전체 데이터

둘 다 `.gitignore`에 포함됨.
