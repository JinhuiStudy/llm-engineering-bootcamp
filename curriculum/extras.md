# 14일 이후 심화 트랙 (Post-Bootcamp, v3 Updated)

> **v3 ULTRA에서 대부분의 "extras"는 이미 Day 1-14에 내포**되었습니다.
> 이 문서는 **더 깊이 파고들** 주제 + **실무 투입 후 연장**.
>
> 참조: [`resources/later.md`](../resources/later.md)도 중복 — 이 문서가 curriculum 관점, later.md가 resources 관점.

## 📋 v3 ULTRA에 이미 포함된 주제 (중복 확인)

| 영역 | Day | 위치 |
|---|---|---|
| OWASP LLM Top 10 + Prompt-Guard 2 | Day 3 | Prompt Engineering |
| Vision RAG | Day 7 | 기본 RAG 섹션 |
| RAPTOR / ColBERT / Contextual Retrieval | Day 8 | 고급 RAG + 논문 |
| Multi-agent (LangGraph Supervisor / CrewAI / Swarm) | Day 9 | Eval + Multi-agent |
| Voice input (Whisper / Realtime) | Day 10 | LangGraph Agent |
| Batch API 3사 + Guardrails 3겹 (NeMo / LlamaFirewall) | Day 11 | MCP 섹션 |
| Deployment (Modal / Fly.io / Docker / K8s) | Day 12 | Observability 섹션 |
| Fine-tuning (LoRA/QLoRA/DPO Unsloth) | Day 13 | Local LLM + Fine-tuning |
| MoE / Speculative / FlashAttention / Distillation / 분산 | Day 14 | Advanced Topics Rapid Fire |
| 논문 25편 Figure 수준 | Day 1-14 전반 | — |

따라서 이 문서의 주제는 **"더 깊게"**.

---

## 🎯 Day 15-20 (1주 심화)

### 1. 배포된 포트폴리오 유지보수 (3-4일)
- CI/CD 강화: nightly full Ragas eval → Langfuse dashboard에 붙이기
- Semantic cache 추가 (Redis + embedding) — 같은 의미 쿼리는 LLM 호출 없이 답
- User auth + session 추가 (기본 JWT, 선택)
- Multi-user concurrency — FastAPI async + Qdrant에 user_id filter
- Modal autoscale 튜닝 + keep_warm 비용 실측

### 2. Fine-tune 반복 개선 (2-3일)
- Day 13 base LoRA → **DPO 5 iteration** (preference 수집 → 훈련 → 평가 반복)
- Ragas 개선 측정: 5% 이상 올리려면 데이터 quality > quantity
- HF Hub에 모델 push + README 작성 (공개 포트폴리오 확장)
- (선택) **Constitutional AI 스타일** self-refinement

### 3. Observability 프로덕션 레벨
- Langfuse → Clickhouse TTL 설정 (디스크 폭발 방지)
- Prometheus + Grafana로 latency/cost metric 대시보드
- PagerDuty/Slack 알람 (latency p95 > 10s, error rate > 5%)
- Load test (Locust로 100 concurrent user)

---

## 🎯 Day 21-60 (1-2개월)

### A. Fine-tune Depth (선택)
v3 Day 13이 entry point. 심화:
- **Full SFT** (not LoRA) — 7B 전체 weight. H100 2개 필요.
- **Constitutional AI** ([Bai 2022](https://arxiv.org/abs/2212.08073)) — self-critique 기반 alignment
- **KTO / ORPO** — DPO 경쟁. 2024-2026 신 preference 학습
- **Reward model** 학습 → RLHF full pipeline (어려움, 비용 큼)
- **Multi-turn SFT** — 긴 대화 데이터로 tuning
- **Domain embedding 재훈련** — 본인 문서로 embedding 모델도 fine-tune
  - [sentence-transformers — Training Overview](https://www.sbert.net/examples/training/sts/README.html)

### B. 고급 Agent
v3 Day 9-10 확장:
- **Computer Use** (Anthropic) — screenshot + 마우스/키보드 제어
- **Agent Skills** (PowerPoint/Excel/Word/PDF) — Anthropic 공식
- **Swarm with handoff** — OpenAI Swarm의 진짜 사용
- **LangGraph Studio** — visual debugger
- **Graph RAG** — neo4j + entity linking
- [CrewAI deeper](https://docs.crewai.com/) — 역할 기반 복잡 workflow

### C. 고급 RAG
v3 Day 8 확장:
- **CRAG (Corrective RAG)** — web fallback 구현
- **Self-RAG** — 모델이 retrieval 필요 자체 판단
- **GraphRAG (Microsoft)** — Knowledge Graph + community summarization
- **LlamaIndex Ingestion Pipeline** — 복잡 ETL
- Embedding 4-bit quantization (binary 저장, 32x 압축)
- **Matryoshka + quantization** 조합으로 비용 극소화

### D. Multi-modal Depth
v3 Day 7 확장:
- **Image generation** 통합 — DALL-E / Imagen / Flux
- **Video 이해** — Gemini Video
- **Audio full-duplex** — OpenAI Realtime API + WebRTC
- **3D** — BlenderMCP
- **Document AI** — 스캔 PDF, 테이블, diagram 인식

### E. Security / Production Hardening
v3 Day 3/11 확장:
- **OWASP LLM Top 10 v2.0** 전 항목 대응 구현
- **Guardrails AI validator** 15개+ 커스텀
- **LlamaFirewall** 전체 스택 (input/output/tool_use)
- **Data poisoning 방어** — training set / vector DB 무결성
- **Red team 실습** — 자체 앱 공격 → 방어
- **Audit log + GDPR** 준수

### F. 인프라 / 대규모
- **vLLM 상세 튜닝** — speculative decoding / CUDA graphs / tensor parallel
- **vLLM on Kubernetes** (KServe)
- **Multi-region deployment** — Cloudflare Workers AI
- **Edge inference** — Ollama on Raspberry Pi 5
- **Dedicated GPU** vs Serverless 비용 분석 (월 트래픽 기반)

### G. 연구 / 논문
**Day 14에 Figure만 본** 25편을 **본문까지**:
- 각 논문 1주에 1편, 6개월에 25편
- 실제 코드 reproduce 2-3편 (예: LoRA, FlashAttention)
- 자체 ablation 1회 (예: RAG 기법 조합 비교)
- (선택) arXiv에 blog-post 스타일 정리 글

---

## 🎯 Day 60-180 (3-6개월)

### 실무 진입 옵션

**Option 1: 취업 (LLM Engineer)**
- 포트폴리오 완성도 ↑ — README / demo / 배포 URL 다 있음
- LinkedIn 업데이트 + 프로젝트 detailed
- 모의 인터뷰 — 시스템 디자인 (RAG 설계 / Agent 설계 / 비용 최적화)
- 기술 블로그 1-2편 (본인 프로젝트 lessons learned)

**Option 2: 창업 / 프로덕트**
- 본인 도메인 특화 → MVP 런치
- Growth: HN Show / Product Hunt / 트위터
- 초기 유저 10명 → 피드백 → 반복

**Option 3: 연구 / 오픈소스**
- arxiv + 커뮤니티 기여 (LangChain / Unsloth / MCP servers / Ragas 등)
- HF Hub에 본인 fine-tuned 모델 + 데이터셋
- (선택) 석사 / PhD

---

## 📚 6개월 독서 목록 (선택)

v3 Day 1-14의 Figure 레벨 이상 심화:

### 책
- [Designing ML Systems (Chip Huyen)](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)
- [Building ML Powered Applications (Emmanuel Ameisen)](https://www.oreilly.com/library/view/building-machine-learning/9781492045106/)
- [AI Engineering (Chip Huyen, 2025)](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) — LLM 특화

### 지속 팔로우
- [Simon Willison's blog](https://simonwillison.net/tags/llms/) — 매주
- [Sebastian Raschka Magazine](https://magazine.sebastianraschka.com/) — 매달
- [The Batch (deeplearning.ai)](https://www.deeplearning.ai/the-batch/) — 매주
- [Eugene Yan](https://eugeneyan.com/writing/) — 실무 관점
- [Lilian Weng](https://lilianweng.github.io/) — 고품질 survey

---

## 한국어 보조 (막힐 때만)

- 한국어 검색 키워드: "LangGraph 한국어 튜토리얼" / "vLLM RunPod 한국어" / "Langfuse 설치 한국어" / "Unsloth LoRA 한국어"
- [Google ML Crash Course LLM — 한국어 Transformers](https://developers.google.com/machine-learning/crash-course/llm/transformers?hl=ko)

**공식 문서가 1순위**. 한국어 자료는 outdated 자주.
