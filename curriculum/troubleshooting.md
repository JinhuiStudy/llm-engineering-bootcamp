# Troubleshooting / FAQ — 14일 부트캠프

> 막히면 먼저 여기. 그다음에 구글. 30분 넘기지 말고 Claude/ChatGPT에 풀스택트레이스 + 환경 정보 붙여넣고 질문.

## 목차
- [환경/설치](#환경설치)
- [API 키 / 크레딧](#api-키--크레딧)
- [Rate limit / Timeout / Network](#rate-limit--timeout--network)
- [Docker (Qdrant / Langfuse)](#docker-qdrant--langfuse)
- [Qdrant 쿼리](#qdrant-쿼리)
- [Embedding / RAG 품질](#embedding--rag-품질)
- [Structured Output / Pydantic](#structured-output--pydantic)
- [Tool Use / Agent](#tool-use--agent)
- [LangGraph](#langgraph)
- [MCP](#mcp)
- [Langfuse / Observability](#langfuse--observability)
- [Local LLM (Ollama / vLLM / RunPod)](#local-llm-ollama--vllm--runpod)
- [비용 관리](#비용-관리)
- [마음](#마음)

---

## 환경/설치

### Q. `python3 --version` 이 3.9인데 3.11 깔았어도 안 바뀜
```bash
brew install python@3.12
echo 'export PATH="/opt/homebrew/opt/python@3.12/libexec/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
python3 --version
```
pyenv 쓰면: `pyenv install 3.12.1 && pyenv global 3.12.1`

### Q. `uv sync` 실패 (`pyproject.toml not found`)
현재 디렉토리 확인. `cd shared` 먼저. 루트에는 pyproject.toml 없음.

### Q. `uv sync` 중 SSL 에러
회사 망이면:
```bash
export REQUESTS_CA_BUNDLE=/path/to/corp-ca-bundle.pem
export SSL_CERT_FILE=$REQUESTS_CA_BUNDLE
```
또는 `uv --native-tls`

### Q. Python 인증서 에러 (`ssl.SSLCertVerificationError`)
Python.org 설치본이면: `/Applications/Python\ 3.12/Install\ Certificates.command` 실행.

### Q. `git: command not found`
Xcode CLT 필요: `xcode-select --install`

### Q. shared 패키지를 day 프로젝트에서 import 안 됨
Editable install:
```bash
cd shared
uv pip install -e .
```
또는 workspace 설정으로 공용 venv.

---

## API 키 / 크레딧

### Q. OpenAI: `Incorrect API key provided: sk-...***`
- `.env` 줄 끝에 공백/따옴표/세미콜론 붙었는지 확인
- `sk-proj-...` 전체 복사했는지 (잘림 확인)
- 새 프로젝트 key 발급 후 org default 확인

### Q. Anthropic: 401 Unauthorized
- `sk-ant-...` 시작
- `x-api-key` 헤더 (Bearer 아님)
- `anthropic-version: 2023-06-01` 헤더 필수

### Q. Gemini: `API key not valid`
- Google Cloud에서 해당 프로젝트에 Generative Language API 활성화
- AI Studio key가 특정 프로젝트에 묶임 — 프로젝트 매칭 확인

### Q. 방금 $5 충전했는데 403
반영 10분 정도 걸림. 더 기다린 후 재시도. 한 시간 넘게 안 되면 support.

### Q. 돌연 "Insufficient quota"
하루 Usage limit 도달. 대시보드에서 확인 + 필요하면 상향.

---

## Rate limit / Timeout / Network

### Q. 첫 호출부터 429
Tier 1 RPM 낮음. 호출 사이 delay 넣거나 tier 상향 기다리기.
```python
import time
for item in items:
    call()
    time.sleep(1)  # 임시
```
또는 tenacity:
```python
@retry(wait=wait_random_exponential(min=1,max=60), stop=stop_after_attempt(6))
```

### Q. Streaming 중 timeout
- client timeout 기본 짧을 수 있음. `client = Anthropic(timeout=120.0)`
- 네트워크 재시도 중이면 SSE 스트림 끊김. retry 전제로 짜기

### Q. `httpx.ConnectError: [Errno 60] Operation timed out`
- 프록시: `HTTPS_PROXY=http://proxy:port`
- 방화벽/회사망: VPN 안 켠 상태일 수 있음

### Q. Anthropic 529 overloaded
Anthropic 서버 바쁨. backoff 더 길게 (`wait_random_exponential(min=5, max=120)`).

---

## Docker (Qdrant / Langfuse)

### Q. `Cannot connect to the Docker daemon`
Docker Desktop 실행 중인가? 앱 시작 후 `docker ps`.

### Q. `docker compose up` 멈춤
- 이미지 다운로드 중: `docker compose logs -f`로 확인
- 디스크 부족: `docker system prune -a` (주의: 다른 이미지 삭제됨)

### Q. Qdrant 포트 6333 충돌
```bash
lsof -i :6333
# PID 찾아서 kill 또는 docker-compose.yml에서 포트 변경 6334:6333
```

### Q. Langfuse 컨테이너 자꾸 죽음
- RAM 부족 (최소 4GB 필요). Docker Desktop settings에서 할당 증가
- Clickhouse 초기화 실패: `docker compose down -v && docker compose up -d` (볼륨 초기화)
- 로그: `docker compose logs langfuse-web langfuse-worker`

### Q. Apple Silicon 경고
compose에 `platform: linux/arm64` 명시 or 최신 이미지 사용. Langfuse는 multi-arch 지원.

### Q. Clickhouse 디스크 폭발
`MERGE TREE` partition TTL:
```yaml
# Langfuse docker-compose 환경변수
CLICKHOUSE_TRACES_DAYS: "30"
CLICKHOUSE_OBSERVATIONS_DAYS: "30"
```

---

## Qdrant 쿼리

### Q. `collection not found`
```python
client.create_collection(name="foo", vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
```
우선 생성.

### Q. `Wrong input: Vector dimension error: expected X, got Y`
임베딩 모델 교체했는데 같은 collection 재사용. 재생성 필수 — `client.delete_collection("foo")` 후 create.

### Q. Search 결과 scores 전부 비슷 (~0.5)
- 임베딩 공간이 무너짐 — 모델 로딩 실수 확인
- 또는 쿼리/문서가 언어 다름 (영어 문서에 한국어 쿼리)
- E5 prefix 누락 — `query: ` / `passage: ` 확인

### Q. HNSW 튜닝 해도 latency 안 개선
- collection 크기 1k 미만이면 튜닝 의미 없음
- Payload 필터 heavy → 인덱스 필드 선언: `client.create_payload_index(...)`

---

## Embedding / RAG 품질

### Q. 답이 명백히 context에 있는데 retrieval이 놓침
- chunk 크기 확인 (너무 작/큼)
- paraphrase 쿼리 → multi-query 시도
- 숫자/고유명사 있으면 hybrid (BM25 추가)
- cross-encoder rerank 추가

### Q. 답변이 context 있는데 환각
- 프롬프트: "ONLY from context, else 모른다"
- Pydantic `Answer(citations: list[int])` 강제로 근거 index 명시
- 모델 격상 (haiku → sonnet)

### Q. Unanswerable 질문에 "모른다" 안 함
- 프롬프트 강화: "If the answer is not explicitly stated, reply: 근거 부족."
- Few-shot 예시로 `Q: ... A: 근거 부족.` 추가

### Q. 한국어 RAG 품질 낮음
- 임베딩 모델 변경: `multilingual-e5-large` or `bge-m3`
- Tokenizer 차이 주의 — 비용 계산에 o200k_base
- Reranker도 multilingual (`Cohere rerank-multilingual-v3.0`)

---

## Structured Output / Pydantic

### Q. OpenAI strict mode `400: Invalid schema`
- `additionalProperties: false` 필요
- 모든 필드 required or `null` union
- `$ref`는 **같은 schema 내부**만
- Instructor 쓰면 자동 처리

### Q. `ValidationError: field required`
모델이 필드 누락. description 늘리거나 Optional로 완화:
```python
field: str | None = None
```

### Q. Pydantic `EmailStr` ImportError
`pip install "pydantic[email]"` or `uv add pydantic[email]`

### Q. Claude tool_use로 structured 받았는데 JSON이 string
`content[0].input` 확인 (dict). `content[0].text` 아님.

---

## Tool Use / Agent

### Q. Claude가 tool 안 부름
- description 빈약 / 짧음 → 길게 + 예시 + "언제 쓰면"
- system prompt에 "use tools when applicable" 명시
- `tool_choice: "auto"` 확인

### Q. Parallel tool use 트리거 안 됨
- 모델이 결정. 강제 불가
- 프롬프트로 유도: "A와 B를 **동시에** 조회하고"

### Q. tool_result 400
- Anthropic: `content` string 또는 list of content blocks. dict 넘기면 400
- OpenAI: `{"type":"tool_result","tool_use_id":...,"content":"..."}` — JSON string

### Q. 무한 루프 발생
Safety rail:
```python
if iter >= 10: abort
if same_call_repeated(3): abort
if total_tokens > 50000: abort
if elapsed > 60s: abort
```

---

## LangGraph

### Q. State가 덮어써져서 messages 사라짐
`add_messages` reducer 빠짐:
```python
messages: Annotated[list[BaseMessage], add_messages]
```

### Q. `conditional_edges` 조건이 안 맞음
반환값과 매핑 dict의 키 정확히 일치. 오타 흔함.

### Q. Checkpoint 세션 재개 안 됨
`thread_id` 같아야 함. config에서 `{"configurable": {"thread_id": "user-123"}}`

### Q. `interrupt_before` 후 재개 안 됨
`app.invoke(None, config)` — None이 중요. 새 input 넘기면 처음부터.

---

## MCP

### Q. Claude Desktop에서 server 연결 안 됨
- `claude_desktop_config.json` 경로: `~/Library/Application Support/Claude/`
- 절대경로 사용 (`~` 안 풀림)
- Claude Desktop **완전 재시작** (quit → run)
- 로그: `~/Library/Logs/Claude/mcp.log`

### Q. stdio 서버가 tool 못 찾음
`print()` 쓰면 안 됨 (stdout에 로그 찍혀 JSON-RPC 깨짐). `logging.stderr` 사용.

### Q. Inspector에서 tool은 보이는데 Claude Desktop에서 안 보임
- config 문법 (JSON comma)
- env vars 명시적으로 넘겼는지
- Claude Desktop 로그 확인

### Q. `@mcp.tool` description 적었는데 모델이 잘못 호출
docstring/description에 **예시 + 언제 쓰는지** 추가.

---

## Langfuse / Observability

### Q. `@observe` 써도 trace 안 나옴
- `Langfuse()` 싱글톤 생성 확인
- `langfuse.flush()` 호출 (async batch — 즉시 안 가는 경우)
- LANGFUSE_HOST / PUBLIC_KEY / SECRET_KEY env 확인

### Q. Nested span이 flat으로 보임
`@observe` 중첩은 자동. 수동 `langfuse.start_as_current_span` 쓰면 context 관리 필요.

### Q. Generation span에 usage 빈값
`update_current_observation(usage=...)` 호출 필요:
```python
langfuse.update_current_observation(
    input=messages,
    output=response.content,
    model="claude-haiku-4-5",
    usage={"input": 100, "output": 50}
)
```

### Q. Prompt fetch 실패
- Langfuse UI에서 prompt를 `production` label로 publish 했는지
- Name/version/label 오타

---

## Local LLM (Ollama / vLLM / RunPod)

### Q. Ollama `http://localhost:11434` 접속 안 됨
`ollama serve` 실행 필요 (앱 실행 시 자동이지만 CLI에서도 시작 가능).

### Q. OpenAI SDK `base_url=localhost:11434/v1` 에러
`api_key` 빈 문자열이면 400 — `api_key="ollama"` (dummy string).

### Q. Ollama에서 tool_calling 실패
모델이 tool 지원 확인 — `ollama list`에서 `<think>` 또는 tool template. Qwen3 / Llama 3.3 지원.

### Q. vLLM 시작 시 VRAM OOM
- `--gpu-memory-utilization 0.8` 낮추기
- `--max-model-len 4096` 줄이기
- `--quantization awq` (AWQ 양자화 모델만)

### Q. RunPod Serverless cold start 너무 길다
- Endpoint 설정에서 `min_workers: 1` (warm)
- 작은 모델 + AWQ 양자화
- `MAX_MODEL_LEN` 줄이기

### Q. RunPod에서 OpenAI SDK tool_calling 파싱 에러
- vLLM의 `chat-template` 확인
- `tool_call_parser` 명시 필요한 모델 있음 (Qwen3 등)
- worker-vllm 최신 버전 사용

---

## 비용 관리

### Q. 밤사이 agent loop 잘못 짜서 $100+ 나감
- OpenAI/Anthropic 대시보드에서 **Hard limit** 설정 ($20 등)
- Agent에 token budget (state에 누적)
- 개발 중엔 Haiku/4o-mini/Flash만. Sonnet은 검증 후

### Q. Eval 한 번 돌리는 게 $10 넘음
- Sample 20건 PR / nightly full 구조
- Judge를 큰 모델만 고집 X — 4o-mini도 판정 비슷
- Prompt caching 적용

### Q. Embedding 비용 체감
- `text-embedding-3-small`로 전환 (`-large` 대비 1/6)
- `dimensions=512` 잘라쓰기 (Matryoshka) — 97% 품질 유지
- 로컬 `multilingual-e5-large` 대체

---

## 마음

### Q. Day 5쯤 번아웃. 의지 안 나옴
- `curriculum/recovery-playbook.md` 참조
- 오늘 필수만. Stretch 다 버려
- 잠 8시간 확보 (14일 중 3-4일은 이렇게 풀어주는 게 정상)

### Q. Day 8 고급 RAG에서 감 잃음
- 모든 걸 한 번에 이해하려 하지 말고
- baseline → +rewrite → +hybrid → +rerank 순서로 **하나씩** 추가
- 매번 수치 기록. 결과 안 좋으면 버려

### Q. "이렇게 대충 짜면 의미 있나?" 불안
- 의미 있음. 2주 안에 production-grade 완성하는 게 목표 아님
- **돌아가는 것**이 우선, **Eval로 측정 가능한 것**이 다음
- 14일 끝에 포트폴리오 들고 다른 사람한테 보이면 그 피드백이 다음 학습

### Q. 다 끝냈는데 뭔가 부족
- `curriculum/extras.md` 참고 — 보안 / fine-tuning / multi-agent / vision / ...
- 이 14일은 **시작**. 꾸준함이 더 중요
- 포트폴리오 repo에 계속 기능 추가 (2주 후 CrewAI, 한 달 후 fine-tuning 등)

---

## 🆘 마지막 수단

30분 넘게 막혔으면:
1. **에러 풀스택 + 환경 정보** (OS, Python 버전, SDK 버전)
2. **재현 최소 코드**
3. 이 troubleshooting 문서 검색했는지
4. 공식 문서 검색했는지

그 다음 Claude/ChatGPT에 질문. 그래도 안 되면 GitHub Issue에.

**자존심 쓰지 말 것**. 막힌 30분이 9시간이 되면 부트캠프가 3일 밀린다.
