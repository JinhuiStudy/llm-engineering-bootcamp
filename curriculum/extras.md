# 14일 이후 확장 트랙 (Post-Bootcamp)

2주 부트캠프에서 의도적으로 뺀 주제. 실무에 들어가기 전에 반드시 건드려야 할 것과, 특정 프로젝트에서만 필요한 것들.

## 우선순위 A — 2주 끝나자마자 해야 함

### A1. Security / Prompt Injection 방어
- [Anthropic — Jailbreaking & prompt injections](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- 실습: Day 14 포트폴리오에 system prompt 누출 방어, tool allow-list, 입력 sanitize 추가
- 키워드: prompt injection (direct/indirect), jailbreak, data exfiltration, tool abuse, sandboxing

### A2. Guardrails
- [Guardrails AI](https://www.guardrailsai.com/docs)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [LlamaFirewall / Llama-Prompt-Guard](https://huggingface.co/meta-llama/Prompt-Guard-86M)
- 실습: output validation 파이프라인 (PII 탐지, 해로운 컨텐츠 필터)

### A3. Deployment / Serving
- [FastAPI + SSE streaming](https://fastapi.tiangolo.com/)
- [Modal](https://modal.com/docs), [Fly.io](https://fly.io/docs/)
- [Docker multi-stage builds for Python]
- 실습: Day 14 포트폴리오를 Fly.io 또는 Modal에 배포

### A4. Batch API (비용 절감 50%)
- [OpenAI Batch API](https://platform.openai.com/docs/guides/batch)
- [Anthropic Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing)
- [Gemini Batch](https://ai.google.dev/gemini-api/docs/batch-mode)
- 실습: 대량 classification/extraction task를 batch로 돌려 비용 비교

## 우선순위 B — 특정 니즈 생기면

### B1. Fine-tuning (section 17의 자료들)
- [OpenAI Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)
- [HF PEFT](https://huggingface.co/docs/peft/index) / [repo](https://github.com/huggingface/peft)
- [HF TRL](https://huggingface.co/docs/trl/index) / [repo](https://github.com/huggingface/trl)
- [Axolotl](https://github.com/axolotl-ai-cloud/axolotl)
- [Unsloth docs](https://docs.unsloth.ai/) / [repo](https://github.com/unslothai/unsloth)
- 언제 하는가: 프롬프트 엔지니어링으로 품질 한계에 부딪혔을 때. RAG로도 못 막는 특정 톤/포맷/도메인 지식이 필요할 때.
- 순서: LoRA → QLoRA (Unsloth) → 필요하면 full fine-tune → RLHF/DPO
- 비용: RunPod H100 1시간 ~$3-5. 7B QLoRA 1 epoch ≈ 몇 시간.

### B2. Multi-modal
- [OpenAI Vision](https://platform.openai.com/docs/guides/vision)
- [Anthropic Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision)
- [Gemini multimodal](https://ai.google.dev/gemini-api/docs/vision)
- [Google multimodal RAG codelab](https://codelabs.developers.google.com/multimodal-rag-gemini)
- [GCP multimodal RAG notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/use-cases/retrieval-augmented-generation/intro_multimodal_rag.ipynb)
- 실습: PDF 안의 표/차트까지 인덱싱하는 RAG

### B3. Semantic Cache / Response Cache
- [GPTCache](https://github.com/zilliztech/GPTCache)
- Redis + embedding 직접 구현
- 실습: 동일 의미 쿼리 hit 시 LLM 호출 없이 즉답

### B4. Advanced Agents
- [CrewAI docs](https://docs.crewai.com/) / [repo](https://github.com/crewAIInc/crewAI)
- [Pydantic AI](https://pydantic.dev/docs/ai/overview/) / [repo](https://github.com/pydantic/pydantic-ai)
- Multi-agent (supervisor / hierarchical / swarm)
- Human-in-the-loop patterns (LangGraph interrupts)

### B5. Vector DB 비교 / 교체
- [Weaviate](https://docs.weaviate.io/weaviate) — 그래프 + 벡터 하이브리드
- [Pinecone](https://docs.pinecone.io/) — 완전 관리형
- [Chroma](https://docs.trychroma.com/) — 단순 임베디드
- [FAISS](https://faiss.ai/) / [repo](https://github.com/facebookresearch/faiss) — 라이브러리 수준
- [pgvector](https://github.com/pgvector/pgvector) / [Supabase AI](https://supabase.com/docs/guides/ai) — Postgres 통합
- 언제 교체: 규모 (100M+ vectors), 관리 부담, 기존 Postgres 있음 등

### B6. 논문 정독 (section 18)
실무에서는 요약만 알아도 되지만 리더 역할 하려면:
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) ([PDF](https://arxiv.org/pdf/1706.03762))
- [RAG (Lewis et al. 2020)](https://arxiv.org/abs/2005.11401) ([NeurIPS PDF](https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf))
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) ([PDF](https://arxiv.org/pdf/2201.11903))
- [ReAct](https://arxiv.org/abs/2210.03629) ([PDF](https://arxiv.org/pdf/2210.03629)) ([Google blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/))
- 방법: Claude한테 요약 시키고 Figure + Abstract + Conclusion만. 본문은 궁금한 섹션만.

## 우선순위 C — 언젠가 필요할 수도

- RLHF / DPO / PPO (alignment)
- Mixture of Experts (MoE) — GPT-4, Mixtral 내부
- Speculative decoding (inference 가속)
- Embedding quantization (binary, int8)
- KV cache management
- MoCoLM, long-context (1M+ tokens) 전략
- Distillation (teacher → student)

## 확장 자료 (section 19 - YouTube 전체)

- [LLM Zoomcamp 전체 playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIoBpuc900htYF4uhEAbaT-)
- [LLM Zoomcamp intro video](https://www.youtube.com/watch?v=FgnelhEJFj0)
- [RAG From Scratch playlist](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x)
- [RAG From Scratch intro](https://www.youtube.com/watch?v=sVcwVQRHIc8)
- [DeepLearning.AI YouTube](https://www.youtube.com/@Deeplearningai) + [Short Courses](https://www.deeplearning.ai/short-courses/)
- [LangChain YouTube](https://www.youtube.com/@LangChain) + [Academy](https://academy.langchain.com/)
- [Hugging Face YouTube](https://www.youtube.com/@HuggingFace) + [Learn](https://huggingface.co/learn)
- [Google Developers YouTube](https://www.youtube.com/@GoogleDevelopers)
- [OpenAI Devs YouTube](https://www.youtube.com/@OpenAIDevs)
- [Anthropic YouTube](https://www.youtube.com/@anthropic-ai)

## 한국어 보조 검색 키워드 (section 20)
막힐 때만 사용. 공식 문서가 1순위.

- LLM RAG 한국어 튜토리얼
- LangChain RAG 한국어
- Qdrant RAG 한국어
- vLLM 한국어 튜토리얼
- Ollama 로컬 LLM 한국어
- LangGraph 한국어
- LLM evaluation 한국어
- RAGAS 한국어
- Langfuse 한국어

한국어 유일 공식 자료:
- [Google ML Crash Course LLM — 한국어 Transformers](https://developers.google.com/machine-learning/crash-course/llm/transformers?hl=ko)
