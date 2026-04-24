# 14일 ULTRA 하드코어 LLM 엔지니어링 로드맵 (v3)

> **하루 12-14h × 14일 = ~170h.**
> v2(10h × 14) 대비 **20-40% 시간 증량 + 영역 7개 추가** — Fine-tuning/Vision/Voice/Guardrails/Deploy/Multi-agent/Advanced Topics/Distributed.
>
> ⚠️ **전제**: 8년차 소프트웨어 엔지니어. 풀 몰입 가능. 2주간 타 업무/연락 차단. 수면 7h+ 고수. 주말 풀가동.

## 전체 로드맵 — v3 한눈에

| Day | 주제 | 핵심 산출물 | 시간 | 난이도 |
|---|---|---|---|---|
| 1 | LLM 기초 + Tokenizer + **Attention/Chinchilla 논문** | tokens/temperature/logprobs + 논문 요약 2편 | 12h | ★★★ |
| 2 | 3대 Provider API + Streaming + **Prompt Caching 선행** | Provider 추상화 + 3사 caching 실측 | 12h | ★★★ |
| 3 | Prompt Engineering + **Injection Lab + OWASP LLM Top 10 + Prompt-Guard** | 12 패턴 × 3 태스크 + 공격/방어 + Llama Prompt-Guard 2 로컬 | 12h | ★★★★★ |
| 4 | Structured Output (Pydantic strict) | 3 도메인 × 3 provider × F1 | 12h | ★★★★ |
| 5 | Function/Tool Use + 방어적 agent loop | 15 시나리오 safety rails 통과 | 12h | ★★★★ |
| 6 | Embedding + Qdrant + **ColBERT + BGE-M3 deep** | 5 모델 × HNSW sweep × quantization | 12h | ★★★★ |
| 7 | RAG 기본 + **Vision/Multi-modal RAG** | 3 프레임워크 + 표/이미지 포함 RAG | 12h | ★★★★★ |
| 8 | 고급 RAG + **Lost in Middle + RAPTOR + ColBERT papers** | 6 pipeline + contextual retrieval + papers | 12h | ★★★★★ |
| 9 | Eval + **Multi-agent (Supervisor/CrewAI/Swarm) + ReAct/Reflexion/ToT papers** | Ragas 매트릭스 + 3 agent 프레임 비교 | 12h | ★★★★★ |
| 10 | LangGraph Agent + **Voice 입력 (Whisper + Realtime API)** | state machine + reflection + 음성→RAG | 12h | ★★★★★ |
| 11 | MCP + **Batch API + Guardrails 풀스택 (OWASP production / NeMo / LlamaFirewall)** | MCP 서버 + 3사 batch + 방어 3겹 | 12h | ★★★★★ |
| 12 | Observability + Production + **Deployment (Modal/Fly.io/Docker/K8s basics)** | Langfuse + Modal 배포 + K8s manifest | 12h | ★★★★★ |
| 13 | Local LLM + **Fine-tuning 전일 (LoRA/QLoRA/DPO with Unsloth on RunPod GPU)** | qwen3-8B LoRA → DPO → RunPod serving | 14h | ★★★★★★ |
| 14 | **Mega Portfolio + Advanced Topics Rapid Fire** (MoE/Speculative/FlashAttention/Distillation/분산 훈련 개념 + 논문 5편) | GitHub 공개 + 모든 통합 + 회고 | 14h | ★★★★★★ |

총 **168-172h**. 잠 자는 시간 제외 진행.

## 📚 논문 스케줄 (Figure + Abstract 중심, Claude 요약 병행)

- Day 1: **Attention Is All You Need** / **Chinchilla**
- Day 2: **RAG (Lewis 2020)**
- Day 3: **CoT (Wei 2022)** / **Self-Consistency (Wang 2022)**
- Day 5: **PagedAttention / vLLM** / **Matryoshka**
- Day 7: **Lost in the Middle (Liu 2023)** / **Vision RAG (Google Codelab paper)**
- Day 8: **RAPTOR** / **ColBERT / ColBERTv2** / **Anthropic Contextual Retrieval 블로그**
- Day 9: **ReAct** / **Reflexion** / **Tree of Thoughts** / **Judging LLM-as-a-Judge**
- Day 11: **OWASP LLM Top 10 v2.0**
- Day 13: **LoRA (Hu 2021)** / **QLoRA (Dettmers 2023)** / **DPO (Rafailov 2023)** / **Constitutional AI**
- Day 14 Rapid Fire: **Mixtral / MoE** / **Medusa (Speculative)** / **FlashAttention (Dao 2022)** / **Distilling Step-by-Step** / **Ring Attention**

총 **25편** (깊이 차등). 하루 1-5편 배치. Claude로 Figure + Abstract + Conclusion 요약 + 본인이 핵심 3줄.

## 📅 Week 1 (Day 1–7) — Foundation + RAG + Vision

**목표**: LLM 전 스택 기초 + RAG 풀스택 + Multi-modal 맛보기.

- [ ] Transformer/Attention/Sampling + Attention/Chinchilla Figure 레벨
- [ ] 3사 API + Streaming + Caching 실측 체감
- [ ] Prompt 10+ 패턴 + Injection 4공격 × 3방어 + **Prompt-Guard 로컬 실행**
- [ ] Pydantic v2 strict + 3사 schema 강제 + F1 측정
- [ ] Tool use + safety rails 4-layer + parallel
- [ ] 5 embedding 모델 × HNSW/quantization 수치
- [ ] Hybrid + Rerank + Contextual Retrieval
- [ ] **Vision RAG** — 표/차트/스캔 PDF 처리
- [ ] **Voice input** 맛보기 (Whisper)

## 📅 Week 2 (Day 8–14) — Production + Multi-Agent + Fine-tune + 고급

**목표**: Eval 기반 의사결정 + 배포 + Fine-tuning + 고급 개념 + 완성된 포트폴리오.

- [ ] Ragas 4 metric + judge bias + CI gate
- [ ] LangGraph + **Multi-agent (Supervisor/CrewAI/Swarm)**
- [ ] MCP 4 primitives + 3 호스트 등록
- [ ] **Batch API 3사** 비용 절감 실측 (50%)
- [ ] **Guardrails 3겹** (Prompt-Guard + NeMo + LlamaFirewall)
- [ ] Langfuse trace + Prompt versioning
- [ ] **Deployment**: Modal / Fly.io / Docker / K8s manifest
- [ ] Local LLM (Ollama + vLLM)
- [ ] **Fine-tuning**: LoRA/QLoRA/DPO with Unsloth on RunPod H100
- [ ] **Advanced**: MoE / Speculative / FlashAttention / Distillation / 분산 훈련 개념
- [ ] Portfolio: **Vision + Voice + Multi-agent + Fine-tuned model + Deployed** 전부 통합

## ⏱ 하루 시간 배분 (12-14h 기준)

| 블록 | 시간 | 용도 |
|---|---|---|
| 07:30-08:00 | 웜업 | 어제 회고 + 오늘 주제 훑기 |
| 08:00-10:30 | 읽기 (read-only) | 공식 docs + 논문 Figure |
| 10:30-12:30 | 튜토리얼 실행 | Jupyter / Colab notebook 따라치기 |
| 12:30-13:15 | 점심 (산책) | 화면 밖 |
| 13:15-17:00 | 본 실습 | 프로젝트 디렉토리 변형 과제 |
| 17:00-17:30 | 쉬는 시간 | 운동/산책 |
| 17:30-20:00 | 디버깅 + stretch | 막힌 것 + 고급 과제 |
| 20:00-20:45 | 저녁 | — |
| 20:45-22:30 | 정리 + 논문 요약 | keywords / concepts / 논문 bullet |
| 22:30-23:00 | 회고 | daily-log + commit |

**Day 13, 14는 +2h** (fine-tuning 컴파일/훈련 대기, portfolio 통합 작업).

## 🔥 핵심 원칙 (v3 강화)

1. **공식 문서 + 논문 Figure 우선** — 한국어 블로그 금지
2. **튜토리얼 딱 1번** — 두 번째는 반드시 변형
3. **Eval 수치로만** — "체감" 금지. Ragas + custom judge로
4. **Prompt caching + Batch API** — 비용 가드레일. 실수로 $수백 터지는 것 방지
5. **Fine-tuning 결과 = Ragas 개선 증명 필수** — "돌려봄"으로 끝내지 마
6. **GPU 시간 예산**: RunPod $20 상한 (H100 기준 4-5시간). 초과 시 실험 중단
7. **논문 Figure 수준 읽기** — 본문 통독 금지. Abstract + Figure + Conclusion + Claude 요약
8. **모델 선택**:
   - Day 1-3: Haiku / 4o-mini / Flash (빠른 실험)
   - Day 4-9: Sonnet / 4o / Pro (품질)
   - Day 10-14: 상황별 + Fine-tuned local model
9. **일일 회고 필수** — 건너뛰면 Day N+1 방향 흔들림
10. **토/일 풀가동** — "주말 쉬기" 금지. 14일 완주의 전제

## 🚨 중단/뒤처짐 대응 (v3)

v3는 v2보다 **밀도 40% 높음** → 뒤처지기 쉬움. 대응:

- **1일 뒤처짐**: Stretch 버리고 필수만
- **2일 뒤처짐**: 영역별 "건너뛰기 우선순위" 적용:
  1. 먼저 버림: 논문 Figure 읽기 → Claude 요약만 믿기
  2. 다음: Vision/Voice 맛보기 축소 → 설명만
  3. 다음: Multi-agent → 하나만 (Supervisor)
  4. 다음: Advanced topics → 개념 3개만 (MoE/Speculative/FlashAttention)
- **3일 이상 뒤처짐**: [`recovery-playbook.md`](recovery-playbook.md) B/C 모드 + v2로 회귀 선언
- **번아웃**: 하루 통째 쉬기 > 무리해서 완주 시도

## 💰 예산 (v3)

| 항목 | 예상 |
|---|---|
| OpenAI | $15-25 |
| Anthropic (caching 적용) | $10-20 |
| Gemini | $0-5 |
| RunPod Serverless 테스트 (Day 11-13) | $5-10 |
| **RunPod GPU Fine-tuning** (Day 13 H100 4-5h) | $15-25 |
| **Modal / Fly.io deploy** (Day 12) | $0-5 (free tier) |
| **합계** | **$45-90** |

v2보다 **$20-50 더** (fine-tuning GPU 때문).

## 📌 v2 → v3 변화 요약

| 영역 | v2 | v3 |
|---|---|---|
| 하루 시간 | 10h | **12-14h** |
| 총 시간 | ~140h | **~170h** |
| Day 7 | Basic RAG | Basic RAG + **Vision RAG** |
| Day 10 | Agent | Agent + **Voice + 논문 4편** |
| Day 11 | MCP | MCP + **Batch API + Guardrails 풀스택** |
| Day 12 | Observability | Observability + **Deployment (Modal/Fly/K8s)** |
| Day 13 | Local LLM | Local LLM + **Fine-tuning 전일** |
| Day 14 | Portfolio | Portfolio + **Advanced Topics Rapid Fire** |
| 논문 | 2-3편 (이름만) | **25편** (Figure 수준) |
| 고급 주제 | extras.md 위탁 | **Day 14 전반부 통합** |
| Fine-tuning | extras B1 | **Day 13 전일** |
| Deploy | extras A3 | **Day 12 섹션** |
| Security | extras A1-A2 | **Day 3 + Day 11 통합** |
| Multi-modal | extras B2 | **Day 7 + Day 10 분산** |
| Multi-agent | extras B4 | **Day 9 섹션** |
| 분산 훈련 | extras C | **Day 14 개념** |

## 🎯 최종 산출물 (v3)

**"Devlog RAG Copilot ULTRA"** — Day 14까지:
- GitHub 공개 repo (MIT)
- docker-compose 원클릭
- **Fine-tuned 내 도메인 LoRA 모델** (RunPod 서빙)
- **Vision RAG** (표/차트/스캔 PDF)
- **Voice input** (Whisper)
- **Multi-agent** (Supervisor + 2-3 workers)
- **Guardrails 3겹** (Prompt-Guard + canary + classifier)
- **Deployed on Modal or Fly.io** (public URL)
- **Langfuse trace + Ragas CI gate** (threshold 0.85+)
- **K8s manifest** (배포 옵션 증명)
- 아키텍처 다이어그램 + 데모 gif + 회고

## 🎖 Mastery 정의 (정직하게)

v3 완주 = "LLM **풀스택** 엔지니어 진입급". 구체적으로:

- ✅ LLM 전 영역 (RAG/Agent/Eval/Observability/Fine-tune/Deploy) **손으로** 1회 이상
- ✅ 수치 기반 의사결정 습관
- ✅ 논문 25편 Figure 수준 파악
- ✅ GitHub 공개 포트폴리오 + 배포된 URL
- ✅ 면접에서 "이 기능을 왜 이렇게 짰고 수치가 얼마였다" 설명

여전히 **안 되는 것**:
- ❌ LLM 논문 쓸 수준의 학술 깊이
- ❌ 대규모 분산 훈련 직접 운영 (개념만)
- ❌ 모델 아키텍처 연구
- ❌ Multi-billion 서비스 ops

하지만 **LLM 엔지니어 취업 → 3개월 OJT 단축 → 1개월이면 기여** 수준은 충분히 도달.

## 🔗 관련 문서

- [`day00-prep.md`](day00-prep.md) — Day 0 프리컬 (2-4h)
- [`schedule.md`](schedule.md) — 12-14h 일과
- [`self-check.md`](self-check.md) — Day별 자가진단
- [`recovery-playbook.md`](recovery-playbook.md) — 뒤처졌을 때
- [`troubleshooting.md`](troubleshooting.md) — FAQ
- 각 Day별 상세 문서
