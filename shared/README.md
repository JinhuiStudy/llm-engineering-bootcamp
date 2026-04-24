# shared/ — 공통 유틸리티 패키지 `ai_study.*`

14일 부트캠프의 **공통 딥스 + 핵심 헬퍼**. 모든 day 프로젝트가 `from ai_study.* import ...` 로 재사용.

## 🎯 왜 공통 패키지인가

- 13개 프로젝트가 각자 `load_dotenv()` / `OpenAI()` / `QdrantClient(...)` 반복 금지
- LLM provider 분기 + 재시도 + 비용 계산을 **한 곳에만**
- Day 14 포트폴리오에서 import 경로만 바꿔 이식

## 📦 설치

### 방법 1 — editable install (권장)

```bash
cd /Users/parkjinhui/Desktop/dev/ai-study
uv pip install -e ./shared     # root venv 사용 시
# 또는
cd shared && uv sync            # 독립 venv
```

### 방법 2 — 프로젝트별 path dep

각 프로젝트 `pyproject.toml`에:
```toml
dependencies = [
  "ai-study-shared @ file://${PROJECT_ROOT}/../../shared",
]
```

## 📁 모듈 구조

```
shared/
├── pyproject.toml          # 모든 deps (2026-04 기준)
├── README.md
└── ai_study/
    ├── __init__.py
    ├── config.py           # .env 로딩 + Settings dataclass
    ├── logging.py          # loguru
    ├── retry.py            # tenacity @with_retry
    ├── tokens.py           # count_tokens + estimate_cost + PRICING
    ├── llm.py              # chat / chat_stream (4 provider: openai/anthropic/gemini/ollama)
    ├── embeddings.py       # embed (openai/gemini/local SBERT)
    ├── vectors.py          # Qdrant helper (ensure_collection / upsert / search)
    ├── prompts.py          # Jinja2 기반 template render
    └── langfuse_client.py  # observe() no-op fallback + flush
```

## 🚀 사용 예

### LLM 호출
```python
from ai_study.llm import chat, chat_stream

answer = chat("anthropic", "Say hi", system="You are concise.")

for token in chat_stream("openai", "Write a haiku", temperature=0.8):
    print(token, end="", flush=True)
```

### 비용 계산
```python
from ai_study.tokens import count_tokens, estimate_cost

n = count_tokens("안녕하세요 세계", model="gpt-4o-mini")
cost = estimate_cost("claude-sonnet-4-6", input_tokens=10_000, output_tokens=2_000)
print(cost)  # claude-sonnet-4-6: 10000→2000 tokens = $0.0600
```

### Embedding + Qdrant
```python
from ai_study.embeddings import embed, embedding_dim
from ai_study.vectors import ensure_collection, upsert_texts, UpsertItem, search

dim = embedding_dim("openai")   # 1536
client = ensure_collection("my_docs", dim=dim)

vecs = embed(["Hello", "안녕"], provider="openai")
upsert_texts("my_docs", [
    UpsertItem(text="Hello", vector=vecs[0], payload={"lang":"en"}),
    UpsertItem(text="안녕",  vector=vecs[1], payload={"lang":"ko"}),
])

qv = embed(["Korean greeting"], provider="openai")[0]
for hit in search("my_docs", qv, top_k=2):
    print(hit.score, hit.payload["text"])
```

### Retry
```python
from ai_study.retry import with_retry

@with_retry
def flaky():
    ...  # tenacity가 429/529/timeout을 지수 백오프로 재시도
```

### Prompt templates
```python
from ai_study.prompts import render

# prompts/rag_answer.txt 또는 .j2 를 탐색 → 렌더
msg = render("rag_answer", context="...", question="...")
```

### Langfuse (Day 12+)
```python
from ai_study.langfuse_client import observe, flush

@observe(name="my_rag_step", as_type="retriever")
def retrieve(q: str):
    ...

# 앱 종료 시
flush()
```

## 🧪 Smoke test

```bash
cd shared

# LLM
uv run python -m ai_study.llm openai "In one line, what is RAG?"
uv run python -m ai_study.llm anthropic "In one line, what is RAG?"

# Pricing
uv run python -m ai_study.tokens

# Config dump
uv run python -c "from ai_study.config import settings; import json; print(json.dumps({k:(bool(v) if 'key' in k.lower() else v) for k,v in settings.__dict__.items() if not k.startswith('_')}, default=str, indent=2))"
```

## 🔄 업데이트

```bash
cd shared
uv sync --upgrade   # 모든 deps 최신
uv add "langfuse>=2.55"
```

## 🧨 자주 막히는 것

- **`ModuleNotFoundError: ai_study`** — `uv pip install -e ./shared` 안 했거나, 다른 venv에서 실행
- **`.env` 값이 안 읽힘** — `config.py`의 `_find_root()`가 `.env` 찾음. 루트에 `.env` 있는지 확인
- **`qdrant_client not installed`** — `uv sync` 먼저
- **SBERT 로컬 모델 다운로드 멈춤** — Hugging Face Hub 연결 확인, 또는 `HF_HOME` 바꾸기

## 📌 핵심 모듈별 한 줄

| 모듈 | 책임 |
|---|---|
| `config` | .env 로딩 + Settings singleton |
| `logging` | loguru 색상 로거 |
| `retry` | `@with_retry`로 지수 백오프 |
| `tokens` | `count_tokens`, `estimate_cost`, `PRICING` |
| `llm` | 4-provider `chat` / `chat_stream` |
| `embeddings` | 3-provider `embed` |
| `vectors` | Qdrant `ensure_collection` / `upsert` / `search` |
| `prompts` | Jinja2 template `render` |
| `langfuse_client` | `@observe` + no-op fallback |

## 🎁 확장 아이디어

- `cache.py` — Redis + embedding 기반 semantic cache
- `tools.py` — 공용 tool schema 헬퍼
- `chunking.py` — RecursiveCharacterTextSplitter wrapper + metadata injection
- `eval.py` — Ragas helper (metric/judge 기본값)
- `mcp_client.py` — MCP 클라이언트 사이드 헬퍼
