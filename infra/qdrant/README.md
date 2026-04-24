# Qdrant — 로컬 벡터 DB

Day 6부터 사용.

## 기동
```bash
make qdrant-up
# 또는
docker compose -f infra/qdrant/docker-compose.yml up -d
```

## 점검
- Dashboard: http://localhost:6333/dashboard
- Health: `curl http://localhost:6333/readyz`
- Collections: `curl http://localhost:6333/collections`

## 데이터 위치
`./storage/` 에 persistent volume. 재기동해도 유지.

## 초기화 (컬렉션 전체 삭제)
```bash
make qdrant-down
rm -rf infra/qdrant/storage
make qdrant-up
```

## 리소스
로컬 실험 규모 (~100k vectors)에서는 RAM 1-2GB, 디스크 수백MB.
