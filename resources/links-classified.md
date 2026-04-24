# 전체 링크 분류 + 요약 (단일 진실 소스)

사용자가 제공한 모든 링크 + 내가 추가한 필수 확장 링크. **어떤 것도 빼지 않음**.
분류: 🔴 필수 / 🟡 선택 / 🟢 나중에 / ⚪ 스킵/중복

각 항목:
- 🔖 링크
- 💬 한 줄 요약 (WebFetch 직접 확인 or 공식 설명 기반)
- 📅 언제 볼지 (Day 번호)
- ⏱ 예상 소요
- 🛠 실습 여부

---

## 0. 메인 코스

### LLM Zoomcamp
- 🔴 **[LLM Zoomcamp — datatalks.club](https://datatalks.club/courses/llm-zoomcamp/)**
  - 💬 DataTalks.Club의 10주짜리 무료 LLM 엔지니어링 코스. RAG, vector search, eval, monitoring, agent까지. 73k+ 커뮤니티. 우리 2주 플랜의 교차 참조용.
  - 📅 Day 7-9 교차 참조 / ⏱ 전체 20h+ / 🛠 ✔
- 🔴 **[LLM Zoomcamp — GitHub](https://github.com/DataTalksClub/llm-zoomcamp)**
  - 💬 위 코스의 전체 커리큘럼, notebook, homework가 담긴 레포. 공식 페이지보다 여기가 더 실용적.
  - 📅 Day 7-9 / ⏱ 참조 / 🛠 ✔
- 🟡 **[LLM Zoomcamp — YouTube Playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIoBpuc900htYF4uhEAbaT-)**
  - 💬 강의 영상 전체. 배속으로 필요 부분만.
  - 📅 필요시 / ⏱ 영상 20h+ / 🛠 —

### Hugging Face Agents Course
- 🔴 **[HF Agents Course (learn)](https://huggingface.co/learn/agents-course)**
  - 💬 무료 5-unit 코스. Unit 0 온보딩, Unit 1 에이전트 기초(Tools/Thoughts/Actions/Observations), Unit 2 프레임워크(smolagents, LangGraph, LlamaIndex), Unit 3 유스케이스, Unit 4 최종 과제. Bonus로 Fine-tuning for function calling, Observability, Pokemon agent.
  - 📅 Day 10 / ⏱ 4h (핵심) / 🛠 ✔ 퀴즈 + 과제
- 🔴 **[HF Agents Course — GitHub](https://github.com/huggingface/agents-course)**
  - 💬 위 코스의 소스. 이슈/PR 가능.
  - 📅 Day 10 / ⏱ 참조 / 🛠 ✔
- 🟡 **[HF Agents Course — Org](https://huggingface.co/agents-course)**
  - 💬 HF org 페이지. Spaces/datasets 모음.
  - 📅 Day 10 / ⏱ 참조
- 🔴 **[HF Agents — unit0 intro](https://huggingface.co/learn/agents-course/unit0/introduction)**
  - 💬 코스 네비게이션 시작점.
  - 📅 Day 10 / ⏱ 10m
- 🔴 **[HF Agents — smolagents retrieval agents](https://huggingface.co/learn/agents-course/unit2/smolagents/retrieval_agents)**
  - 💬 smolagents로 agentic RAG 구현. Day 10 실습 소스.
  - 📅 Day 10 / ⏱ 1h / 🛠 ✔

### Google ML Crash Course
- 🔴 **[Google ML Crash Course — LLM](https://developers.google.com/machine-learning/crash-course/llm)**
  - 💬 45분 공식 입문 모듈. Token, N-gram, RNN → Transformer, fine-tuning, distillation, LLM 문제점. Day 1의 메인 이론.
  - 📅 Day 1 / ⏱ 2h / 🛠 —
- 🔴 **[Google ML Crash Course — Transformers](https://developers.google.com/machine-learning/crash-course/llm/transformers)**
  - 💬 Transformer만 별도 페이지. Self-attention을 개발자 시각으로 설명.
  - 📅 Day 1 / ⏱ 1h / 🛠 —
- 🟡 **[Google ML Crash Course — 전체 홈](https://developers.google.com/machine-learning/crash-course)**
  - 💬 전체 ML 기초. LLM 모듈 이외는 우리 목적 밖.
  - 📅 나중에 / ⏱ — / 🛠 —

---

## 1. API / 공식 문서

### OpenAI
- 🔴 **[OpenAI Platform Docs](https://platform.openai.com/docs)**
  - 💬 OpenAI 공식 문서 허브. 모델/가이드/API 레퍼런스.
  - 📅 Day 2, 상시 참조 / ⏱ 1h / 🛠 —
- 🔴 **[OpenAI API Reference](https://platform.openai.com/docs/api-reference)**
  - 💬 각 엔드포인트 스펙. 실습 때 상시.
  - 📅 상시 / ⏱ 참조
- 🔴 **[OpenAI Cookbook (developers.openai.com)](https://developers.openai.com/cookbook)**
  - 💬 실전 노트북 허브. 카테고리: Agents, Evals, Multimodal, Text, Guardrails, Optimization, ChatGPT.
  - 📅 Day 2-14 상시 / ⏱ 매일 30m / 🛠 ✔
- ⚪ **[openai-cookbook (GitHub)](https://github.com/openai/openai-cookbook)**
  - 💬 위와 동일한 내용의 GitHub 레포. developers.openai.com이 렌더링된 버전이라 중복.
  - 📅 — / ⏱ —

### Anthropic
- 🔴 **[Anthropic Docs](https://docs.anthropic.com/)**
  - 💬 공식 문서 허브. (주: 현재 `platform.claude.com`으로 리다이렉트됨.)
  - 📅 Day 2, 상시 / ⏱ 1h
- 🔴 **[Anthropic — Build with Claude](https://www.anthropic.com/learn/build-with-claude)**
  - 💬 Anthropic 학습 랜딩. 가이드/튜토리얼 모음.
  - 📅 Day 2 / ⏱ 1h
- 🔴 **[Anthropic courses (GitHub)](https://github.com/anthropics/courses)**
  - 💬 5개 코스: (1) API Fundamentals (API 키, params, 멀티모달, streaming) (2) Prompt Engineering Interactive Tutorial (3) Real-world prompting (4) Prompt evaluations (5) Tool use. 비용 절감 위해 Haiku 사용.
  - 📅 Day 2-9 / ⏱ 10h+ / 🛠 ✔ 전부
- 🔴 **[Anthropic — Prompt Eng Interactive Tutorial (GitHub)](https://github.com/anthropics/prompt-eng-interactive-tutorial)**
  - 💬 9챕터 + 연습 문제. **Day 3의 메인 자료**.
  - 📅 Day 3 / ⏱ 4h / 🛠 ✔
- 🔴 **[Anthropic courses — anthropic_api_fundamentals](https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals)**
  - 💬 위 (1)의 하위 경로.
  - 📅 Day 2 / ⏱ 2h / 🛠 ✔
- ⚪ **[Anthropic courses — prompt_engineering_interactive_tutorial](https://github.com/anthropics/courses/tree/master/prompt_engineering_interactive_tutorial)**
  - 💬 위 "prompt-eng-interactive-tutorial" 레포가 최신/독립 버전. 이 하위 경로는 참고만.

### Gemini
- 🔴 **[Gemini API Docs](https://ai.google.dev/gemini-api/docs)**
  - 💬 Text, image/video gen, document (1000p PDF), function calling, long context (M tokens), structured output, Live API, built-in tools (Google Search, Maps, Code Exec, Computer Use). Python SDK: `from google import genai`.
  - 📅 Day 2 / ⏱ 1h / 🛠 ✔
- 🔴 **[Gemini — Quickstart](https://ai.google.dev/gemini-api/docs/quickstart)**
  - 💬 첫 호출 30분 안에.
  - 📅 Day 2 / ⏱ 30m / 🛠 ✔
- 🔴 **[Gemini — Models](https://ai.google.dev/gemini-api/docs/models)**
  - 💬 Pro/Flash/Nano 선택 기준.
  - 📅 Day 2 / ⏱ 15m
- 🔴 **[Gemini — Text generation](https://ai.google.dev/gemini-api/docs/text-generation)**
  - 💬 기본 generate_content API.
  - 📅 Day 2 / ⏱ 30m / 🛠 ✔

---

## 2. Prompt Engineering

- 🔴 **[OpenAI Cookbook — 홈](https://developers.openai.com/cookbook)** (중복, 0/1 섹션 참조)
- 🔴 **[cookbook.openai.com](https://cookbook.openai.com/)**
  - 💬 위와 동일 컨텐츠의 예전 도메인. 일부 구 레퍼런스.
  - 📅 참조 / ⏱ —
- 🔴 **[Anthropic — Prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)**
  - 💬 Prompt 엔지니어링 전, 성공 기준/평가 먼저 정의하라고 강조. 구체 기법은 "Claude prompting best practices"에 통합됨. Interactive tutorial 링크 제공.
  - 📅 Day 3 / ⏱ 30m
- 🔴 **[Anthropic — Prompt Eng Interactive Tutorial (GitHub)](https://github.com/anthropics/prompt-eng-interactive-tutorial)** (중복)
- ⚪ **[Anthropic courses — prompt_engineering_interactive_tutorial](https://github.com/anthropics/courses/tree/master/prompt_engineering_interactive_tutorial)** (중복)
- 🟡 **[apeit.github.io](https://idsulik.github.io/apeit/)**
  - 💬 위 Anthropic 튜토리얼의 비공식 웹 뷰. 노트북 대신 브라우저로 보고 싶을 때.
  - 📅 Day 3 / ⏱ 참조
- 🔴 **[Prompting Guide — 홈](https://www.promptingguide.ai/)**
  - 💬 영문 커뮤니티 가이드. 기법 백과.
  - 📅 Day 3 / ⏱ 1h
- 🔴 **[Prompting Guide — techniques](https://www.promptingguide.ai/techniques)**
  - 💬 18가지 기법 정리: Zero/Few-shot, CoT, Multimodal CoT, Meta, Self-Consistency, Generate Knowledge, Prompt Chaining, ToT, RAG, ART, APE, Active-Prompt, Directional Stimulus, PAL, ReAct, Reflexion, Graph Prompting.
  - 📅 Day 3 / ⏱ 1h
- 🟡 **[Prompting Guide — applications](https://www.promptingguide.ai/applications)**
  - 💬 도메인별 응용. 2주차 이후 선택.
  - 📅 나중에 / ⏱ —
- 🔴 **[DeepLearning.AI — Courses](https://www.deeplearning.ai/courses/)**
  - 💬 Andrew Ng 강의 카탈로그.
  - 📅 참조 / ⏱ —
- 🔴 **[DeepLearning.AI — Short Courses](https://www.deeplearning.ai/short-courses/)**
  - 💬 무료 1-2시간짜리 short course 수십 개. LangChain/Prompt/RAG/Agents 입문 최고.
  - 📅 나중에 / ⏱ 코스당 1-2h / 🛠 ✔

---

## 3. Structured Output / JSON

- 🔴 **[OpenAI — Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)**
  - 💬 JSON Schema strict mode. 최신 모델 전부 지원. JSON mode와 다름 (이 쪽이 훨씬 정확).
  - 📅 Day 4 / ⏱ 1h / 🛠 ✔
- 🔴 **[OpenAI Cookbook](https://developers.openai.com/cookbook)** (중복)
- ⚪ **[openai-cookbook GitHub](https://github.com/openai/openai-cookbook)** (중복)
- 🔴 **[Anthropic — Structured Outputs](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs)**
  - 💬 Claude native structured output + tool_use로 강제 JSON 추출 트릭.
  - 📅 Day 4 / ⏱ 1h / 🛠 ✔
- ⚪ **[Claude platform — Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)**
  - 💬 위의 리다이렉트 대상. 동일 내용.
- 🔴 **[Gemini — Structured Output](https://ai.google.dev/gemini-api/docs/structured-output)**
  - 💬 `response_schema`로 Pydantic/TypedDict 지정.
  - 📅 Day 4 / ⏱ 30m / 🛠 ✔
- 🔴 **[Pydantic docs](https://docs.pydantic.dev/)**
  - 💬 v2 기준 BaseModel, Field, Validator. `EmailStr`, `AnyUrl` 등 타입.
  - 📅 Day 4 / ⏱ 1.5h / 🛠 ✔
- 🟡 **[pydantic.dev](https://pydantic.dev/)**
  - 💬 회사 페이지. 제품 라인업(Pydantic / Logfire / Pydantic AI).
  - 📅 Day 4 / ⏱ 10m

---

## 4. Function Calling / Tool Use

- 🔴 **[OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling)**
  - 💬 `tools` 배열 정의, parallel, `tool_choice` 옵션.
  - 📅 Day 5 / ⏱ 1h / 🛠 ✔
- 🔴 **[OpenAI Cookbook — Responses API tool orchestration](https://developers.openai.com/cookbook/examples/responses_api/responses_api_tool_orchestration)**
  - 💬 새 Responses API로 복합 tool workflow.
  - 📅 Day 5 / ⏱ 1h / 🛠 ✔
- 🔴 **[OpenAI Cookbook](https://developers.openai.com/cookbook)** (중복)
- 🔴 **[Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)**
  - 💬 Client tools (사용자 정의) vs server tools (Anthropic 실행: web_search, code_execution, web_fetch, tool_search). `stop_reason: "tool_use"` 루프. `strict: true`로 스키마 강제.
  - 📅 Day 5 / ⏱ 30m
- 🔴 **[Anthropic courses — tool_use](https://github.com/anthropics/courses/tree/master/tool_use)**
  - 💬 6-lesson 하드코어 실습 코스. **Day 5의 메인**.
  - 📅 Day 5 / ⏱ 3h / 🛠 ✔
- 🟡 **[Anthropic — Advanced tool use blog](https://www.anthropic.com/engineering/advanced-tool-use)**
  - 💬 engineering 블로그. parallel, long-horizon 팁.
  - 📅 Day 5 / ⏱ 30m
- 🔴 **[Gemini — Function calling](https://ai.google.dev/gemini-api/docs/function-calling)**
  - 💬 `function_declarations`, automatic function calling.
  - 📅 Day 5 / ⏱ 30m / 🛠 ✔
- 🟡 **[LlamaIndex — Gemini agent example](https://developers.llamaindex.ai/python/examples/agent/gemini_agent/)**
  - 💬 LlamaIndex에서 Gemini로 agent 만드는 예제.
  - 📅 Day 10 / ⏱ 30m / 🛠 ✔

---

## 5. Embeddings

- 🔴 **[OpenAI — Embeddings guide](https://platform.openai.com/docs/guides/embeddings)**
  - 💬 `text-embedding-3-small/large`, 차원 조절.
  - 📅 Day 6 / ⏱ 1h / 🛠 ✔
- 🔴 **[OpenAI Cookbook](https://developers.openai.com/cookbook)** (중복)
- 🔴 **[Gemini — Embeddings](https://ai.google.dev/gemini-api/docs/embeddings)**
  - 💬 `text-embedding-004`, task-specific types.
  - 📅 Day 6 / ⏱ 30m / 🛠 ✔
- 🟡 **[Google for Developers blog — Gemini Embedding for RAG](https://developers.googleblog.com/en/gemini-embedding-powering-rag-context-engineering/)**
  - 💬 RAG 맥락에서 embedding 역할 마케팅 글. 개념 확인용.
  - 📅 Day 6 / ⏱ 15m
- 🔴 **[HF — sentence-transformers](https://huggingface.co/sentence-transformers)**
  - 💬 10k+ 사전학습 모델 허브.
  - 📅 Day 6 / ⏱ 20m
- 🔴 **[SBERT (sbert.net)](https://www.sbert.net/)**
  - 💬 Sentence Transformers 공식 사이트. Bi-encoder / Cross-encoder / Sparse encoder. Semantic search, reranking, clustering, image search까지.
  - 📅 Day 6, 8 / ⏱ 1h / 🛠 ✔
- 🔴 **[MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)**
  - 💬 Embedding 모델 성능 리더보드. 작업/언어별 필터.
  - 📅 Day 6 / ⏱ 30m

---

## 6. Vector DB

### Qdrant
- 🔴 **[Qdrant docs](https://qdrant.tech/documentation/)**
  - 💬 Getting Started, User Manual (data mgmt, search, inference), Qdrant Tools (FastEmbed, MCP Server), Tutorials. Hybrid, advanced retrieval, quantization, multitenancy. Edge도 지원(offline).
  - 📅 Day 6-7 / ⏱ 2h / 🛠 ✔
- 🔴 **[Qdrant Quickstart](https://qdrant.tech/documentation/quickstart/)**
  - 💬 Docker 한 줄로 시작 → collection → upsert → search.
  - 📅 Day 6 / ⏱ 1h / 🛠 ✔
- 🔴 **[Qdrant — RAG (DeepSeek) tutorial](https://qdrant.tech/documentation/tutorials-build-essentials/rag-deepseek/)**
  - 💬 RAG pipeline을 Qdrant로 처음부터.
  - 📅 Day 6-7 / ⏱ 1.5h / 🛠 ✔

### Weaviate
- 🟡 **[Weaviate docs](https://docs.weaviate.io/weaviate)**
  - 💬 Open-source vector DB. Semantic + hybrid, RAG, agent workflow. 배포: WCD / Docker / K8s / Embedded.
  - 📅 Day 8 선택 / ⏱ 1h
- 🟡 **[Weaviate Quickstart](https://docs.weaviate.io/weaviate/quickstart)**
  - 💬 빠른 시작.
  - 📅 Day 8 선택 / ⏱ 30m
- 🟡 **[Weaviate — Generative starter](https://docs.weaviate.io/weaviate/starter-guides/generative)**
  - 💬 Generative modules로 RAG.
  - 📅 Day 8 선택 / ⏱ 30m
- 🟡 **[weaviate-tutorials (GitHub org)](https://github.com/weaviate-tutorials)**
  - 💬 공식 튜토리얼 레포 모음.
  - 📅 나중에

### Pinecone
- 🟡 **[Pinecone docs](https://docs.pinecone.io/)**
  - 💬 완전 관리형. Integrated embedding 모드 or BYO vectors. Semantic + lexical + reranking + namespace.
  - 📅 나중에 / ⏱ 1h
- 🟡 **[Pinecone Learn](https://www.pinecone.io/learn/)**
  - 💬 RAG/embedding 개념 글 시리즈.
  - 📅 나중에 / ⏱ 2h

### Chroma / FAISS / pgvector
- 🟡 **[Chroma docs](https://docs.trychroma.com/)**
  - 💬 Apache 2.0. Self-host 또는 Chroma Cloud. In-memory부터 persistent, 멀티모달.
  - 📅 나중에 / ⏱ 30m
- 🟡 **[Chroma (GitHub)](https://github.com/chroma-core/chroma)**
  - 💬 위와 동일.
  - 📅 나중에
- 🟢 **[FAISS (GitHub)](https://github.com/facebookresearch/faiss)**
  - 💬 Meta의 벡터 검색 **라이브러리** (DB 아님). 다른 DB의 내부 엔진으로 쓰임.
  - 📅 나중에 (원리 궁금할 때)
- 🟢 **[FAISS — faiss.ai](https://faiss.ai/)**
  - 💬 동일.
- 🟡 **[pgvector (GitHub)](https://github.com/pgvector/pgvector)**
  - 💬 Postgres 확장. 기존 Postgres 있으면 최선.
  - 📅 나중에 / ⏱ 1h / 🛠 실무에서 자주 쓰임
- 🟡 **[Supabase AI docs](https://supabase.com/docs/guides/ai)**
  - 💬 Supabase(Postgres+pgvector) 기반 AI 가이드.
  - 📅 나중에 / ⏱ 1h

---

## 7. RAG 기본

- 🔴 **[LangChain — RAG From Scratch (GitHub)](https://github.com/langchain-ai/rag-from-scratch)**
  - 💬 5개 노트북, 18 Part. `1-4.ipynb` 기초(index/retrieval/generation), `5-9.ipynb` 중급, `10-11.ipynb`/`12-14.ipynb`/`15-18.ipynb` 고급. **Day 7-8 메인 자료**.
  - 📅 Day 7-8 / ⏱ 5h / 🛠 ✔
- 🔴 **[RAG From Scratch — YouTube Playlist](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x)**
  - 💬 위 노트북들의 영상 해설.
  - 📅 Day 7-8 / ⏱ 3h / 🛠 —
- 🟡 **[RAG From Scratch — Intro video](https://www.youtube.com/watch?v=sVcwVQRHIc8)**
  - 💬 플레이리스트 첫 영상.
  - 📅 Day 7 / ⏱ 15m
- 🔴 **[LlamaIndex — Understanding RAG](https://developers.llamaindex.ai/python/framework/understanding/rag/)**
  - 💬 5단계 (Loading / Indexing / Storing / Querying / Evaluation). 핵심 컴포넌트: Document/Node, Retriever, Router, Response Synthesizer.
  - 📅 Day 7 / ⏱ 1.5h / 🛠 ✔
- 🔴 **[LlamaIndex docs](https://docs.llamaindex.ai/)**
  - 💬 전체 docs 허브.
  - 📅 Day 7-10 상시 / ⏱ 참조
- 🟡 **[LlamaIndex (GitHub)](https://github.com/run-llama/llama_index)**
  - 💬 오픈소스 레포.
- 🔴 **[OpenAI Cookbook — QA using embeddings](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb)**
  - 💬 RAG 교과서 노트북. 짧고 핵심만.
  - 📅 Day 7 / ⏱ 1h / 🛠 ✔
- 🟡 **[OpenAI Cookbook — Parse PDF for RAG](https://developers.openai.com/cookbook/examples/parse_pdf_docs_for_rag)**
  - 💬 PDF 파싱/chunking 노하우.
  - 📅 Day 7 / ⏱ 1h / 🛠 ✔
- 🔴 **[OpenAI Cookbook 홈](https://developers.openai.com/cookbook)** (중복)
- 🟡 **[Google codelab — Multimodal RAG Gemini](https://codelabs.developers.google.com/multimodal-rag-gemini)**
  - 💬 이미지 포함 RAG.
  - 📅 나중에 / ⏱ 2h / 🛠 ✔
- 🟡 **[GCP — Intro multimodal RAG notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/use-cases/retrieval-augmented-generation/intro_multimodal_rag.ipynb)**
  - 💬 Vertex AI + Gemini 멀티모달 RAG.
  - 📅 나중에 / ⏱ 2h / 🛠 ✔

---

## 8. RAG 개선

- 🔴 **[OpenAI Cookbook — Reranking with cross-encoders](https://github.com/openai/openai-cookbook/blob/main/examples/Search_reranking_with_cross-encoders.ipynb)**
  - 💬 Bi-encoder로 top-50 → Cross-encoder로 top-5 재정렬.
  - 📅 Day 8 / ⏱ 1h / 🛠 ✔
- 🔴 **[SBERT — Cross-Encoders](https://www.sbert.net/examples/cross_encoder/applications/README.html)**
  - 💬 Cross-encoder 사용법.
  - 📅 Day 8 / ⏱ 30m / 🛠 ✔
- 🟡 **[HF — cross-encoder models](https://huggingface.co/cross-encoder)**
  - 💬 cross-encoder/ms-marco-MiniLM-L-6-v2 같은 모델 허브.
  - 📅 Day 8 / ⏱ 10m
- 🔴 **[Qdrant — Hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/)**
  - 💬 Dense + sparse 결합, RRF, fusion.
  - 📅 Day 8 / ⏱ 1h / 🛠 ✔
- 🟡 **[Weaviate — Hybrid search](https://docs.weaviate.io/weaviate/search/hybrid)**
  - 💬 Weaviate 버전.
  - 📅 Day 8 / ⏱ 30m
- 🟡 **[LlamaIndex — Qdrant hybrid](https://docs.llamaindex.ai/en/stable/examples/vector_stores/qdrant_hybrid/)**
  - 💬 LlamaIndex + Qdrant hybrid 예제.
  - 📅 Day 8 / ⏱ 30m / 🛠 ✔
- 🔴 **[LangChain — RAG From Scratch](https://github.com/langchain-ai/rag-from-scratch)** (중복, 고급 Part)
- 🟡 **[LlamaIndex — Optimizing](https://developers.llamaindex.ai/python/framework/optimizing/)**
  - 💬 RAG 최적화 가이드.
  - 📅 Day 8 / ⏱ 1h
- 🟡 **[LlamaIndex — Querying guide](https://docs.llamaindex.ai/en/stable/module_guides/querying/)**
  - 💬 query engine 커스터마이징.
  - 📅 Day 8 / ⏱ 1h

---

## 9. Eval

- 🔴 **[OpenAI Cookbook — Evals topic](https://developers.openai.com/cookbook/topic/evals)**
  - 💬 22개 notebook: structured output eval, tools eval, web search eval, image/audio input eval, prompt regression, bulk experiment, RAG eval, MCP eval, "Eval Driven System Design", agent evals.
  - 📅 Day 9 / ⏱ 2h / 🛠 ✔
- 🔴 **[OpenAI Cookbook — Getting started with OpenAI evals](https://developers.openai.com/cookbook/examples/evaluation/getting_started_with_openai_evals)**
  - 💬 첫 eval 작성.
  - 📅 Day 9 / ⏱ 1h / 🛠 ✔
- 🟡 **[OpenAI — Evals guide](https://developers.openai.com/api/docs/guides/evals)**
  - 💬 대시보드 기반 evals.
  - 📅 Day 9 / ⏱ 30m
- 🟡 **[openai/evals (GitHub)](https://github.com/openai/evals)**
  - 💬 오픈소스 eval framework. 지금은 Platform evals가 더 편함.
  - 📅 Day 9 선택 / ⏱ 1h
- 🔴 **[Cookbook — Evaluate RAG with LlamaIndex](https://developers.openai.com/cookbook/examples/evaluation/evaluate_rag_with_llamaindex)**
  - 💬 실전 RAG eval.
  - 📅 Day 9 / ⏱ 1h / 🛠 ✔
- 🔴 **[Ragas docs](https://docs.ragas.io/)**
  - 💬 Experiments-first 접근. Faithfulness, answer relevancy, context precision/recall. LangChain/LlamaIndex 통합.
  - 📅 Day 9 / ⏱ 2h / 🛠 ✔
- 🟡 **[Colab — openai-ragas-eval-cookbook](https://colab.research.google.com/github/shahules786/openai-cookbook/blob/ragas/examples/evaluation/ragas/openai-ragas-eval-cookbook.ipynb)**
  - 💬 Ragas + OpenAI 결합 cookbook (fork).
  - 📅 Day 9 / ⏱ 1h / 🛠 ✔
- 🔴 **[LlamaIndex — Evaluating](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/)**
  - 💬 LlamaIndex 자체 eval 도구.
  - 📅 Day 9 / ⏱ 1h / 🛠 ✔
- 🟡 **[LlamaIndex — Observability notebook](https://developers.llamaindex.ai/python/examples/cookbooks/oreilly_course_cookbooks/module-5/observability/)**
  - 💬 O'Reilly 코스의 observability 모듈.
  - 📅 Day 12 / ⏱ 1h

---

## 10. Agents

- 🔴 **[HF Agents Course](https://huggingface.co/learn/agents-course)** (중복)
- 🔴 **[HF Agents Course — GitHub](https://github.com/huggingface/agents-course)** (중복)
- 🔴 **[HF Agents Course — unit0](https://huggingface.co/learn/agents-course/unit0/introduction)** (중복)
- 🔴 **[HF Agents Course — smolagents retrieval](https://huggingface.co/learn/agents-course/unit2/smolagents/retrieval_agents)** (중복)
- 🔴 **[LangGraph docs](https://langchain-ai.github.io/langgraph/)**
  - 💬 docs.langchain.com/langgraph 로 이동. StateGraph + Node + Edge + conditional_edges + checkpointing + interrupts로 상태머신 에이전트.
  - 📅 Day 10 / ⏱ 2h / 🛠 ✔
- 🔴 **[LangGraph (GitHub)](https://github.com/langchain-ai/langgraph)**
  - 💬 오픈소스 레포.
  - 📅 Day 10 / ⏱ 참조
- 🟡 **[LangChain Academy](https://academy.langchain.com/)**
  - 💬 LangGraph 공식 무료 코스.
  - 📅 Day 10 / ⏱ 4h / 🛠 ✔
- 🔴 **[LlamaIndex — Agents](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/)**
  - 💬 LlamaIndex agent 시스템.
  - 📅 Day 10 / ⏱ 1h
- 🟡 **[LlamaIndex — Understanding Agent](https://developers.llamaindex.ai/python/framework/understanding/agent/)**
  - 💬 개념 설명.
  - 📅 Day 10 / ⏱ 30m
- 🔴 **[Pydantic AI overview](https://pydantic.dev/docs/ai/overview/)**
  - 💬 FastAPI-style DX + Pydantic validation + Logfire. MCP/A2A/UI 지원. OpenAI/Anthropic/Gemini/DeepSeek/Grok/Cohere/Mistral/Perplexity/Bedrock/Vertex/Ollama.
  - 📅 Day 10 / ⏱ 1h / 🛠 ✔
- 🟡 **[Pydantic AI — Agent core concepts](https://pydantic.dev/docs/ai/core-concepts/agent/)**
  - 💬 핵심 컨셉.
  - 📅 Day 10 / ⏱ 30m
- 🟡 **[Pydantic AI (GitHub)](https://github.com/pydantic/pydantic-ai)**
  - 💬 오픈소스 레포.
- 🟢 **[CrewAI docs](https://docs.crewai.com/)**
  - 💬 Multi-agent 프레임워크. 2주에는 우선순위 낮음.
  - 📅 나중에 / ⏱ —
- 🟢 **[CrewAI (GitHub)](https://github.com/crewAIInc/crewAI)**
  - 💬 레포.
  - 📅 나중에

---

## 11. MCP (Model Context Protocol)

- 🔴 **[modelcontextprotocol.io](https://modelcontextprotocol.io/)**
  - 💬 "USB-C for AI applications" 비유. 오픈 표준. Claude/ChatGPT/VS Code/Cursor 등 광범위 지원.
  - 📅 Day 11 / ⏱ 1.5h / 🛠 ✔
- 🔴 **[MCP docs](https://modelcontextprotocol.io/docs)**
  - 💬 Develop (build-server / build-client / build-app), Learn (architecture).
  - 📅 Day 11 / ⏱ 2h / 🛠 ✔
- 🔴 **[MCP GitHub org](https://github.com/modelcontextprotocol)**
  - 💬 SDKs/servers org.
  - 📅 Day 11 / ⏱ 참조
- 🔴 **[Anthropic — MCP](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)**
  - 💬 Anthropic 관점의 MCP connector 가이드.
  - 📅 Day 11 / ⏱ 1h
- 🔴 **[MCP reference servers (GitHub)](https://github.com/modelcontextprotocol/servers)**
  - 💬 filesystem, fetch, github, slack 등 공식 서버 예제. 읽으면서 패턴 학습.
  - 📅 Day 11 / ⏱ 1.5h / 🛠 ✔
- 🔴 **[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)**
  - 💬 Python 구현체. `FastMCP` 고수준 API.
  - 📅 Day 11 / ⏱ 2h / 🛠 ✔
- 🟡 **[MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)**
  - 💬 TS 버전.
  - 📅 나중에

---

## 12. Observability

### Langfuse
- 🔴 **[Langfuse docs](https://langfuse.com/docs)**
  - 💬 Open-source self-hostable. Observability + Prompt management + Evaluation.
  - 📅 Day 12 / ⏱ 1.5h / 🛠 ✔
- 🔴 **[Langfuse — Tracing](https://langfuse.com/docs/tracing)**
  - 💬 `@observe` decorator, 통합 SDK.
  - 📅 Day 12 / ⏱ 1h / 🛠 ✔
- 🔴 **[Langfuse — Prompt management](https://langfuse.com/docs/prompt-management/overview)**
  - 💬 Prompt versioning + label(production/staging).
  - 📅 Day 12 / ⏱ 1h / 🛠 ✔
- 🔴 **[Langfuse — Scores](https://langfuse.com/docs/scores/overview)**
  - 💬 Eval 결과를 score로 저장.
  - 📅 Day 12 / ⏱ 30m / 🛠 ✔
- 🔴 **[Langfuse (GitHub)](https://github.com/langfuse/langfuse)**
  - 💬 Self-host용.
  - 📅 Day 12 / ⏱ 참조

### Phoenix (Arize)
- 🟡 **[Phoenix](https://phoenix.arize.com/)**
  - 💬 Open-source tracing + eval. OpenTelemetry 기반, no vendor lock-in.
  - 📅 Day 12 / ⏱ 1h
- 🟡 **[Phoenix docs](https://docs.arize.com/phoenix)**
  - 💬 Tracing, Evaluation, Playground, Datasets, Experiments.
  - 📅 Day 12 / ⏱ 1h / 🛠 ✔
- 🟡 **[Phoenix (GitHub)](https://github.com/Arize-ai/phoenix)**
  - 💬 레포.
- 🟡 **[Phoenix — Colab tutorial](https://colab.research.google.com/github/Arize-ai/phoenix/blob/main/tutorials/llm_application_tracing_evaluating_and_analysis.ipynb)**
  - 💬 한 번에 tracing/eval/analysis.
  - 📅 Day 12 / ⏱ 1h / 🛠 ✔

### LangSmith
- 🟡 **[LangSmith docs](https://docs.smith.langchain.com/)**
  - 💬 LangChain 상용 observability. LangGraph 쓰면 자연스러움.
  - 📅 Day 12 / ⏱ 1h
- 🟡 **[LangChain Academy](https://academy.langchain.com/)** (중복)

### OpenTelemetry
- 🟡 **[OpenTelemetry docs](https://opentelemetry.io/docs/)**
  - 💬 Tracing 표준. Phoenix/Langfuse 모두 지원.
  - 📅 Day 12 / ⏱ 1h

---

## 13. Production

- 🔴 **[OpenAI Cookbook — How to handle rate limits](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb)**
  - 💬 Tenacity, exponential backoff, batch queue 패턴.
  - 📅 Day 12 / ⏱ 30m / 🛠 ✔
- 🔴 **[OpenAI Cookbook — How to stream completions](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb)**
  - 💬 Streaming 패턴.
  - 📅 Day 12 / ⏱ 30m / 🛠 ✔
- 🔴 **[OpenAI — Rate limits](https://platform.openai.com/docs/guides/rate-limits)**
  - 💬 RPM/TPM 정책.
  - 📅 Day 12 / ⏱ 30m
- 🟡 **[OpenAI — Latency optimization](https://platform.openai.com/docs/guides/latency-optimization)**
  - 💬 Streaming, prompt caching, model routing.
  - 📅 Day 12 / ⏱ 30m
- 🔴 **[OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching)**
  - 💬 Implicit cache (system prompt 선두 일치).
  - 📅 Day 12 / ⏱ 30m
- 🔴 **[Anthropic — Rate limits](https://docs.anthropic.com/en/api/rate-limits)**
  - 💬 429 처리, `retry-after` 헤더.
  - 📅 Day 12 / ⏱ 30m
- 🔴 **[Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)**
  - 💬 `cache_control` 명시적 캐시. 90% 토큰 비용 절감 가능.
  - 📅 Day 12 / ⏱ 30m / 🛠 ✔
- 🔴 **[Anthropic — Streaming](https://docs.anthropic.com/en/docs/build-with-claude/streaming)**
  - 💬 SSE 이벤트 타입.
  - 📅 Day 12 / ⏱ 30m
- 🔴 **[Gemini — Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)**
  - 💬 tier별 RPM/TPM.
  - 📅 Day 12 / ⏱ 20m
- 🔴 **[Gemini — Caching](https://ai.google.dev/gemini-api/docs/caching)**
  - 💬 명시적 context caching (TTL 기반).
  - 📅 Day 12 / ⏱ 30m
- 🟡 **[Gemini — Tokens](https://ai.google.dev/gemini-api/docs/tokens)**
  - 💬 토큰 카운팅.
  - 📅 Day 12 / ⏱ 15m

---

## 14. Local LLM / Self-hosting

### Ollama
- 🔴 **[Ollama 홈](https://ollama.com/)**
  - 💬 macOS/Win/Linux 로컬 모델 런처.
  - 📅 Day 13 / ⏱ 15m / 🛠 ✔
- 🔴 **[Ollama docs](https://docs.ollama.com/)**
  - 💬 Quickstart, Download, Cloud models, API, Python/JS libs. gpt-oss, Gemma 3, DeepSeek-R1, Qwen3 등.
  - 📅 Day 13 / ⏱ 1h / 🛠 ✔
- 🔴 **[Ollama (GitHub)](https://github.com/ollama/ollama)**
  - 💬 레포.
- 🔴 **[Ollama API docs](https://github.com/ollama/ollama/blob/main/docs/api.md)**
  - 💬 `/api/generate`, `/api/chat`, OpenAI 호환 `/v1/*`.
  - 📅 Day 13 / ⏱ 30m / 🛠 ✔

### llama.cpp
- 🟡 **[llama.cpp (GitHub)](https://github.com/ggml-org/llama.cpp)**
  - 💬 C/C++ GGUF 인퍼런스. Mac/CPU 친화.
  - 📅 Day 13 선택 / ⏱ 30m / 🛠 ✔
- 🟡 **[llama-cpp-python server](https://llama-cpp-python.readthedocs.io/en/latest/server/)**
  - 💬 OpenAI-compatible Python 서버.
  - 📅 Day 13 선택 / ⏱ 30m / 🛠 ✔

### vLLM
- 🔴 **[vLLM docs](https://docs.vllm.ai/)**
  - 💬 PagedAttention, continuous batching, OpenAI 호환 서버, FP8/INT4/GPTQ/AWQ, 분산 (tensor/pipeline/data parallel), 200+ 모델, NVIDIA/AMD/CPU/TPU/Gaudi.
  - 📅 Day 13 / ⏱ 1h / 🛠 ✔
- 🔴 **[vLLM — OpenAI-compatible server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server/)**
  - 💬 `python -m vllm.entrypoints.openai.api_server` 한 줄.
  - 📅 Day 13 / ⏱ 30m / 🛠 ✔
- 🔴 **[vLLM (GitHub)](https://github.com/vllm-project/vllm)**
  - 💬 레포.

### HF 스택
- 🟡 **[HF Transformers docs](https://huggingface.co/docs/transformers/index)**
  - 💬 transformers 라이브러리 표준 참조.
  - 📅 나중에 / ⏱ 1h
- 🟡 **[HF Transformers (GitHub)](https://github.com/huggingface/transformers)**
  - 💬 레포.
- 🟡 **[HF TGI docs](https://huggingface.co/docs/text-generation-inference/index)**
  - 💬 Hugging Face 공식 추론 서버. Rust.
  - 📅 나중에 / ⏱ 1h
- 🟡 **[HF TGI (GitHub)](https://github.com/huggingface/text-generation-inference)**
  - 💬 레포.
- 🟡 **[Unsloth docs](https://docs.unsloth.ai/)**
  - 💬 빠른 fine-tuning. QLoRA 2-5x 가속.
  - 📅 나중에 (fine-tune 시) / ⏱ 2h
- 🟡 **[Unsloth (GitHub)](https://github.com/unslothai/unsloth)**
  - 💬 레포.

---

## 15. RunPod

- 🔴 **[RunPod 홈](https://www.runpod.io/)**
  - 💬 GPU cloud. 시간/초 단위 과금.
  - 📅 Day 13 / ⏱ 15m
- 🔴 **[RunPod docs](https://docs.runpod.io/)**
  - 💬 Pods(전용 GPU), Serverless(초단위), Flash(로컬 터미널→원격 GPU), Instant Clusters(분산), Network Volume, Public Endpoints.
  - 📅 Day 13 / ⏱ 1h / 🛠 ✔
- 🔴 **[RunPod — Pods overview](https://docs.runpod.io/pods/overview)**
  - 💬 Persistent GPU 인스턴스.
  - 📅 Day 13 / ⏱ 30m
- 🔴 **[RunPod — Serverless overview](https://docs.runpod.io/serverless/overview)**
  - 💬 Request당 과금, scale-to-zero.
  - 📅 Day 13 / ⏱ 30m
- 🔴 **[RunPod Serverless — vLLM get started](https://docs.runpod.io/serverless/vllm/get-started)**
  - 💬 **Day 13 실습의 핵심**. 공식 worker-vllm로 엔드포인트 한 번에.
  - 📅 Day 13 / ⏱ 1h / 🛠 ✔
- 🔴 **[RunPod Serverless — vLLM configuration](https://docs.runpod.io/serverless/vllm/configuration)**
  - 💬 모델, max_model_len, GPU 타입 등 설정.
  - 📅 Day 13 / ⏱ 30m / 🛠 ✔
- 🔴 **[vLLM — RunPod deployment](https://docs.vllm.ai/en/latest/deployment/frameworks/runpod/)**
  - 💬 vLLM 공식 관점.
  - 📅 Day 13 / ⏱ 30m
- 🟡 **[runpod-workers/worker-vllm (GitHub)](https://github.com/runpod-workers/worker-vllm)**
  - 💬 Serverless worker 소스.
  - 📅 Day 13 / ⏱ 30m

---

## 16. 모델 찾기 / 리더보드

- 🔴 **[HF Models](https://huggingface.co/models)**
  - 💬 메인 모델 검색 허브.
  - 📅 Day 13 / ⏱ 15m
- 🔴 **[Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)**
  - 💬 자동 벤치 기반. 편향 있음 — 참고용.
  - 📅 Day 13 / ⏱ 30m
- 🔴 **[LMArena / Chatbot Arena Leaderboard](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard)**
  - 💬 사람 투표 Elo. 현실 성능에 더 가까움.
  - 📅 Day 13 / ⏱ 15m
- 🟡 **[LMArena 홈](https://lmarena.ai/)**
  - 💬 투표 UI.
  - 📅 Day 13 / ⏱ 10m
- 🟡 **[Chatbot Arena (구 링크)](https://chat.lmsys.org/)**
  - 💬 LMArena로 리브랜드. 일부 구 링크.
  - 📅 참조
- 🔴 **[MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)** (중복)

---

## 17. Fine-tuning (🟢 14일 이후 트랙)

- 🟢 **[OpenAI — Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)**
  - 💬 GPT-4o-mini/3.5 fine-tuning.
  - 📅 나중에 / ⏱ 2h / 🛠 ✔
- 🟢 **[HF PEFT docs](https://huggingface.co/docs/peft/index)**
  - 💬 LoRA, QLoRA, Prefix tuning 등.
  - 📅 나중에 / ⏱ 2h
- 🟢 **[HF PEFT (GitHub)](https://github.com/huggingface/peft)**
  - 💬 레포.
- 🟢 **[HF TRL docs](https://huggingface.co/docs/trl/index)**
  - 💬 SFT, DPO, PPO, RLHF.
  - 📅 나중에 / ⏱ 2h
- 🟢 **[HF TRL (GitHub)](https://github.com/huggingface/trl)**
  - 💬 레포.
- 🟢 **[Axolotl (GitHub)](https://github.com/axolotl-ai-cloud/axolotl)**
  - 💬 YAML 설정으로 fine-tuning 파이프라인.
  - 📅 나중에 / ⏱ 2h
- 🟢 **[Unsloth](https://docs.unsloth.ai/)** (중복)
- 🟢 **[Unsloth (GitHub)](https://github.com/unslothai/unsloth)** (중복)

---

## 18. 논문 (🟢 요약만, Claude한테 시킬 것)

- 🟢 **[Attention Is All You Need — arxiv](https://arxiv.org/abs/1706.03762)** / [PDF](https://arxiv.org/pdf/1706.03762)
  - 💬 Transformer 원 논문 (2017). Self-attention 기반, recurrence/conv 없이.
  - 📅 Day 1 Figure 1,2만 / 나중에 정독 / ⏱ 30m
- 🟢 **[RAG — Lewis 2020 (arxiv)](https://arxiv.org/abs/2005.11401)** / [NeurIPS PDF](https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf)
  - 💬 Parametric + non-parametric memory 결합. RAG 용어 확립.
  - 📅 Day 7 초록만 / 나중에 정독 / ⏱ 30m
- 🟢 **[Chain-of-Thought Prompting (arxiv)](https://arxiv.org/abs/2201.11903)** / [PDF](https://arxiv.org/pdf/2201.11903)
  - 💬 "Let's think step by step"의 유래. reasoning task 성능 ↑.
  - 📅 Day 3 / ⏱ 30m
- 🟢 **[ReAct (arxiv)](https://arxiv.org/abs/2210.03629)** / [PDF](https://arxiv.org/pdf/2210.03629)
  - 💬 Reasoning + Acting interleave. Agent의 원형.
  - 📅 Day 10 / ⏱ 30m
- 🟢 **[ReAct — Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)**
  - 💬 블로그 요약. 논문보다 빠름.
  - 📅 Day 10 / ⏱ 15m

---

## 19. YouTube (🟡 보조)

- 🔴 **[LLM Zoomcamp playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIoBpuc900htYF4uhEAbaT-)** (중복)
- 🟡 **[LLM Zoomcamp — intro video](https://www.youtube.com/watch?v=FgnelhEJFj0)**
  - 💬 코스 오리엔테이션.
  - 📅 Day 7 / ⏱ 15m
- 🔴 **[RAG From Scratch playlist](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x)** (중복)
- 🟡 **[RAG From Scratch — intro](https://www.youtube.com/watch?v=sVcwVQRHIc8)** (중복)
- 🟡 **[DeepLearning.AI YouTube](https://www.youtube.com/@Deeplearningai)**
  - 💬 short course 클립.
  - 📅 참조
- 🔴 **[DeepLearning.AI short courses](https://www.deeplearning.ai/short-courses/)** (중복)
- 🟡 **[LangChain YouTube](https://www.youtube.com/@LangChain)**
  - 💬 live coding, webinar.
  - 📅 참조
- 🟡 **[LangChain Academy](https://academy.langchain.com/)** (중복)
- 🟡 **[Hugging Face YouTube](https://www.youtube.com/@HuggingFace)**
  - 💬 workshop, paper reading.
  - 📅 참조
- 🟡 **[Hugging Face — Learn](https://huggingface.co/learn)**
  - 💬 모든 코스 허브.
  - 📅 참조
- 🟡 **[Google Developers YouTube](https://www.youtube.com/@GoogleDevelopers)**
  - 💬 Gemini 기능 데모.
  - 📅 참조
- 🔴 **[Google ML Crash Course LLM](https://developers.google.com/machine-learning/crash-course/llm)** (중복)
- 🟡 **[OpenAI Developers YouTube](https://www.youtube.com/@OpenAIDevs)**
  - 💬 DevDay 등.
  - 📅 참조
- 🔴 **[OpenAI Cookbook](https://developers.openai.com/cookbook)** (중복)
- 🟡 **[Anthropic YouTube](https://www.youtube.com/@anthropic-ai)**
  - 💬 research 요약, 엔지니어링 토크.
  - 📅 참조
- 🔴 **[Anthropic — Build with Claude](https://www.anthropic.com/learn/build-with-claude)** (중복)

---

## 20. 한국어 보조 자료

- 🟡 **[Google ML Crash Course LLM — Transformers (한국어)](https://developers.google.com/machine-learning/crash-course/llm/transformers?hl=ko)**
  - 💬 Google 공식 한국어 번역 (일부).
  - 📅 Day 1 보조 / ⏱ 1h

### 한국어 검색 키워드 (Claude에게 시킬 것)
- LLM RAG 한국어 튜토리얼
- LangChain RAG 한국어
- Qdrant RAG 한국어
- vLLM 한국어 튜토리얼
- Ollama 로컬 LLM 한국어
- LangGraph 한국어
- LLM evaluation 한국어
- RAGAS 한국어
- Langfuse 한국어

---

## 21. (원문 섹션) Claude 분류 프롬프트
정리 방식으로만 참고 — 실제 적용은 위 분류 그대로.

## 22. (원문 섹션) 우선순위 Top 20 — `00-top20-priority.md` 참조

---

## 분류 통계
- 🔴 필수: ~80개 (14일 플랜 소화 대상)
- 🟡 선택: ~50개 (여력 시)
- 🟢 나중에: ~20개 (14일 이후 트랙)
- ⚪ 중복/스킵: ~15개 (같은 내용의 다른 URL)

중복/스킵 상세 → `skip.md`
필수 짧은 리스트 → `must-read.md`
선택 → `optional.md`
나중에 → `later.md`
