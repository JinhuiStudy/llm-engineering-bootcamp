# 📦 Pre-Digested — 공식 문서에서 직접 뽑아온 핵심 코드/사실

> **2026-04-25 기준 WebFetch로 실제 공식 페이지 열어서 추출.** 링크 일일이 열지 말고 여기서 대부분 해결.
> 각 섹션은 "**공식 문서 원문 요약 + 복붙 가능 코드 + 2026 최신 사항**".

---

## 🚨 2026년 최신 필수 사항 (먼저 읽어)

### 1. Anthropic 도메인 이전
- **기존**: `docs.anthropic.com/...`
- **현재**: `platform.claude.com/docs/en/...` (301 redirect)
- **SDK 엔드포인트는 유지**: `https://api.anthropic.com/v1/messages`
- 코드는 변경 없음. **문서 URL만 업데이트**.

### 2. Claude 모델 이름 (2026-04)
```
claude-opus-4-7         ← flagship, adaptive thinking 권장
claude-opus-4-6
claude-opus-4-5
claude-sonnet-4-6       ← workhorse
claude-sonnet-4-5
claude-haiku-4-5        ← fast/cheap
claude-haiku-3-5        ← legacy (deprecated soon)
```
- **Sonnet 3.7 deprecated**
- Context window: **1M tokens** (모든 4.x)
- New features: **Adaptive thinking (4.7 권장)**, **Effort parameter (4.5+)**, **Compaction (4.6/4.7)**, **Agent Skills** (PowerPoint/Excel/Word/PDF)

### 3. Gemini 모델 (2026-04)
- **`gemini-3-flash-preview`** ← 최신 (gemini-2.5-flash → 업그레이드)
- `gemini-2.5-pro`, `gemini-2.5-flash` 아직 작동하지만 3가 권장
- 새 SDK: `from google import genai` (구 `google-generativeai`는 레거시)

### 4. OpenAI Cookbook URL
- **기존**: `cookbook.openai.com/...`
- **현재**: `developers.openai.com/cookbook/...` (308 redirect)

### 5. LangGraph 도메인 이전
- **기존**: `langchain-ai.github.io/langgraph`
- **현재**: `docs.langchain.com/oss/python/langgraph`

---

## Day 1 — LLM 기초

### Google ML Crash Course — LLM (공식 요약)
- **3대 주제**: Language Model Fundamentals / LLMs / Optimization Techniques
- **학습 목표** (공식):
  - 언어 모델 타입 정의 (n-gram → RNN → Transformer)
  - Context/parameters가 LLM을 어떻게 만드는가
  - Self-attention 메커니즘 설명
  - LLM의 **3가지 주요 문제**(소스 원문) 식별
  - Fine-tuning/distillation/prompt engineering 이해
- **핵심 개념**: Tokens, N-grams, Context, RNN limitations, Attention
- 🔗 https://developers.google.com/machine-learning/crash-course/llm

### 복붙 코드: tiktoken 토큰 카운트
```python
import tiktoken

# OpenAI 4o/4o-mini용
enc = tiktoken.encoding_for_model("gpt-4o-mini")  # o200k_base
print(len(enc.encode("안녕하세요 세계")))  # ~4-5 tokens

# 이전 GPT-4용
enc_old = tiktoken.get_encoding("cl100k_base")
print(len(enc_old.encode("안녕하세요 세계")))  # ~8-10 tokens (2배 차이!)
```

### 복붙 코드: 3사 토큰 카운트 비교
```python
# OpenAI
from openai import OpenAI; c = OpenAI()
# 토큰은 tiktoken으로 로컬 계산

# Anthropic 공식 카운트
import anthropic
a = anthropic.Anthropic()
r = a.messages.count_tokens(
    model="claude-haiku-4-5",
    messages=[{"role":"user","content":"안녕하세요"}]
)
print(r.input_tokens)

# Gemini 공식 카운트
from google import genai
g = genai.Client()
print(g.models.count_tokens(model="gemini-2.5-flash", contents="안녕하세요"))
```

---

## Day 2 — 3사 API

### OpenAI (Chat Completions)
```python
from openai import OpenAI
client = OpenAI()  # OPENAI_API_KEY env 자동 인식

r = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system","content":"You are helpful."},
        {"role":"user","content":"Say hi"}
    ],
    max_tokens=100,
)
print(r.choices[0].message.content)
print(r.usage)  # prompt_tokens / completion_tokens / total_tokens
```

### Anthropic Messages
```python
import anthropic
client = anthropic.Anthropic()  # ANTHROPIC_API_KEY env

r = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,  # ⚠️ 필수! 없으면 400
    system="You are helpful.",  # top-level
    messages=[{"role":"user","content":"Say hi"}],
)
print(r.content[0].text)
print(r.usage)  # input_tokens / output_tokens / cache_*
print(r.stop_reason)  # end_turn | max_tokens | tool_use | stop_sequence
```

### Gemini (google-genai, 2026 신 SDK)
```python
from google import genai
client = genai.Client()  # GOOGLE_API_KEY env (권장. GEMINI_API_KEY도 Google SDK가 인식)

r = client.models.generate_content(
    model="gemini-3-flash-preview",  # 2026-04 최신
    contents="Explain how AI works in a few words",
    config={"system_instruction": "You are helpful.", "temperature": 0.2}
)
print(r.text)
print(r.usage_metadata)
```

### Streaming 3사

**OpenAI**:
```python
stream = client.chat.completions.create(
    model="gpt-4o-mini", messages=[...], stream=True,
    stream_options={"include_usage": True},  # 마지막 chunk에 usage
)
for chunk in stream:
    if chunk.choices:
        print(chunk.choices[0].delta.content or "", end="")
```

**Anthropic** (context manager):
```python
with client.messages.stream(
    model="claude-haiku-4-5", max_tokens=1024,
    messages=[{"role":"user","content":"..."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**Gemini**:
```python
for chunk in client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents="...",
):
    print(chunk.text or "", end="", flush=True)
```

---

## Day 3 — Prompt Engineering + Security

### Anthropic Interactive Prompt Tutorial
- 🔗 https://github.com/anthropics/prompt-eng-interactive-tutorial
- **9챕터 + appendix**. Jupyter notebook으로 직접 실행
- 순서: `Anthropic API` (ch1) → `Being Clear and Direct` (ch2) → `Assigning Roles` (ch3) → `Separating Data and Instructions` (ch4) → `Formatting Output and Speaking for Claude` (ch5) → `Precognition (CoT)` (ch6) → `Using Examples (Few-shot)` (ch7) → `Avoiding Hallucinations` (ch8) → `Complex Prompts from Scratch` (ch9)

### OWASP LLM Top 10 v2.0 (2025) — 체크리스트
1. **LLM01 Prompt Injection** — direct/indirect/payload splitting/encoded
2. **LLM02 Sensitive Info Disclosure** — PII leak
3. **LLM03 Supply Chain** — 모델/deps 신뢰
4. **LLM04 Data/Model Poisoning**
5. **LLM05 Improper Output Handling** — SQL/XSS
6. **LLM06 Excessive Agency** — tool sandbox
7. **LLM07 System Prompt Leakage**
8. **LLM08 Vector/Embedding Weakness**
9. **LLM09 Misinformation** — citations로 대응
10. **LLM10 Unbounded Consumption** — rate limit
- 🔗 https://owasp.org/www-project-top-10-for-large-language-model-applications/

### Prompt-Guard 2 (Meta) — 86M 로컬 classifier
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL = "meta-llama/Llama-Prompt-Guard-2-86M"
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def classify(text: str) -> str:
    inputs = tok(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    return model.config.id2label[logits.argmax().item()]
    # 반환: "INJECTION" | "JAILBREAK" | "BENIGN"

# Day 3 injection_lab 결과:
# - 악의 샘플 탐지율 ~90%
# - 정상 샘플 오탐율 ~3%
```

---

## Day 4 — Structured Output

### OpenAI — Pydantic + strict (공식 cookbook 원문 코드)
```python
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",  # ← 이 버전 이후만 strict 보장
    messages=[
        {"role":"system","content":"You are a helpful math tutor."},
        {"role":"user","content":"Solve 8x + 7 = -23"}
    ],
    response_format=MathReasoning,
)

msg = completion.choices[0].message
if msg.refusal:
    print(f"Refused: {msg.refusal}")
else:
    parsed: MathReasoning = msg.parsed  # 타입 안전!
    for step in parsed.steps:
        print(step.explanation, "→", step.output)
    print("Answer:", parsed.final_answer)
```

### Strict mode 제약 (공식 문서)
- **모든 필드 `required`** (Optional은 `X | None` union)
- **`additionalProperties: false`** 필수
- `$ref` 같은 schema 내부만
- Enum은 `Literal[...]`로

### Anthropic Structured Output (2026)
**Strict tool use**로 달성 (native `response_format` 도 GA):
```python
class UserInfo(BaseModel):
    name: str
    age: int

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    tools=[{
        "name": "record_user_info",
        "description": "Record user information",
        "input_schema": UserInfo.model_json_schema(),
        "strict": True,  # ← 2026 신규, schema 준수 100% 보장
    }],
    tool_choice={"type": "tool", "name": "record_user_info"},
    messages=[{"role":"user","content":"..."}],
)
# response.content[0].input 이 Pydantic dict
```

### Gemini — response_schema
```python
class Recipe(BaseModel):
    name: str
    ingredients: list[str]

r = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Give me a cookie recipe",
    config={
        "response_mime_type": "application/json",
        "response_schema": Recipe,  # Pydantic 직접 전달
    },
)
recipe: Recipe = r.parsed  # 자동 파싱
```

---

## Day 5 — Tool Use

### Anthropic Tool Use (공식 원문 기반)
```python
import anthropic
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get current weather for a city. Use when user asks about weather, temperature, or climate in a specific location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type":"string","description":"City name, e.g. Seoul"},
                "units": {"type":"string","enum":["C","F"],"default":"C"},
            },
            "required":["city"],
        },
        "strict": True,  # 2026 신규
    }],
    messages=[{"role":"user","content":"서울 날씨"}],
)

# 응답 처리
if response.stop_reason == "tool_use":
    for block in response.content:
        if block.type == "tool_use":
            print(f"Call: {block.name}({block.input})")
            print(f"ID: {block.id}")  # 다음 턴 tool_result에 필요

            # 실제 실행 후
            result = {"temp": 22, "condition": "sunny"}

            # 다음 호출
            followup = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=1024,
                tools=[...],
                messages=[
                    {"role":"user","content":"서울 날씨"},
                    {"role":"assistant","content": response.content},
                    {"role":"user","content":[{
                        "type":"tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),  # ⚠️ dict 아닌 string or content blocks
                    }]},
                ],
            )
```

### stop_reason 값 (공식)
- `end_turn` — 정상 종료
- `max_tokens` — 잘림 (증량 필요)
- `tool_use` — tool 실행 대기 상태
- `stop_sequence` — stop sequences 매칭
- `pause_turn` — (새) 긴 agentic 작업 pause

### Anthropic 2026 신규 서버 tools
```python
# Web Search
tools=[{"type":"web_search_20260209","name":"web_search"}]

# Code Execution (sandboxed)
tools=[{"type":"code_execution_20250825","name":"code_execution"}]

# Web Fetch
tools=[{"type":"web_fetch_20250910","name":"web_fetch"}]
```
Web search + web fetch는 **code_execution과 함께 쓰면 무료**.

### OpenAI Function Calling (Responses API 권장, 2026)
```python
r = client.responses.create(
    model="gpt-4o",
    input="서울 날씨",
    tools=[{
        "type": "function",
        "name": "get_weather",
        "description": "...",
        "parameters": {...},
        "strict": True,  # arguments도 스키마 준수
    }]
)
for item in r.output:
    if item.type == "function_call":
        print(item.name, item.arguments)
```

### Gemini Function Calling
```python
from google.genai import types

tools = [types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="get_weather",
        description="...",
        parameters={...},
    )
])]

r = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="서울 날씨",
    config={"tools": tools},
)
for fc in (r.function_calls or []):
    print(fc.name, fc.args)
```

---

## Day 6 — Embedding + Qdrant

### Qdrant Quickstart (공식 원문 그대로)
```bash
# Docker로 기동
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant

# 확인: http://localhost:6333/dashboard
```

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(url="http://localhost:6333")

# Collection 생성
client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    # OpenAI text-embedding-3-small = 1536
)

# 벡터 + payload upsert
client.upsert(
    collection_name="test_collection",
    wait=True,
    points=[
        PointStruct(id=1, vector=[0.05]*1536, payload={"city":"Berlin"}),
        PointStruct(id=2, vector=[0.19]*1536, payload={"city":"London"}),
    ],
)

# Search (2026 기준: query_points 사용, 구 search 는 deprecated)
result = client.query_points(
    collection_name="test_collection",
    query=[0.2]*1536,
    limit=3,
).points
for pt in result:
    print(pt.id, pt.score, pt.payload)
```

### OpenAI Embeddings
```python
r = client.embeddings.create(
    model="text-embedding-3-small",  # 1536d, 싸고 빠름
    input=["hello", "안녕"]
)
vecs = [d.embedding for d in r.data]
# large: text-embedding-3-large (3072d). dimensions=1024로 자르면 비용 3배 절감
```

### Gemini Embeddings
```python
r = client.models.embed_content(
    model="text-embedding-004",  # 768d
    contents=["hello", "안녕"],
    config={"task_type": "RETRIEVAL_DOCUMENT"},
    # query는 "RETRIEVAL_QUERY"로 다르게!
)
vecs = [e.values for e in r.embeddings]
```

### 로컬 SBERT (한국어 강함)
```python
from sentence_transformers import SentenceTransformer
m = SentenceTransformer("intfloat/multilingual-e5-large")
vecs = m.encode([
    "query: Korean greeting",    # ⚠️ prefix 필수!
    "passage: 안녕하세요 세계"
], normalize_embeddings=True)
```

---

## Day 7 — 기본 RAG

### LangChain LCEL (2026 표준)
```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

emb = OpenAIEmbeddings(model="text-embedding-3-small")
vs = QdrantVectorStore.from_existing_collection(
    collection_name="docs", embedding=emb, url="http://localhost:6333"
)
retriever = vs.as_retriever(search_kwargs={"k": 5})

prompt = ChatPromptTemplate.from_template("""
Answer ONLY from context. If not found, say "근거 부족".
Context: {context}
Question: {question}
""")

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()
)
answer = chain.invoke("Qdrant에서 collection 만드는 법?")
```

---

## Day 8 — 고급 RAG: Contextual Retrieval (공식 수치)

### Anthropic Contextual Retrieval (2024-09) — 검증된 수치
| 기법 | Retrieval 실패율 |
|---|---|
| Baseline (embedding only) | 5.7% |
| **Contextual Embeddings** | **3.7%** (35% 감소) |
| **+ BM25 (Contextual Hybrid)** | **2.9%** (49% 감소) |
| **+ Reranker** | **1.9%** (67% 감소) |

### 공식 prompt template (그대로 복붙)
```
<document>{{WHOLE_DOCUMENT}}</document>
Here is the chunk we want to situate within the whole document
<chunk>{{CHUNK_CONTENT}}</chunk>
Please give a short succinct context to situate this chunk within the overall document
for the purposes of improving search retrieval of the chunk. Answer only with the
succinct context and nothing else.
```

### Before/After 예시 (공식)
- **Before**: "The company's revenue grew by 3% over the previous quarter."
- **After**: "This chunk is from an SEC filing on ACME corp's performance in Q2 2023; the previous quarter's revenue was $314 million. The company's revenue grew by 3% over the previous quarter."

### 비용 (공식)
- Prompt caching 적용 시 document 1M 토큰당 **~$1.02** 일회성

### 코드 스케치
```python
def contextualize(full_doc: str, chunk: str) -> str:
    r = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        # 📌 prompt caching으로 full_doc 재사용
        system=[{
            "type":"text",
            "text": f"<document>{full_doc}</document>",
            "cache_control":{"type":"ephemeral"}
        }],
        messages=[{"role":"user","content":
            f"Here is the chunk we want to situate within the whole document\n"
            f"<chunk>{chunk}</chunk>\n"
            f"Please give a short succinct context to situate this chunk...\n"
            f"Answer only with the succinct context and nothing else."
        }]
    )
    return r.content[0].text

# 각 chunk에 prepend
contextualized = f"{contextualize(full_doc, chunk)}\n\n{chunk}"
# 이걸 embed
```

---

## Day 9 — Ragas Eval

### Ragas v0.2+ 표준 구조 (API 변경 있음 주의)
```python
from ragas import EvaluationDataset, evaluate
from ragas.metrics import (
    Faithfulness,
    ResponseRelevancy,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
)
from ragas.llms import LangchainLLMWrapper
from langchain_anthropic import ChatAnthropic

# Judge (testee와 다른 모델 권장)
judge_llm = LangchainLLMWrapper(
    ChatAnthropic(model="claude-sonnet-4-6", temperature=0)
)

# 데이터셋 (각 sample은 question + answer + retrieved_contexts + reference)
dataset = EvaluationDataset.from_list([
    {
        "user_input": "RAG flow 7단계는?",
        "response": "Load → Split → Embed → Store → ...",
        "retrieved_contexts": ["chunk 1 text", "chunk 2 text"],
        "reference": "Load → Split → Embed → Store → Retrieve → Augment → Generate",
    },
    # ... 80건
])

result = evaluate(
    dataset=dataset,
    metrics=[
        Faithfulness(llm=judge_llm),
        ResponseRelevancy(llm=judge_llm),
        LLMContextPrecisionWithReference(llm=judge_llm),
        LLMContextRecall(llm=judge_llm),
    ],
)
print(result.to_pandas())
```

### 해석 기준
- Faithfulness >= 0.85 (production ready)
- Answer Relevancy >= 0.85
- Context Precision >= 0.8
- Context Recall >= 0.8

---

## Day 10 — LangGraph (공식 원문 기반 코드)

```python
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
# 프로덕션용: from langgraph.checkpoint.sqlite import SqliteSaver

# 1. State
class State(TypedDict):
    input: str
    result: str

# 2. Nodes
def node_a(state: State) -> dict:
    return {"result": f"Processed: {state['input']}"}

def node_b(state: State) -> dict:
    return {"result": state['result'] + " [from B]"}

def node_c(state: State) -> dict:
    return {"result": state['result'] + " [from C]"}

# 3. Routing
def route(state: State) -> Literal["node_b", "node_c"]:
    return "node_b" if len(state["input"]) > 5 else "node_c"

# 4. Build
builder = StateGraph(State)
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)
builder.add_edge(START, "node_a")
builder.add_conditional_edges(
    "node_a", route,
    {"node_b":"node_b","node_c":"node_c"}
)
builder.add_edge("node_b", END)
builder.add_edge("node_c", END)

# 5. Compile + checkpoint + interrupt (HITL)
graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["node_b", "node_c"],  # HITL: 실행 전 일시정지
)

# 6. 실행 (thread_id로 세션 구분)
config = {"configurable": {"thread_id": "user-123"}}
result = graph.invoke({"input": "hello world"}, config=config)

# HITL 재개:
#   state = graph.get_state(config)
#   graph.invoke(None, config=config)  # None = resume (새 input 아님)
```

### Streaming
```python
for event in graph.stream(input, config, stream_mode="updates"):
    for node, update in event.items():
        print(f"[{node}] {update}")
# stream_mode: values | updates | messages | debug
```

---

## Day 11 — MCP

### MCP 핵심 (공식 요약)
- **USB-C for AI** — 호스트(Claude Desktop/Code/Cursor/ChatGPT/VS Code/...)와 서버 연결 표준
- **JSON-RPC 2.0** 기반
- **4 primitives**: Tools / Resources / Prompts / Sampling
- **2 transports**: stdio (local) / Streamable HTTP (remote)

### 지원 호스트 (2026)
- Claude (Anthropic) · ChatGPT · VS Code · Cursor · MCPJam · Zed · Windsurf · 기타

### FastMCP 최소 서버
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers. Use for arithmetic."""
    return a + b

@mcp.resource("notes://{name}")
def get_note(name: str) -> str:
    """Read a note by name."""
    return open(f"notes/{name}.md").read()

@mcp.prompt()
def code_review(diff: str) -> list:
    """Review a git diff."""
    return [{"role":"user","content":f"Review this diff:\n{diff}"}]

if __name__ == "__main__":
    mcp.run()  # stdio 기본
```

### Claude Desktop 등록
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["run","python","/absolute/path/server.py"],
      "env": {"OPENAI_API_KEY":"..."}
    }
  }
}
```
Claude Desktop **완전 재시작** 필요.

### Inspector (디버깅 필수)
```bash
npx @modelcontextprotocol/inspector uv run python server.py
# → http://localhost:5173 에서 tools/list, tools/call, resources/read 테스트
```

### Anthropic MCP Connector (2026 신규)
**MCP 클라이언트 없이** Messages API가 직접 remote MCP 서버 호출:
```python
response = client.messages.create(
    model="claude-opus-4-7", max_tokens=1024,
    tools=[{
        "type": "mcp",
        "server_url": "https://my-mcp-server.com/mcp",
        "name": "my-server",
    }],
    messages=[{"role":"user","content":"..."}]
)
```

---

## Day 12 — Observability + Deploy

### Langfuse 자체 호스팅 (공식 경로)
```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up
# 2-3분 대기 ("Ready" 메시지 until langfuse-web-1)
# http://localhost:3000 → 가입 → org/project 생성 → Settings → API Keys
```

### Langfuse @observe (공식 원문 코드)
```python
from langfuse import observe, get_client, propagate_attributes

@observe()
def my_pipeline(q):
    ...

@observe(name="llm-call", as_type="generation")
async def call_llm(prompt):
    return "response"

# Nested (자동 trace hierarchy)
@observe()
def main(data):
    return my_pipeline(data)

# Tags / user_id / session_id
@observe()
def handle_request(user_id, session_id, question):
    with propagate_attributes(
        user_id=user_id,
        session_id=session_id,
        metadata={"pipeline":"rag"}
    ):
        return my_pipeline(question)

# Trace input/output 명시
@observe()
def process(q):
    answer = call_llm(q)
    langfuse = get_client()
    langfuse.set_current_trace_io(
        input={"question": q},
        output={"answer": answer}
    )
    return answer
```

### Score 부착 (Day 9 Ragas와 연결)
```python
langfuse = get_client()
langfuse.score(
    trace_id="abc123",
    name="faithfulness",
    value=0.87,  # 숫자 / boolean / categorical
    comment="Ragas evaluator=sonnet-4.6"
)
```

### Prompt Caching (Anthropic 공식 완전판)

**최소 토큰 (silent 실패 — 미만이면 캐시 안 되지만 에러 없음)**:
| 모델 | 최소 토큰 |
|---|---|
| Claude Opus 4.7/4.6/4.5 | **4,096** |
| Claude Sonnet 4.6 | **2,048** |
| Claude Sonnet 4.5/4/3.7 | **1,024** |
| Claude Haiku 4.5 | **4,096** |
| Claude Haiku 3.5 | **2,048** |

**Automatic caching (2026 신규 — 가장 간단)**:
```python
r = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},   # ← 최상위에 한 줄
    system="You are an AI assistant analyzing documents.",
    messages=[...]
)
```

**Explicit block-level**:
```python
r = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    system=[{
        "type":"text",
        "text": LONG_DOCUMENT,  # 4096+ tokens
        "cache_control":{"type":"ephemeral"}  # 5분 TTL
    }],
    messages=[...]
)
```

**1시간 TTL** (쓰기 비용 +100%, 읽기 -90% 동일):
```python
"cache_control":{"type":"ephemeral","ttl":"1h"}
# 5m + 1h 섞을 때는 1h가 먼저 와야
```

**usage 확인**:
```python
print(r.usage.cache_creation_input_tokens)  # 첫 호출: 캐시 쓰기
print(r.usage.cache_read_input_tokens)      # 재호출: 캐시 읽기 (목표)
print(r.usage.input_tokens)                 # non-cached 부분
# 총: cache_read + cache_creation + input_tokens
```

### Modal 배포 (공식 원문)
```python
# modal_app.py
import modal
from fastapi import FastAPI

app = modal.App("devlog-rag")
web_app = FastAPI()

@web_app.post("/chat")
def chat(q: dict):
    return {"answer": "..."}

image = modal.Image.debian_slim().pip_install(
    "fastapi","openai","anthropic","qdrant-client"
)

@app.function(image=image, secrets=[modal.Secret.from_name("api-keys")])
@modal.asgi_app()
def fastapi_app():
    return web_app
```

```bash
# Secret 등록
modal secret create api-keys OPENAI_API_KEY=sk-... ANTHROPIC_API_KEY=sk-ant-...

# 배포 (30초)
modal deploy modal_app.py
# → https://<workspace>--devlog-rag-fastapi-app.modal.run
```

---

## Day 13 — Fine-tuning (Unsloth)

### 설치 (2026 공식 원가)
```bash
# macOS / Linux / WSL
curl -fsSL https://unsloth.ai/install.sh | sh

# Windows PowerShell
irm https://unsloth.ai/install.ps1 | iex

# Docker
docker run --gpus all -it unsloth/unsloth
```

### LoRA SFT 기본 패턴 (일반적, 2026)
```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# 1. 4-bit quantized base 로드
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-8B-bnb-4bit",
    max_seq_length=4096,
    load_in_4bit=True,
)

# 2. LoRA adapter 추가
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],
    lora_alpha=16,
    lora_dropout=0.0,
    use_gradient_checkpointing="unsloth",
)

# 3. 데이터 (ShareGPT 포맷)
ds = load_dataset("json", data_files="data/sft.jsonl", split="train")
ds = ds.map(lambda x: {
    "text": tokenizer.apply_chat_template(x["messages"], tokenize=False)
})

# 4. Train
trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=ds,
    args=SFTConfig(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        learning_rate=2e-4,
        bf16=True, logging_steps=5,
        output_dir="outputs/sft",
    ),
)
trainer.train()

# 5. LoRA adapter만 저장
model.save_pretrained("outputs/sft/lora")
```

**지원 모델** (2026-04): `Qwen3`, `Qwen2.5`, `Llama-3.3`, `Llama-3.2`, `Llama-3.1`, `gpt-oss`, `Mistral`, `Gemma-3`, `Phi-4`, 500+ 기타
**속도 가속**: **2x faster, ~70% less VRAM** vs 표준 HF.

### DPO (Preference 학습)
```python
from trl import DPOConfig, DPOTrainer

trainer = DPOTrainer(
    model=model, tokenizer=tokenizer,
    train_dataset=dpo_ds,  # [{"prompt":..., "chosen":..., "rejected":...}]
    args=DPOConfig(
        beta=0.1,   # 너무 크면 base 능력 붕괴, 너무 작으면 학습 X
        per_device_train_batch_size=2,
        num_train_epochs=1,
        learning_rate=5e-6,
    ),
)
trainer.train()
```

### RunPod vLLM Serverless 배포
```
RunPod Console → Serverless → New Endpoint → vLLM template
Model: Qwen/Qwen3-8B-Instruct (또는 your HF-pushed tuned model)
GPU: 24GB (L4) or 48GB (L40S)
ENV:
  MAX_MODEL_LEN=8192
  DTYPE=bfloat16
  GPU_MEMORY_UTILIZATION=0.95
  CUSTOM_CHAT_TEMPLATE=  (모델별)
```

```python
# OpenAI SDK로 호출
from openai import OpenAI

client = OpenAI(
    base_url=f"https://api.runpod.ai/v2/{ENDPOINT_ID}/openai/v1",
    api_key=RUNPOD_API_KEY,
)
r = client.chat.completions.create(
    model="qwen3-8b-devlog",
    messages=[...],
)
```

Cold start 20-60s → warm worker 1개 유지하려면 `Min Workers: 1` 설정 (추가 비용).

---

## Day 14 — Mega Portfolio 체크리스트

공개 전 최종:
- [ ] `.env` 커밋 안 됨 (`git log -p | grep sk-` 으로 검증)
- [ ] API keys는 Modal Secret에 (git에 X)
- [ ] 모든 provider에 **Hard spend limit** 설정
- [ ] LICENSE MIT 명시
- [ ] Modal deploy URL 접속 가능
- [ ] MCP 서버 Claude Desktop에 연결 + 스크린샷
- [ ] Ragas faithfulness >= 0.85 스크린샷
- [ ] 데모 gif (asciinema 또는 loom, 30초)
- [ ] README 30초에 읽히는 구조

---

## 📜 논문 25편 — Figure만 보고 3줄 씩

각 논문 Claude에게 요약 프롬프트:
```
Summarize this paper in 5 bullets focusing on:
1. The problem being solved
2. The key novel technique
3. Main experimental result
4. Practical implications for LLM engineers
5. One limitation/criticism

Paper: [arxiv URL]
```

**Day별 배치**:
- D1: Attention (1706.03762) · Chinchilla (2203.15556)
- D2: RAG (2005.11401)
- D3: CoT (2201.11903) · Self-Consistency (2203.11171)
- D5: PagedAttention (2309.06180) · Matryoshka (2205.13147)
- D7: Lost in Middle (2307.03172)
- D8: RAPTOR (2401.18059) · ColBERTv2 (2112.01488) · Anthropic Contextual Retrieval (blog)
- D9: ReAct (2210.03629) · Reflexion (2303.11366) · ToT (2305.10601) · LLM-as-Judge (2306.05685)
- D11: OWASP LLM Top 10 v2.0
- D13: LoRA (2106.09685) · QLoRA (2305.14314) · DPO (2305.18290) · Constitutional AI (2212.08073)
- D14: Mixtral (2401.04088) · Medusa (2401.10774) · FlashAttention (2205.14135) · Distilling Step-by-Step (2305.02301) · Ring Attention (2310.01889)

---

## 🔗 공식 문서 직링크 (2026-04 확인됨)

| 주제 | URL |
|---|---|
| Google ML CC LLM | https://developers.google.com/machine-learning/crash-course/llm |
| Anthropic 전체 | https://platform.claude.com/docs/en/ (기존 docs.anthropic.com → redirect) |
| Anthropic Tool Use | https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/overview |
| Anthropic Prompt Caching | https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching |
| OpenAI API | https://platform.openai.com/docs |
| OpenAI Cookbook | https://developers.openai.com/cookbook (기존 cookbook.openai.com → redirect) |
| Gemini Quickstart | https://ai.google.dev/gemini-api/docs/quickstart |
| Qdrant Quickstart | https://qdrant.tech/documentation/quickstart/ |
| MCP | https://modelcontextprotocol.io/ |
| FastMCP | https://gofastmcp.com/ |
| LangGraph (신) | https://docs.langchain.com/oss/python/langgraph |
| Langfuse self-host | https://langfuse.com/self-hosting/local |
| Langfuse @observe | https://langfuse.com/docs/sdk/python/decorators |
| Ragas | https://docs.ragas.io/en/stable/ |
| HF Agents Course | https://huggingface.co/learn/agents-course |
| Unsloth | https://unsloth.ai/docs (docs.unsloth.ai → redirect) |
| RunPod Serverless vLLM | https://docs.runpod.io/serverless/vllm/get-started |
| Modal webhooks | https://modal.com/docs/guide/webhooks |
| Anthropic Contextual Retrieval | https://www.anthropic.com/news/contextual-retrieval |
| OWASP LLM Top 10 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ |

---

## 💡 이 문서 사용법

1. **Day 시작 전 10분**: 해당 Day 섹션 훑기 → 핵심 코드 패턴 뇌에 박기
2. **실습 중**: "공식 문서 가서 찾기" 전에 여기서 먼저 검색
3. **14일 후**: 실무에서도 참조 문서로 재활용

**이 문서가 공식 문서를 대체하진 않음**. 공식 문서의 **"entry point + 복붙 시작점"** 용도.

---

**최종 업데이트**: 2026-04-25 (실제 WebFetch 기반)
**다음 업데이트 권장**: 3개월마다 (주요 SDK/모델 업데이트 주기)
