# ⏰ 14일 이후 확장 트랙

부트캠프 끝나고 보강할 주제. 실무 진입 전 2-4주간 소화. `curriculum/extras.md`와 교차.

## 우선순위 A — 2주 끝나자마자 (반드시)

### A1. Security / Prompt Injection 방어
- [OWASP LLM Top 10 v2.0 (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — 업데이트판
- [Anthropic — Mitigate jailbreaks](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
- [Lakera — Prompt Injection Playbook](https://www.lakera.ai/blog/guide-to-prompt-injection)
- **실습**: Day 14 포트폴리오에 canary token + input sanitizer + tool allowlist 추가

### A2. Guardrails
- [Guardrails AI](https://www.guardrailsai.com/docs)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [LlamaFirewall (Meta)](https://github.com/facebookresearch/llamafirewall)
- [Llama Prompt Guard 2](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M)
- **실습**: output validation 파이프라인 (PII + 해로운 컨텐츠)

### A3. Deployment
- [FastAPI SSE + async](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- [Modal docs](https://modal.com/docs)
- [Fly.io](https://fly.io/docs/)
- [Docker multi-stage Python](https://docs.docker.com/language/python/containerize/)
- **실습**: Day 14 포트폴리오를 Modal 또는 Fly.io 배포

### A4. Batch API (50% 비용 절감)
- [OpenAI Batch](https://platform.openai.com/docs/guides/batch)
- [Anthropic Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing)
- [Gemini Batch mode](https://ai.google.dev/gemini-api/docs/batch-mode)

## 우선순위 B — 특정 니즈 생기면

### B1. Fine-tuning
- [OpenAI Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)
- [HF PEFT](https://huggingface.co/docs/peft/index) — LoRA/QLoRA
- [HF TRL](https://huggingface.co/docs/trl/index) — SFT/DPO/PPO
- [Axolotl](https://github.com/axolotl-ai-cloud/axolotl)
- [Unsloth](https://docs.unsloth.ai/) — 2-5x 빠른 LoRA
- 비용: RunPod H100 1h ~$3-5. 7B QLoRA 1 epoch ≈ 몇 시간

### B2. Multi-modal
- [OpenAI Vision](https://platform.openai.com/docs/guides/vision)
- [Anthropic Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision)
- [Gemini multimodal](https://ai.google.dev/gemini-api/docs/vision) — 2026 현재 최강
- [Gemini Live API (audio)](https://ai.google.dev/gemini-api/docs/live)
- [Google multimodal RAG codelab](https://codelabs.developers.google.com/multimodal-rag-gemini)

### B3. Semantic Cache
- [GPTCache](https://github.com/zilliztech/GPTCache)
- [LangChain — LLM caching](https://python.langchain.com/docs/integrations/llm_caching/)

### B4. Advanced Agents
- [CrewAI docs](https://docs.crewai.com/)
- [Pydantic AI](https://ai.pydantic.dev/)
- [smolagents (HF)](https://github.com/huggingface/smolagents)
- [OpenAI Swarm (experimental)](https://github.com/openai/swarm)
- [LangGraph Supervisor pattern](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)

### B5. Vector DB 교체
- [Weaviate](https://docs.weaviate.io/weaviate)
- [Pinecone](https://docs.pinecone.io/)
- [pgvector](https://github.com/pgvector/pgvector) + [Supabase AI](https://supabase.com/docs/guides/ai)
- [Milvus](https://milvus.io/docs)

### B6. 논문 정독
Figure + Abstract + Conclusion.
- Attention Is All You Need / RAG / CoT / ReAct / ToT / Reflexion / Chinchilla / Lost in Middle / vLLM PagedAttention / RAPTOR / Self-RAG / DPO / Constitutional AI

## 우선순위 C — 언젠가

- RLHF / DPO / PPO / KTO (alignment)
- MoE (GPT-4 / Mixtral / DeepSeek 내부)
- Speculative decoding
- Embedding quantization (binary / int8)
- KV cache 최적화 (InfiniAttention / Ring)
- Long-context (1M+)
- Distillation

## 📼 확장 YouTube

- [LLM Zoomcamp playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIoBpuc900htYF4uhEAbaT-)
- [RAG From Scratch playlist](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x)
- [DeepLearning.AI YouTube](https://www.youtube.com/@Deeplearningai) + [Short Courses](https://www.deeplearning.ai/short-courses/)
- [LangChain YouTube](https://www.youtube.com/@LangChain) + [Academy](https://academy.langchain.com/)
- [HuggingFace](https://www.youtube.com/@HuggingFace) + [Learn](https://huggingface.co/learn)
- [OpenAI Devs](https://www.youtube.com/@OpenAIDevs)
- [Anthropic](https://www.youtube.com/@anthropic-ai)

## 🗺 1개월 학습 순서

- **Week 1**: A1 Security + A2 Guardrails + A3 Deploy
- **Week 2**: A4 Batch + B2 Multi-modal + B3 Semantic Cache
- **Week 3-4**: 선택 (B1 Fine-tuning 또는 B4 Multi-agent 또는 B5 Vector DB)
