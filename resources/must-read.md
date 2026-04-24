# 🔴 필수 자료 (2026-04 기준)

`links-classified.md`에서 🔴만 추린 **핵심 체크리스트**. 2주 안에 반드시 소화. 각 링크에 한 줄 요약.

## 🔬 Foundation (Day 1)

- [ ] [Google ML Crash Course — LLM](https://developers.google.com/machine-learning/crash-course/llm) — LLM 개념 정립. 한국어 버전 있음 (2h)
- [ ] [Google ML Crash Course — Transformers](https://developers.google.com/machine-learning/crash-course/llm/transformers) — Self-attention의 QKV 직관. 수식 없이 시작 (1h)
- [ ] [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — 교과서급 시각화 (0.5h)
- [ ] [3Blue1Brown — "But what is a GPT?"](https://www.youtube.com/watch?v=wjZofJX0v4M) — 27분 비디오 (0.5h)
- [ ] [Karpathy — Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) — 처음 30분만. BPE가 왜 이 모양인지 (0.5h)

## 🔌 APIs — 3사 (Day 2)

### OpenAI
- [ ] [Platform docs](https://platform.openai.com/docs) — 전체 reference hub
- [ ] [API Reference](https://platform.openai.com/docs/api-reference) — Chat Completions + Responses API
- [ ] [Responses API 마이그레이션 가이드](https://platform.openai.com/docs/guides/migrate-to-responses) — 신규 코드는 Responses 권장
- [ ] [Cookbook](https://cookbook.openai.com/) — 150+ 실전 예제

### Anthropic
- [ ] [Build with Claude](https://docs.anthropic.com/en/docs/build-with-claude/overview) — messages API + top-level system
- [ ] [API Reference](https://docs.anthropic.com/en/api/getting-started) — client SDK 실전
- [ ] [Courses (repo)](https://github.com/anthropics/courses) — api_fundamentals + prompt + tool_use 3코스

### Gemini
- [ ] [Gemini API Docs](https://ai.google.dev/gemini-api/docs) — 전체
- [ ] [Quickstart](https://ai.google.dev/gemini-api/docs/quickstart) — google-genai SDK
- [ ] [Text generation](https://ai.google.dev/gemini-api/docs/text-generation) — Content/Part 구조
- [ ] [Models](https://ai.google.dev/gemini-api/docs/models) — 2.5-pro / 2.5-flash / 2.5-flash-lite (2026-04)

## 🧠 Prompt Engineering (Day 3)

- [ ] [Anthropic — Prompt Eng Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 공식 권장
- [ ] [Interactive Prompt Tutorial (GitHub)](https://github.com/anthropics/prompt-eng-interactive-tutorial) ⭐ — 9챕터 + appendix
- [ ] [Prompting Guide — Techniques](https://www.promptingguide.ai/techniques) — 학계/업계 기법 survey
- [ ] [OpenAI — Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering) — 6가지 전략
- [ ] [Anthropic — Prompt Injection](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) — 공격 4유형 + 방어 원칙
- [ ] [Lilian Weng — Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — OpenAI 전 VP 정리

## 📋 Structured Output (Day 4)

- [ ] [OpenAI — Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) — strict=true 100% 보장
- [ ] [Anthropic — Structured Outputs](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs) — native response_format (2026-초)
- [ ] [Gemini — Structured Output](https://ai.google.dev/gemini-api/docs/structured-output) — response_schema=PydanticModel
- [ ] [Pydantic v2 docs](https://docs.pydantic.dev/latest/) — BaseModel / Field / validators / TypeAdapter
- [ ] [Instructor](https://python.useinstructor.com/) — Pydantic + 3사 + retry + Partial streaming

## 🛠 Tool Use (Day 5)

- [ ] [OpenAI — Function calling](https://platform.openai.com/docs/guides/function-calling) — Responses API 기준
- [ ] [OpenAI Cookbook — Responses API tool orchestration](https://cookbook.openai.com/examples/responses_api/responses_api_tool_orchestration) — builtin + custom mix
- [ ] [Anthropic — Tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) + [Best practices](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview#tool-use-best-practices)
- [ ] [Anthropic Courses — tool_use](https://github.com/anthropics/courses/tree/master/tool_use) ⭐ — 6 notebook
- [ ] [Anthropic — Extended thinking + tool use](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#extended-thinking-with-tool-use) — 4.x 이후
- [ ] [Gemini — Function calling](https://ai.google.dev/gemini-api/docs/function-calling) — Automatic FC

## 🔡 Embeddings / Vector DB (Day 6)

- [ ] [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) — 3-small/3-large, Matryoshka dimensions
- [ ] [Gemini Embeddings](https://ai.google.dev/gemini-api/docs/embeddings) — task_type 파라미터 (query vs document)
- [ ] [Voyage AI](https://docs.voyageai.com/) — Anthropic 권장 (voyage-3-large MTEB 상위)
- [ ] [SBERT](https://www.sbert.net/) — 로컬 embedding (all-MiniLM / multilingual-e5 / BGE-M3)
- [ ] [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) — 필터(Retrieval / Korean) 필수
- [ ] [Qdrant Quickstart](https://qdrant.tech/documentation/quickstart/)
- [ ] [Qdrant — HNSW indexing](https://qdrant.tech/documentation/concepts/indexing/) — m/ef_construct/ef 튜닝
- [ ] [Qdrant — Quantization](https://qdrant.tech/documentation/guides/quantization/) — scalar int8 / binary

## 🏛 기본 RAG (Day 7)

- [ ] [RAG From Scratch repo](https://github.com/langchain-ai/rag-from-scratch) ⭐ — 14 notebook. Part 1-4 Day 7에
- [ ] [LangChain RAG tutorials](https://python.langchain.com/docs/tutorials/rag/) — LCEL pipe 문법
- [ ] [LlamaIndex — Understanding RAG](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) — Node/Index/QueryEngine
- [ ] [OpenAI Cookbook — QA using embeddings](https://cookbook.openai.com/examples/question_answering_using_embeddings) — 프레임워크 없이 직접

## 🚀 고급 RAG (Day 8)

- [ ] RAG From Scratch — Part 5-14 (Multi-query / RAG-Fusion / HyDE / Routing / RAPTOR / ColBERT)
- [ ] [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — 49% 개선 (2024-09)
- [ ] [OpenAI Cookbook — Search reranking with cross-encoders](https://cookbook.openai.com/examples/search_reranking_with_cross-encoders)
- [ ] [SBERT — Cross-Encoders](https://www.sbert.net/examples/applications/cross-encoder/README.html)
- [ ] [Qdrant — Hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/) — dense+sparse+RRF native
- [ ] [Cohere Rerank](https://docs.cohere.com/docs/rerank) — rerank-multilingual-v3.0 한국어 우수
- [ ] [RAPTOR paper](https://arxiv.org/abs/2401.18059) — Figure만

## 📊 Eval (Day 9)

- [ ] [Ragas docs](https://docs.ragas.io/en/stable/) ⭐ — faithfulness/answer_relevancy/context_precision/context_recall
- [ ] [Ragas — Synthetic Test Data](https://docs.ragas.io/en/stable/concepts/test_data_generation/) — TestsetGenerator
- [ ] [OpenAI Cookbook — Evals topic](https://cookbook.openai.com/topic/evals)
- [ ] [Evaluate RAG with LlamaIndex + Ragas](https://cookbook.openai.com/examples/evaluation/evaluate_rag_with_llamaindex) — end-to-end
- [ ] [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) — Table 3 positional bias 실측
- [ ] [Jason Liu — RAG Improvement Loop](https://jxnl.co/writing/2024/08/19/rag-flywheel/) — 실무 인사이트

## 🤖 Agents (Day 10)

- [ ] [HF Agents Course](https://huggingface.co/learn/agents-course) ⭐ — Unit 0-2
- [ ] [HF Agents — smolagents retrieval](https://huggingface.co/learn/agents-course/unit2/smolagents/retrieval_agents)
- [ ] [LangGraph docs](https://langchain-ai.github.io/langgraph/) — StateGraph / conditional / HITL
- [ ] [LangGraph — Persistence](https://langchain-ai.github.io/langgraph/how-tos/persistence/) — SqliteSaver
- [ ] [LangGraph — Human-in-the-loop](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/) — interrupt_before
- [ ] [Pydantic AI](https://ai.pydantic.dev/) — 대안 프레임워크, 타입 안전
- [ ] [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) ⭐ — Agent vs Workflow 구분
- [ ] [ReAct paper](https://arxiv.org/abs/2210.03629) — Figure 1만

## 🔌 MCP (Day 11)

- [ ] [modelcontextprotocol.io](https://modelcontextprotocol.io/) — 4 primitives
- [ ] [Python SDK](https://github.com/modelcontextprotocol/python-sdk) — FastMCP 고수준
- [ ] [Anthropic MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) — Claude Desktop 설정
- [ ] [Reference servers](https://github.com/modelcontextprotocol/servers) — filesystem / fetch / github / memory
- [ ] [Specification](https://spec.modelcontextprotocol.io/) — JSON-RPC 2.0
- [ ] [FastMCP](https://gofastmcp.com/) — Jeremy Howard 팀
- [ ] [MCP Inspector](https://github.com/modelcontextprotocol/inspector) — 디버깅 필수

## 🔭 Observability (Day 12)

- [ ] [Langfuse docs](https://langfuse.com/docs) ⭐ — Self-host 3분
- [ ] [Langfuse tracing](https://langfuse.com/docs/tracing) — @observe decorator
- [ ] [Langfuse prompt management](https://langfuse.com/docs/prompt-management/overview) — UI에서 hot swap
- [ ] [Langfuse scores](https://langfuse.com/docs/scores/overview) — Ragas attach
- [ ] [Arize Phoenix](https://docs.arize.com/phoenix) — OSS 대안
- [ ] [OpenTelemetry GenAI conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)

## ⚡ Production (Day 12)

- [ ] [OpenAI — Rate limits](https://platform.openai.com/docs/guides/rate-limits)
- [ ] [OpenAI Cookbook — Handle rate limits](https://cookbook.openai.com/examples/how_to_handle_rate_limits) — tenacity 표준
- [ ] [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) — implicit
- [ ] [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — explicit cache_control
- [ ] [Anthropic — Streaming](https://docs.anthropic.com/en/docs/build-with-claude/streaming)
- [ ] [Gemini — Context caching](https://ai.google.dev/gemini-api/docs/caching) — 32k+ 최소
- [ ] [Batch API (OpenAI)](https://platform.openai.com/docs/guides/batch) — 50% 할인 24h SLA
- [ ] [Anthropic Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing)

## 🖥 Local LLM + RunPod (Day 13)

### Local
- [ ] [Ollama](https://ollama.com/) — brew install --cask ollama
- [ ] [Ollama docs](https://docs.ollama.com/)
- [ ] [Ollama — OpenAI compatibility](https://docs.ollama.com/openai) — SDK 그대로
- [ ] [Ollama Model Library](https://ollama.com/library) — qwen3 / llama3.3 / gpt-oss / gemma3
- [ ] [vLLM docs](https://docs.vllm.ai/)
- [ ] [vLLM OpenAI server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)

### Cloud (RunPod)
- [ ] [RunPod docs](https://docs.runpod.io/)
- [ ] [Serverless Overview](https://docs.runpod.io/serverless/overview)
- [ ] [Serverless vLLM — Get started](https://docs.runpod.io/serverless/vllm/get-started) ⭐
- [ ] [Serverless vLLM — Config](https://docs.runpod.io/serverless/vllm/configuration)
- [ ] [vLLM on RunPod](https://docs.vllm.ai/en/latest/deployment/frameworks/runpod/)
- [ ] [worker-vllm repo](https://github.com/runpod-workers/worker-vllm)

### Leaderboards
- [ ] [Open LLM Leaderboard v2](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)
- [ ] [Chatbot Arena](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard)
- [ ] [MTEB](https://huggingface.co/spaces/mteb/leaderboard)

---

## 📌 읽기 순서 권장

1. Day 1 전: 1-5 (Foundation)
2. Day 2: 6-9 (OpenAI + Anthropic + Gemini 3사)
3. Day 3: 10-13 + Interactive Tutorial notebook 실행
4. Day 4: 14-17 (Structured)
5. Day 5: 18-22 (Tool Use, Anthropic Courses 6강)
6. Day 6: 23-29 (Embedding)
7. Day 7-8: RAG From Scratch + LlamaIndex + Qdrant
8. Day 9: Ragas + Evals cookbook
9. Day 10: HF Agents + LangGraph + 에세이
10. Day 11: MCP 공식 문서 + SDK
11. Day 12: Langfuse + Caching + Rate limits
12. Day 13: Ollama + RunPod + Leaderboards
13. Day 14: 재활용 + README 작성

## 🎯 진척 점검

체크박스 빈 게 10+ 남으면 재방문. 다 체크되면 `optional.md`로.
