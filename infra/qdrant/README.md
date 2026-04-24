# Qdrant — 로컬 벡터 DB (Day 6+)

## 🚀 기동

```bash
make qdrant-up
# 또는
docker compose -f infra/qdrant/docker-compose.yml up -d
```

### 점검
- Dashboard: <http://localhost:6333/dashboard>
- Health: `curl http://localhost:6333/readyz`
- Collections: `curl http://localhost:6333/collections`
- Metrics: `curl http://localhost:6333/metrics` (Prometheus 형식)

## 🐍 Python 클라이언트 (shared helper 사용)

```python
from ai_study.vectors import ensure_collection, upsert_texts, UpsertItem, search

client = ensure_collection("my_docs", dim=1536)   # OpenAI 3-small
# ... upsert / search ...
```

또는 raw:
```python
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
c = QdrantClient("http://localhost:6333")
c.create_collection("foo", vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
```

## ⚙️ 주요 파라미터 튠 포인트

| 파라미터 | 의미 | 실측 영향 |
|---|---|---|
| `distance` | Cosine / Dot / Euclid / Manhattan | L2-normalized 임베딩에선 Cosine=Dot |
| `hnsw.m` | edge per node (default 16) | 8 = 속도↑, 32 = recall↑ |
| `hnsw.ef_construct` | 빌드 시 탐색 폭 (default 100) | 높이면 인덱싱 느려짐, recall↑ |
| `hnsw.ef` (search) | 쿼리 시 탐색 폭 | 16 = 빠름, 256 = recall↑↑ |
| `on_disk` | 벡터 디스크 저장 | 1M+ 벡터에서 RAM 절감 |
| `quantization_config` | Scalar int8 / Binary | 메모리 4-32배 절감, recall -3~10% |

예시 — 10M+ 벡터 대응:
```python
from qdrant_client.http.models import (
    VectorParams, Distance, HnswConfigDiff, ScalarQuantization, ScalarQuantizationConfig, ScalarType
)

c.create_collection(
    "big",
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE,
        on_disk=True,  # vectors on disk
    ),
    hnsw_config=HnswConfigDiff(m=32, ef_construct=200),
    quantization_config=ScalarQuantization(
        scalar=ScalarQuantizationConfig(
            type=ScalarType.INT8,
            quantile=0.99,
            always_ram=True,
        )
    ),
)
```

## 📁 데이터 위치

- `./storage/` — 영속 볼륨 (재기동해도 유지)
- `.gitignore` 에 포함됨

### 초기화 (컬렉션 전체 삭제)
```bash
make qdrant-down
rm -rf infra/qdrant/storage
make qdrant-up
```

## 💾 리소스 감각

| 규모 | RAM | 디스크 |
|---|---|---|
| 10k 벡터 × 1536d | ~100MB | ~60MB |
| 100k × 1536d | ~700MB | ~600MB |
| 1M × 1536d (on_disk) | ~200MB | ~6GB |
| 10M × 1024d (int8 quant) | ~2-3GB | ~40GB |

## 🔎 Dashboard 탐색 팁

`http://localhost:6333/dashboard` 에서:
- 왼쪽 사이드바 Collections → 클릭 → Info 탭 (points 수, index 상태)
- Points 탭 → payload 기준 필터로 실제 데이터 확인
- `distance` 바꾸려면 컬렉션 재생성 필수 (migrate 없음)

## 🧨 자주 만나는 에러

- **`Wrong input: Vector dimension error: expected 1536, got 384`** — 임베딩 모델 바꿈. 컬렉션 재생성 필수
- **`collection not found`** — `ensure_collection` 먼저 호출
- **`retry_with_lower_query_limit`** — `ef_search` 너무 큼. 낮추기
- **`storage` 퍼미션** — `sudo chown -R $(whoami) infra/qdrant/storage`
- **Dashboard 403** — 보안 설정 (`QDRANT__SERVICE__API_KEY` 설정했으면 헤더 필요)

## 🔗 참고

- [Qdrant docs](https://qdrant.tech/documentation/)
- [HNSW 튜닝](https://qdrant.tech/documentation/concepts/indexing/)
- [Hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/)
- [Quantization](https://qdrant.tech/documentation/guides/quantization/)
