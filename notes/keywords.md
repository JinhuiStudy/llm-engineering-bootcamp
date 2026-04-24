# 모르면 안 되는 핵심 키워드

8년차 개발자가 2주 안에 체화해야 할 LLM 엔지니어링 용어 사전.
"이 단어 들었을 때 정의 + 1줄 예시가 즉답되어야 한다"는 기준.

## Tier S — 매일 10번 이상 마주침
- **Token** — 모델이 처리하는 최소 단위. 글자나 단어 아님. "안녕하세요" ≈ 4-5 tokens.
- **Context window** — 한 번에 모델이 볼 수 있는 총 토큰 수 (입력+출력). **Claude 4.x는 1M GA (2026-04)**, Gemini 1M+.
- **Prompt** — 모델에 보내는 입력 전체 (system + messages).
- **System prompt** — 모델의 역할/규칙을 지시하는 상위 프롬프트. Anthropic은 top-level, OpenAI/Gemini는 messages 배열 안.
- **Temperature** — 출력 랜덤성 조절 (0=결정적, 1+=창발적). Structured output은 0 근처.
- **Top-p / Top-k** — sampling 제한. 대부분 default.
- **max_tokens** — 생성 상한. 비용 가드.
- **Streaming** — SSE로 토큰 단위 점진 출력. UX에 필수.
- **Embedding** — 텍스트 → 고차원 벡터. 의미 기반 검색의 기초.
- **Vector DB** — embedding을 저장하고 유사도 검색하는 DB. Qdrant/Weaviate/Pinecone/Chroma/pgvector.
- **RAG** — Retrieval-Augmented Generation. 외부 지식을 LLM에 주입해 환각 줄이기.
- **Tool use / Function calling** — LLM이 외부 함수를 호출하게 하는 구조화된 메커니즘.
- **Structured Output** — JSON schema로 출력 강제. strict=true로 100% 보장.
- **Agent** — LLM + tool + state + loop. 여러 단계를 자율 수행.

## Tier A — 핵심 개념
- **Transformer** — self-attention 기반 구조. 현대 LLM의 골격.
- **Self-attention** — 입력 내 토큰들이 서로 관계를 계산. "이 단어가 어느 단어를 참조하는가".
- **Decoder-only** — GPT/Claude/Gemini 계열. 입력 → 다음 토큰 예측.
- **Encoder-only** — BERT 계열. 임베딩/분류용.
- **Encoder-decoder** — T5 계열. 번역/요약 원류.
- **Logit / Softmax / Sampling** — 다음 토큰 확률 계산 → 선택.
- **Tokenizer** — 텍스트를 토큰으로 쪼개는 알고리즘. BPE, SentencePiece.
- **Few-shot / Zero-shot** — 예시 없이 / 예시 몇 개 주고 태스크 지시.
- **Chain-of-Thought (CoT)** — "step by step" 생각 유도로 reasoning 향상.
- **ReAct** — Reasoning + Acting. Agent의 원형 패턴.
- **Prompt injection** — 공격자가 시스템 지시를 덮어쓰려는 시도.
- **Jailbreak** — 모델 안전장치 우회 시도.
- **Hallucination** — 사실과 다른 출력. RAG/grounding으로 완화.
- **Grounding / Citation** — 출력이 주어진 근거에서 왔음을 표시.

## Tier B — RAG / 검색
- **Chunk / Chunking** — 문서를 작은 조각으로 쪼개는 것. size/overlap이 품질의 절반.
- **Dense vector / Sparse vector** — embedding(dense) vs BM25(sparse).
- **Cosine similarity / Dot product / L2** — 유사도 계산 방식.
- **Top-k retrieval** — 상위 k개 chunk만 가져오기.
- **Hybrid search** — dense + sparse 결합.
- **RRF (Reciprocal Rank Fusion)** — 여러 retrieval 결과의 rank 기반 병합.
- **Reranking** — retrieval 결과를 cross-encoder로 재정렬.
- **Bi-encoder vs Cross-encoder** — 입력 따로 임베딩 vs 같이 임베딩. 후자는 느리지만 정확.
- **HyDE (Hypothetical Doc Embedding)** — 가상의 답변을 만들어 그걸로 검색.
- **Multi-query** — 쿼리를 여러 변형으로 확장 후 병합.
- **Query rewriting** — LLM으로 쿼리 정제.
- **Step-back prompting** — 구체 → 일반화된 쿼리로 후퇴해 검색.
- **Parent document retriever** — 작게 retrieve, 크게 전달.
- **RAG-Fusion** — multi-query + RRF.
- **HNSW / IVF / PQ** — Qdrant 등이 쓰는 근사 최근접 인덱스.
- **Quantization** — vector를 int8/binary로 압축 (Scalar/Binary quantization).
- **MTEB** — embedding 모델 벤치마크.

## Tier B — Agent / Tool
- **Tool definition / schema** — JSON Schema로 함수 시그니처 기술.
- **Parallel tool use** — 한 턴에 여러 tool 동시 호출.
- **tool_choice** — auto / any / specific tool 강제.
- **Agent loop** — call → execute → result → next call 반복.
- **StateGraph (LangGraph)** — 에이전트의 상태머신.
- **Conditional edge** — 상태 기반 분기.
- **Checkpointing** — 에이전트 상태 영속화 (SqliteSaver 등).
- **Human-in-the-loop / Interrupt** — 사람 승인 지점.
- **Reflection / Reflexion** — 출력을 스스로 비평/재작성.
- **Plan-and-Execute** — 계획 먼저, 실행 따로.
- **Multi-agent (supervisor, hierarchical)** — 여러 agent 협업 구조.

## Tier B — Eval
- **Faithfulness** — 답이 주어진 context에 근거하는가.
- **Answer relevancy** — 답이 질문에 답하는가.
- **Context precision** — 가져온 chunk 중 쓸만한 비율.
- **Context recall** — 정답에 필요한 정보를 다 가져왔는가.
- **LLM-as-a-judge** — LLM이 결과를 채점. 편향 주의 (positional/verbosity/self-preference).
- **Golden dataset** — 정답셋. Eval의 기반.
- **Regression test** — prompt/모델 변경이 기존 점수를 떨어뜨리는지.
- **Pairwise comparison** — A/B 중 어느 게 나은지 대결 방식 eval.
- **Reference-based vs Reference-free** — 정답 비교 vs 정답 없이 품질만.

## Tier B — Production
- **Rate limit (RPM / TPM)** — 분당 요청 / 토큰 한도.
- **Exponential backoff + jitter** — 재시도 정책 표준.
- **Prompt caching** — 동일 prefix 재사용으로 토큰 비용 절감. Anthropic `cache_control`, OpenAI implicit, Gemini explicit.
- **TTFT (Time To First Token)** — 스트리밍에서 체감 지연.
- **Tokens/sec** — 생성 속도.
- **Batch API** — 대량 요청을 오프라인 큐로 처리 (50% 비용 절감).
- **Circuit breaker** — 연속 실패 시 호출 차단.
- **Semantic cache** — 의미 유사 쿼리를 캐시 히트로.

## Tier B — Self-hosting
- **GGUF** — llama.cpp의 양자화 포맷.
- **Quantization (Q4_K_M / Q8_0 / FP8 / INT4)** — 메모리/품질 트레이드오프.
- **PagedAttention** — vLLM의 핵심. KV cache를 페이지 단위로 관리.
- **Continuous batching** — 요청을 도착 순으로 즉시 묶기.
- **KV cache** — attention의 key/value를 재계산 안 하게 캐싱.
- **Tensor / Pipeline / Data parallel** — 대형 모델 분산 추론.
- **Cold start / Scale to zero** — Serverless GPU의 특성.
- **OpenAI-compatible endpoint** — 거의 모든 오픈소스 서버가 제공. SDK base_url만 바꾸면 됨.

## Tier C — MCP / 프로토콜
- **MCP (Model Context Protocol)** — AI 앱과 외부 시스템을 잇는 오픈 표준.
- **Tools / Resources / Prompts / Sampling** — MCP의 **4가지 primitives**.
- **Transport (stdio / SSE / HTTP)** — 통신 방식.
- **Client / Server / Host** — 각각 LLM 앱 / tool 노출 측 / 앱을 돌리는 플랫폼 (Claude Desktop, Cursor).
- **Sampling** — 서버가 호스트의 LLM을 역호출.
- **Roots / Capabilities** — 접근 범위와 기능 협상.

## Tier C — Fine-tuning (나중에)
- **SFT (Supervised Fine-Tuning)** — 프롬프트/응답 쌍으로 학습.
- **LoRA / QLoRA** — 적은 파라미터만 학습 (PEFT).
- **DPO / PPO / RLHF** — 선호 정렬.
- **Distillation** — 큰 모델 → 작은 모델 지식 전이.

---

## 업데이트 규칙
- 학습 중 새 용어 만나면 즉시 이 파일에 추가
- 정의는 **한 줄**로. 길어지면 안 이해한 것.
- 여러 번 혼동되는 건 앞에 ⚠️ 마크

## 자주 혼동되는 쌍 ⚠️
- **Function calling (OpenAI 용어) ↔ Tool use (Anthropic 용어)** — 같은 개념.
- **Embedding model ↔ Generation model** — 용도 다름. 임베딩은 벡터 출력, 생성은 텍스트 출력.
- **Dense ↔ Sparse vector** — 의미 기반 vs 단어 기반.
- **RAG ↔ Fine-tuning** — 외부 지식 주입 vs 모델 가중치 변경. RAG가 먼저.
- **Bi-encoder ↔ Cross-encoder** — 빠름/덜 정확 vs 느림/정확. 2단계 조합이 표준.
- **Workflow ↔ Agent (Anthropic)** — 고정 경로 vs 동적. 기본은 workflow.
- **Chat Completions ↔ Responses API (OpenAI)** — 레거시 vs 신규. 신규 코드는 Responses.
- **JSON mode ↔ Structured Outputs (strict)** — JSON 형식만 보장 vs 스키마까지 보장.
- **stdio ↔ Streamable HTTP (MCP)** — 로컬 subprocess vs 원격/멀티클라이언트.
- **Implicit (OpenAI) ↔ Explicit (Anthropic/Gemini) prompt caching** — 자동 vs 수동 `cache_control`.
- **GGUF ↔ AWQ/GPTQ** — CPU/범용 양자화 vs GPU 중심 weight-only quantization.
- **Pod ↔ Serverless (RunPod)** — persistent VM vs event-driven scale-to-zero.
- **TTFT ↔ E2E latency** — 첫 토큰 지연 vs 완료까지 지연. 스트리밍에선 TTFT가 UX.

## v2 추가 키워드 (난이도 상향 반영)

### Day 1-3
- Chars-per-Token (CPT, 토큰 효율), Lost in the Middle, logprob entropy, nucleus sampling
- Self-Consistency (N-sampling + 다수결), Chain-of-Density, Step-back prompting
- Prompt injection 4 vectors (direct/indirect/payload splitting/encoded), sandwich defense, canary token, Prompt-Guard
- Anthropic Interactive Tutorial 9 chapters

### Day 4-5
- Pydantic v2 (`model_validate_json`, `RootModel`, `discriminator`)
- JSON Schema Draft 2020-12, `$ref`, `$defs`, `additionalProperties: false`
- Instructor `Partial[T]` / `Iterable[T]` / `Maybe[T]`, Outlines grammar-constrained decoding
- Extended thinking + tool use (Claude 4.x)
- Built-in tools (OpenAI web_search / file_search / code_interpreter)
- asteval (safe expression parser), Docker/firejail sandbox
- Recursion limit, token budget enforcement

### Day 6-8
- Matryoshka Representation Learning (MRL)
- Task-specific embeddings (retrieval_query / retrieval_document / STS)
- E5 prefix convention (`query:` / `passage:`)
- BGE-M3 (dense + sparse + colbert 3-output)
- HNSW `m` / `ef_construct` / `ef`, on-disk mode
- Scalar / Binary / Product Quantization, recall-latency trade
- Anthropic Contextual Retrieval (49% 개선)
- RAPTOR (recursive abstraction tree), ColBERT late interaction
- Corrective RAG (CRAG), Self-RAG (adaptive retrieval)
- RRF formula `1/(k+rank)`, k=60

### Day 9
- Noise Sensitivity, Answer Correctness, reference-free vs reference-based
- Pairwise comparison (Elo), inter-rater agreement (Kappa)
- CI gate, threshold, Pareto frontier (cost vs quality)
- Golden dataset categories (factual / synthesis / unanswerable / adversarial)

### Day 10
- LangGraph `StateGraph`, `conditional_edges`, `add_messages` reducer
- Checkpointing (SqliteSaver / PostgresSaver), thread_id
- `interrupt_before` / `interrupt_after` (HITL)
- Streaming modes (values / updates / messages / debug)
- Agent vs Workflow (Anthropic blog)
- Pydantic AI, smolagents, CrewAI

### Day 11
- MCP primitives: Tools / Resources / Prompts / Sampling
- JSON-RPC 2.0, `initialize` handshake, capability negotiation
- stdio / Streamable HTTP / SSE transports
- Host / Client / Server 역할 분리
- Roots (sandbox), consent prompts
- FastMCP, MCP Inspector

### Day 12
- OpenTelemetry GenAI semantic conventions
- Anthropic `cache_creation_input_tokens` / `cache_read_input_tokens`
- OpenAI `usage.prompt_tokens_details.cached_tokens`
- Gemini `client.caches.create()` (32k+ 최소 prefix)
- tenacity `wait_random_exponential`, `retry_if_exception_type`
- aiolimiter, pybreaker 3상태
- Batch API (50% 할인, 24h SLA)

### Day 13
- PagedAttention, continuous batching, speculative decoding
- AWQ / GPTQ (4-bit GPU), GGUF Q-levels
- Ollama base_url trick, OpenAI-compatible endpoint
- RunPod Pod / Serverless, worker-vllm template, cold start
- MLX (Apple Silicon native)

## v3 ULTRA 추가 키워드

### Day 1-3 (v3)
- Scaling Law, Chinchilla optimal (20 tokens/parameter)
- Attention head count, d_model, d_ff
- OWASP LLM Top 10 v2.0 (2025)
- Prompt-Guard 2 86M (INJECTION/JAILBREAK/BENIGN)
- Lakera Playbook attack catalog

### Day 7 (v3)
- Multi-modal RAG, Vision fallback
- PDF → PNG 렌더 (pdf2image), Vision API chunk
- Confidence-based fallback triggering

### Day 9 (v3)
- Supervisor pattern, Hierarchical / Swarm / Network agent topologies
- CrewAI Process (sequential/hierarchical)
- OpenAI Swarm handoff
- Cohen's Kappa (inter-rater agreement)
- Elo rating, pairwise comparison

### Day 10 (v3)
- Whisper WER, Realtime API
- Voice agent full-duplex
- Gemini Live API

### Day 11 (v3)
- Batch API 50% 할인 (OpenAI/Anthropic/Gemini)
- 24h SLA, custom_id
- Guardrails AI validators (RAIL spec)
- NeMo Colang (dialogue flow)
- LlamaFirewall (Meta 통합 방어)

### Day 12 (v3)
- Modal serverless (decorator 기반)
- Fly.io (Docker + region)
- Docker multi-stage (builder + runtime)
- K8s: Deployment/Service/ConfigMap/Secret/HPA
- k3d (로컬 K8s)

### Day 13 (v3)
- LoRA (Hu 2021): rank decomposition, ΔW = BA
- QLoRA (Dettmers 2023): 4-bit NF4, Double Quantization, Paged Optimizers
- DPO (Rafailov 2023): preference pairs, beta, PPO 대체
- Unsloth 2-5x 가속
- TRL SFTTrainer / DPOTrainer
- Chat template alignment
- Adapter merge / GGUF export

### Day 14 (v3 Advanced)
- Mixture of Experts (MoE): sparse expert routing, Mixtral 8x7B
- Speculative Decoding: draft + target, Medusa
- FlashAttention: IO-aware tiling, HBM read/write 급감
- Distilling Step-by-Step: Rationale distillation
- Data / Tensor / Pipeline Parallel: DDP / FSDP / Megatron / GPipe
- Ring Attention: ring passing for 1M+ context
- KV cache compression, InfiniAttention
