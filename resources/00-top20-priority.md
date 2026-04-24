# Top 20 최우선 자료 (2026-04 갱신)

시간 없으면 이것만. 14일 플랜의 뼈대. 각 링크에 **한 줄 요약** 포함.

## 🔴 필수 20개

| # | 링크 | Day | 소요 | 🧠 TL;DR |
|---|---|---|---|---|
| 1 | [Google ML Crash Course — LLM](https://developers.google.com/machine-learning/crash-course/llm) | Day 1 | 2h | LLM 작동 원리 — n-gram → RNN → Transformer 진화, pretraining/fine-tuning/prompt 구분. **한국어 버전 있음** |
| 2 | [Anthropic Courses repo](https://github.com/anthropics/courses) | Day 2-5 | 6h | Anthropic 공식 실습 과정. `anthropic_api_fundamentals` (Day 2) + `prompt_engineering` + `tool_use` (Day 5) 6강 필수 |
| 3 | [Anthropic Interactive Prompt Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) | Day 3 | 4h | **Day 3 메인**. 9챕터 + appendix. XML 태그 / prefill / CoT / few-shot 전부 |
| 4 | [OpenAI Cookbook](https://cookbook.openai.com/) | Day 2-14 | 참조 | 실전 예제 150+. rate_limits / logprobs / responses_api / structured / embeddings / evals — 매 Day 1-2개씩 참조 |
| 5 | [OpenAI — Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | Day 4 | 1h | `strict: true`로 JSON Schema 100% 준수 보장. Pydantic 직접 전달 지원 |
| 6 | [OpenAI — Function calling](https://platform.openai.com/docs/guides/function-calling) | Day 5 | 1h | Responses API 기준. strict arguments, parallel tool calls, tool_choice 3모드 |
| 7 | [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) | Day 5 | 0.5h | `tools=[...]` + `tool_use`/`tool_result` 블록 구조. description 긴 게 정확도의 70% |
| 8 | [Anthropic — Structured Outputs](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs) | Day 4 | 1h | 2026-초 native response_format 지원. legacy tool_use 트릭도 있음 |
| 9 | [Gemini API docs](https://ai.google.dev/gemini-api/docs) | Day 2 | 1h | `google-genai` SDK. Content/Part 구조, system_instruction, thinking_budget. 무료 tier 있음 |
| 10 | [LangChain RAG From Scratch](https://github.com/langchain-ai/rag-from-scratch) | Day 7-8 | 5h | Lance Martin의 14 notebook 시리즈. Part 1-4 (Day 7) + Part 5-14 (Day 8) |
| 11 | [RAG From Scratch YouTube](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x) | Day 7-8 | 3h | 위 repo의 영상 버전. 1.5배속 권장 |
| 12 | [LlamaIndex — Understanding RAG](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) | Day 7 | 1.5h | Node/Index/Retriever/QueryEngine 추상화. LangChain과 다른 접근. 코드 30-80줄에 RAG 완성 |
| 13 | [Qdrant Quickstart + Hybrid queries](https://qdrant.tech/documentation/quickstart/) | Day 6-8 | 2h | 로컬 Docker 1분. Hybrid (dense+sparse+RRF) 2024 버전에서 native 지원 |
| 14 | [Ragas docs](https://docs.ragas.io/en/stable/) | Day 9 | 2h | **Day 9 메인**. Faithfulness / ResponseRelevancy / LLMContextPrecision / LLMContextRecall. v0.2 API |
| 15 | [OpenAI Cookbook — Evals topic](https://cookbook.openai.com/topic/evals) | Day 9 | 2h | OpenAI Evals 프레임 + RAG eval w/ LlamaIndex + eval driven 개선 사례 |
| 16 | [HF Agents Course](https://huggingface.co/learn/agents-course) | Day 10 | 4h | Unit 0-2. smolagents / LangGraph / LlamaIndex 프레임워크 비교. Colab 실습 포함 |
| 17 | [LangGraph docs](https://langchain-ai.github.io/langgraph/) | Day 10 | 2h | StateGraph / conditional_edges / checkpoint / HITL. Production agent 표준 |
| 18 | [modelcontextprotocol.io](https://modelcontextprotocol.io/) | Day 11 | 1.5h | 2024-11 Anthropic 오픈 표준. 4 primitives (Tools/Resources/Prompts/Sampling). Python SDK + FastMCP |
| 19 | [Langfuse docs](https://langfuse.com/docs) | Day 12 | 2h | Self-host 3분 (docker-compose). Trace / Score / Prompt versioning / Cost dashboard |
| 20 | [RunPod Serverless vLLM](https://docs.runpod.io/serverless/vllm/get-started) | Day 13 | 1h | worker-vllm template으로 Qwen3/Llama 엔드포인트 1시간 내 배포. OpenAI-compat URL 제공 |

## 🎬 사전 준비 (Day 1 시작 전)

- [ ] OpenAI API 키 + $5 충전 → [`setup/3-accounts-checklist.md`](../setup/3-accounts-checklist.md)
- [ ] Anthropic API 키 + $5 충전
- [ ] Google AI Studio 무료 키
- [ ] Python 3.11+ + uv 설치
- [ ] Docker Desktop 실행 확인
- [ ] Claude Desktop 설치 (Day 11 MCP용)
- [ ] RunPod 계정 (Day 13, 카드 등록)
- [ ] GitHub 빈 repo 생성 (`devlog-rag-copilot` 등)

상세: [`curriculum/day00-prep.md`](../curriculum/day00-prep.md)

## 💰 비용 예상 (2주)

| 항목 | 최저 | 현실 |
|---|---|---|
| OpenAI (+Structured/Eval) | $8 | $15 |
| Anthropic (+Tool/Caching) | $8 | $15 |
| Gemini | $0 | $0 |
| RunPod (Day 13만) | $5 | $10 |
| **합계** | **$21** | **$40** |

Prompt caching 적극 적용 시 Anthropic 비용 50%+ 절감.

## ⏱ 시간 분포 (필수 자료만)

- 읽기: ~25h
- 튜토리얼 따라치기: ~15h
- 본 실습 + 변형: ~55h
- 정리/회고: ~15h
- 합계 ~110h (14일 × 8h 평균, 휴식 제외)

## 🏆 "이 20개만 제대로 하면"

- 14일 끝에 Ragas faithfulness 0.85+ RAG 앱 완성
- LangGraph agent + MCP 서버 + Langfuse trace 통합
- Multi-provider (OpenAI/Anthropic/Ollama/RunPod) 스위치
- GitHub 공개 가능한 포트폴리오

## 🔗 더 많은 자료

- [`must-read.md`](must-read.md) — 핵심 링크 전체
- [`optional.md`](optional.md) — 여력 있을 때
- [`later.md`](later.md) — 14일 이후
- [`skip.md`](skip.md) — 중복/비효율
- [`links-classified.md`](links-classified.md) — 모든 URL + 분류
