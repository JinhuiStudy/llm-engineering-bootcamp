# Langfuse self-hosted (Day 12+)

Observability + Prompt Management + Eval / Scores. 모두 로컬.

## 🏗 아키텍처 (v3)

```
┌─────────┐   ┌──────────┐
│ langfuse├──▶│ Postgres │  메타데이터 (users/org/project)
│  web    │   │  16      │
│ (3000)  │   └──────────┘
│         │   ┌──────────┐
│         ├──▶│ClickHouse│  trace / observation 본체
│         │   │  24.3    │
│         │   └──────────┘
│         │   ┌──────────┐
│         ├──▶│  Redis   │  queue
│         │   └──────────┘
│         │   ┌──────────┐
│         └──▶│  MinIO   │  event/media blob (S3-compat)
└─────────┘   └──────────┘
      ▲
      │
┌─────┴────────┐
│ langfuse     │  백엔드 worker (ingest batch)
│   worker     │
└──────────────┘
```

총 **6 컨테이너**. RAM 2-3GB.

## 🚀 최초 기동

```bash
make langfuse-up
# 또는
docker compose -f infra/langfuse/docker-compose.yml up -d
```

**2-3분** 걸림 (clickhouse migrations + 이미지 pull).

## 🎬 첫 접속 순서

1. <http://localhost:3000> 열기
2. **Sign up** → 이메일/비번 아무거나 (로컬만 사용 — 실제 외부 가입 아님)
3. **New organization** → 이름 아무거나 (예: "ai-study")
4. **New project** → 이름 (예: "bootcamp")
5. **Settings → API Keys → Create**:
   - Public key: `pk-lf-...`
   - Secret key: `sk-lf-...` (한 번만 표시)
6. `.env`에 붙여넣기:
   ```
   LANGFUSE_HOST=http://localhost:3000
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   ```
7. 점검:
   ```bash
   cd shared
   uv run python -c "from ai_study.langfuse_client import get_langfuse; lf=get_langfuse(); print('OK' if lf else 'FAIL')"
   ```

## 🔭 주요 사용

### Tracing (Day 12)
```python
from ai_study.langfuse_client import observe, get_langfuse

@observe(name="my_rag_pipeline")
def rag(q):
    @observe(as_type="retriever")
    def retrieve(q): ...
    @observe(as_type="generation")
    def generate(q, ctx): ...
    ...
```

### Prompt Management
1. UI에서 **Prompts → New** → name/version/label/prompt 작성
2. 코드에서 fetch:
   ```python
   lf = get_langfuse()
   p = lf.get_prompt("rag_system", label="production")
   msg = p.compile(context=ctx, question=q)
   ```

### Score Attach (Day 9 연결)
```python
lf.score(
    trace_id=trace_id,
    name="faithfulness",
    value=0.87,
    comment="Ragas evaluator_llm=sonnet-4.6"
)
```

## 🔌 포트

| 포트 | 용도 |
|---|---|
| **3000** | Web UI + SDK 엔드포인트 |
| **9090** | MinIO S3 API (9000 내부 → 9090 외부 매핑, Qdrant 9000과 충돌 방지) |
| **9091** | MinIO Console |

내부용 (docker network):
- postgres:5432
- clickhouse:8123 (HTTP) / 9000 (native)
- redis:6379

## 💾 데이터

```
./volumes/
├── postgres/         # 메타데이터
├── clickhouse/       # trace 본체 (여기가 큰 용량 차지)
└── minio/            # event/media blob
```

### 초기화
```bash
make langfuse-down
rm -rf volumes
make langfuse-up     # 새 가입부터
```

### 부분 초기화 (clickhouse만)
```bash
docker compose -f infra/langfuse/docker-compose.yml down
rm -rf volumes/clickhouse
docker compose -f infra/langfuse/docker-compose.yml up -d
# → org/user는 유지, trace만 날아감
```

## 💡 Clickhouse 디스크 관리 (꼭 읽기)

Trace 양 많아지면 volumes/clickhouse 가 GB 단위로 커짐. TTL 설정 권장:

docker-compose.yml의 langfuse-worker 환경변수에 추가:
```yaml
LANGFUSE_CLICKHOUSE_TTL_DAYS: "30"     # 30일 후 자동 삭제
```

또는 직접 Clickhouse에 접속:
```bash
docker exec -it ai-study-langfuse-clickhouse clickhouse-client
# SQL:
ALTER TABLE traces MODIFY TTL timestamp + INTERVAL 30 DAY;
ALTER TABLE observations MODIFY TTL start_time + INTERVAL 30 DAY;
```

## 🧨 자주 발생하는 이슈

### 컨테이너 계속 재시작
- **원인**: RAM 부족. Docker Desktop **Settings → Resources → Memory 6GB+** 할당
- 확인: `docker stats`

### postgres unhealthy
- `volumes/postgres` 권한/데이터 문제
- 해결: `rm -rf volumes/postgres` 후 재기동

### web이 안 뜸
```bash
docker logs ai-study-langfuse-web --tail 100
```
- `ECONNREFUSED postgres:5432` — postgres 기다리는 중 (1-2분)
- `migration failed` — volumes/postgres 삭제 후 재기동
- `ClickHouse connection timeout` — clickhouse 시작 대기 중

### SALT / ENCRYPTION_KEY 경고
- production 아니면 무시. 공개 배포 시 `openssl rand -hex 32`로 교체 필수

### SDK에서 trace 가 안 뜸
1. `LANGFUSE_HOST=http://localhost:3000` 확인
2. PK/SK가 현재 project의 것인지
3. `lf.flush()` 호출 (batch 전송이라 즉시 안 감)
4. Web UI Settings → Tracing 에서 project가 맞는지
5. `time.sleep(2)` 기다리기 (worker 처리 지연)

### Mac 발열 / 배터리
- Day 12 때만 켜고 Day 13-14 필요시만. 상시 구동 비권장
- 또는 Langfuse Cloud 무료 tier (50k obs/mo) 사용

## 🔒 Production 배포 전 체크

- [ ] `SALT`, `ENCRYPTION_KEY`, `NEXTAUTH_SECRET` 교체 (openssl rand)
- [ ] `POSTGRES_PASSWORD`, `MINIO_ROOT_PASSWORD` 강한 비밀번호
- [ ] HTTPS 리버스 프록시 (Caddy / Traefik)
- [ ] Clickhouse TTL (LANGFUSE_CLICKHOUSE_TTL_DAYS)
- [ ] Postgres / Clickhouse backup 스케줄
- [ ] Port 3000/9090/9091 외부 노출 제거

## 🔗 참고

- [Langfuse docs — Self-hosting](https://langfuse.com/self-hosting)
- [Langfuse tracing](https://langfuse.com/docs/tracing)
- [Prompt management](https://langfuse.com/docs/prompt-management/overview)
- [Scores / evals](https://langfuse.com/docs/scores/overview)
- [Datasets](https://langfuse.com/docs/datasets/overview)
