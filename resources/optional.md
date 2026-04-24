# 🟡 선택 자료 (여력 있을 때)

`must-read.md` 끝낸 후. 각 영역 2-3개만 골라 읽어도 충분.

## 📼 비디오 / 코스

- [DeepLearning.AI Short Courses](https://www.deeplearning.ai/short-courses/) — Andrew Ng 1-2시간 코스들. "LangChain for LLM Apps" / "Functions, Tools and Agents" / "Building Systems with the ChatGPT API"
- [Karpathy — Let's build GPT from scratch (nanoGPT)](https://www.youtube.com/watch?v=kCc8FmEb1nY) — 2h. GPT-2를 ~100 lines로. **Week 2 이후 보상용**
- [Karpathy — State of GPT (MS Build)](https://www.youtube.com/watch?v=bZQun8Y4L2A) — OpenAI 내부자의 LLM 훈련 파이프라인 설명
- [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) — 4주 무료 코스. RAG / agents 많이 겹침 — 교차 참조용
- [Hugging Face NLP course](https://huggingface.co/learn/nlp-course) — chapter 1-2만 (transformer 감각)

## 📖 블로그 / 에세이

- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — agent 분류체계 원류
- [Simon Willison — LLM category](https://simonwillison.net/tags/llms/) — 2022~현재 실시간 업계 동향
- [Sebastian Raschka — Understanding LLMs](https://magazine.sebastianraschka.com/) — 학술 감각 + 실무 균형
- [Eugene Yan — Prompt Engineering Survey](https://eugeneyan.com/writing/prompting/) — 프롬프트 기법 카테고리화
- [Chip Huyen — Designing ML Systems 블로그](https://huyenchip.com/blog/) — MLOps + LLM production 감각
- [Jason Liu — RAG improvements](https://jxnl.co/writing/) — Instructor 저자. 실전 RAG 조언

## 📜 논문 (Figure + Abstract 수준)

### 필수 개념
- [Attention Is All You Need (Vaswani 2017)](https://arxiv.org/abs/1706.03762) — Transformer 원조. Figure 1-2
- [BERT (Devlin 2018)](https://arxiv.org/abs/1810.04805) — encoder-only
- [RAG (Lewis 2020)](https://arxiv.org/abs/2005.11401) — RAG 용어 원조
- [Chain-of-Thought (Wei 2022)](https://arxiv.org/abs/2201.11903) — Figure 1
- [Self-Consistency (Wang 2022)](https://arxiv.org/abs/2203.11171) — N-sampling + 다수결
- [ReAct (Yao 2022)](https://arxiv.org/abs/2210.03629) — agent 원형
- [Lost in the Middle (Liu 2023)](https://arxiv.org/abs/2307.03172) — 긴 context 중간 무시

### 2024-2026 중요
- [Reflexion (Shinn 2023)](https://arxiv.org/abs/2303.11366) — self-reflection agent
- [Tree of Thoughts (Yao 2023)](https://arxiv.org/abs/2305.10601) — tree search reasoning
- [RAPTOR (Sarthi 2024)](https://arxiv.org/abs/2401.18059) — recursive abstraction tree
- [Self-RAG (Asai 2023)](https://arxiv.org/abs/2310.11511) — adaptive retrieval
- [CRAG (Yan 2024)](https://arxiv.org/abs/2401.15884) — corrective RAG with web fallback
- [Judging LLM-as-a-Judge (Zheng 2023)](https://arxiv.org/abs/2306.05685) — judge bias 실측
- [PagedAttention (Kwon 2023)](https://arxiv.org/abs/2309.06180) — vLLM 핵심
- [The Prompt Report (Schulhoff 2024)](https://arxiv.org/abs/2406.06608) — 58 기법 survey

## 🛠 프레임워크 대안

- [LiteLLM](https://docs.litellm.ai/docs/) — provider 통합 (자체 추상화 대신)
- [aisuite (Andrew Ng)](https://github.com/andrewyng/aisuite) — 얇은 provider 추상화
- [Haystack](https://docs.haystack.deepset.ai/docs/) — deepset의 RAG/agent 프레임
- [DSPy](https://dspy.ai/) — 선언적 프롬프트 프로그래밍. 복잡 pipeline
- [LangFlow](https://docs.langflow.org/) — 노코드 LLM 앱 빌더

## 🗂 Vector DB 대안

- [Weaviate](https://docs.weaviate.io/weaviate) — 그래프 + 벡터
- [Pinecone](https://docs.pinecone.io/) — 완전 관리형
- [Chroma](https://docs.trychroma.com/) — 임베디드, 가장 심플
- [FAISS](https://faiss.ai/) — 라이브러리 수준
- [pgvector](https://github.com/pgvector/pgvector) — Postgres 통합
- [LanceDB](https://lancedb.github.io/lancedb/) — embedded serverless

## 🔬 Advanced RAG

- [Anthropic — Contextual Retrieval cookbook](https://github.com/anthropics/anthropic-cookbook) — 실제 구현 예시
- [LlamaIndex — Qdrant hybrid](https://docs.llamaindex.ai/en/stable/examples/vector_stores/qdrant_hybrid/)
- [Weaviate — Hybrid alpha 튜닝](https://weaviate.io/developers/weaviate/search/hybrid)
- [ColBERT repo](https://github.com/stanford-futuredata/ColBERT) — late interaction 원본
- [BGE-M3 paper](https://arxiv.org/abs/2402.03216) — dense+sparse+colbert 단일 모델
- [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147) — text-embedding-3이 채택한 이유

## 🔭 Observability / Eval 대안

- [LangSmith](https://docs.smith.langchain.com/) — LangChain 순정 (SaaS)
- [Helicone](https://docs.helicone.ai/) — Gateway proxy 방식
- [DeepEval](https://docs.confident-ai.com/docs/getting-started) — pytest 스타일
- [Braintrust](https://www.braintrust.dev/docs) — Eval SaaS, ladder 비교 UI
- [Trulens](https://www.trulens.org/) — Ragas 대안/보완
- [OpenLLMetry](https://github.com/traceloop/openllmetry) — OTel 표준 LLM spans
- [OpenAI Evals repo](https://github.com/openai/evals) — maintenance mode이지만 레퍼런스

## 🖥 Local LLM 확장

- [llama.cpp](https://github.com/ggml-org/llama.cpp) — GGUF 원가
- [llama-cpp-python](https://llama-cpp-python.readthedocs.io/en/latest/server/) — Python server
- [MLX (Apple)](https://github.com/ml-explore/mlx) — Apple Silicon native
- [HF TGI](https://huggingface.co/docs/text-generation-inference/index) — vLLM 경쟁
- [Unsloth](https://docs.unsloth.ai/) — 4-bit 최적화 + fine-tuning
- [LM Studio](https://lmstudio.ai/) — GUI 앱
- [Outlines](https://dottxt-ai.github.io/outlines/) — grammar-constrained decoding

## 🔒 Security / Guardrails (Day 14+)

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Anthropic — Guardrails](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/overview)
- [Guardrails AI](https://www.guardrailsai.com/docs)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [Llama Prompt Guard 2](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M)
- [LlamaFirewall](https://github.com/facebookresearch/llamafirewall)

## 🧪 MCP 서버 예시 읽기

- [mcp/servers — filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) — 파일 R/W
- [mcp/servers — fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) — HTTP GET
- [mcp/servers — github](https://github.com/modelcontextprotocol/servers/tree/main/src/github) — GH API
- [mcp/servers — memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) — 대화 메모리
- [Block's MCP servers](https://github.com/block/mcp-servers) — 고급 구현체 모음

## 📦 프로덕션 배포

- [FastAPI — SSE streaming](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- [Modal](https://modal.com/docs) — serverless Python (LLM 앱 배포 쉬움)
- [Fly.io](https://fly.io/docs/) — Docker 배포 간단
- [Docker multi-stage builds for Python](https://docs.docker.com/language/python/containerize/)

## 🎨 UI / Demo

- [Streamlit](https://docs.streamlit.io/) — 빠른 demo
- [Gradio](https://www.gradio.app/docs) — HF 공식 UI
- [Chainlit](https://docs.chainlit.io/) — Chat UI 특화
- [asciinema](https://asciinema.org/) — 터미널 녹화 (README demo용)

## 📅 한국어 보조 (막힐 때만, 공식 문서가 1순위)

- [Google ML Crash Course LLM — 한국어](https://developers.google.com/machine-learning/crash-course/llm/transformers?hl=ko)
- [LangChain Korea 커뮤니티](https://github.com/LangChain-Kr)
- 한국어 검색 키워드: "LangGraph 한국어 튜토리얼" / "vLLM RunPod 한국어" / "Langfuse 설치 한국어"
