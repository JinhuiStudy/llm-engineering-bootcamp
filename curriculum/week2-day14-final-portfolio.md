# Day 14 — Mega Portfolio + Advanced Topics Rapid Fire (ULTRA — 14h 극한)

> **난이도**: ★★★★★★ (최고)
> **총량**: 14h. 밤 넘어가지 말고 **자정 전 공개** 목표.
> **철학**: 14일간 배운 **모든 것**을 하나에 통합 + 업계 최신 개념 5-6개 rapid fire + 세상에 던지기.

## 🎯 오늘 끝에

1. **GitHub 공개** repo — MIT, docker-compose 원클릭, 배포된 public URL
2. **Mega Portfolio**: Vision + Voice + Multi-agent + Fine-tuned + Guardrails + Deployed 통합
3. **Advanced Topics rapid fire 6개 개념** 설명 가능 (MoE / Speculative / FlashAttention / Distillation / 분산 / Long-context)
4. **논문 5편 Figure 수준** 추가 (Mixtral / Medusa / FlashAttention / DiStilling Step-by-Step / Ring Attention)
5. **회고** + 다음 2주 플랜

## ⏱ 14시간 타임박스

| 시간 | 블록 | 작업 |
|---|---|---|
| 07:00-09:00 | Advanced Topics rapid fire (2h) | 6개 개념 + 논문 5편 Figure |
| 09:00-12:00 | Portfolio 스켈레톤 + 재활용 집계 (3h) | grep으로 재활용 파일 선별 + 구조 세팅 |
| 12:00-12:45 | 점심 | — |
| 12:45-16:00 | Core 통합 (3.25h) | FastAPI + LangGraph agent + RAG pipeline + MCP + Langfuse |
| 16:00-18:00 | Multi-modal + Fine-tune + Deploy (2h) | Vision 모듈 + Fine-tuned LoRA 연결 + Modal 배포 |
| 18:00-18:30 | 휴식 | 필수 |
| 18:30-20:30 | Eval + Guardrails 마무리 (2h) | Ragas 통과 + Guardrails 3겹 연결 |
| 20:30-21:00 | 저녁 | — |
| 21:00-23:00 | README + demo + 공개 (2h) | diagram + gif + threshold 표 + GitHub push |
| 23:00-00:00 | 회고 + commit final (1h) | retrospective.md + Day 15+ 플랜 |

## 🚀 Part 1 — Advanced Topics Rapid Fire (2h, 오전)

### ⚡ 6개 개념 × 20분씩

각 개념당 **"한 줄 정의 + 그림 1개 + 본인 언어 설명 3줄 + 언제 실무에 쓰는가"** → `notes/concepts.md`

#### 1. Mixture of Experts (MoE)
- 🔗 [Mixtral paper (Jiang 2024)](https://arxiv.org/abs/2401.04088) · Figure 1-2
- 🧠 **요지**: Transformer MLP 층을 N개 "전문가" sparse 활성화. Mixtral 8x7B = 8 전문가 중 2개만 활성 → 13B inference cost로 47B 파라미터 효과
- 🛠 **실무**: 자체 훈련 아님. **"왜 DeepSeek-V3/Mixtral inference가 빠른지" 이해**. Day 13 RunPod 선택 시 영향

#### 2. Speculative Decoding
- 🔗 [Medusa paper (Cai 2024)](https://arxiv.org/abs/2401.10774) · Figure 2
- 🧠 **요지**: 작은 draft 모델이 N 토큰 예측 → big target 모델이 검증. 맞으면 한 번에 N 토큰 accept. 2-3x 가속
- 🛠 **실무**: vLLM `--speculative-model` 옵션. 서빙 throughput 개선. 오늘 포트폴리오 Deploy 단에서 활성화 가능

#### 3. FlashAttention
- 🔗 [FlashAttention paper (Dao 2022)](https://arxiv.org/abs/2205.14135) · Figure 1
- 🧠 **요지**: Attention 계산을 **tiling + IO-aware**로 재구성. HBM read/write 급감. 2-4x 빠르고 memory O(n²) → O(n)
- 🛠 **실무**: PyTorch 2.0+ SDPA에 내장. **그냥 켜는 것만으로** 훈련/추론 가속. `torch.nn.functional.scaled_dot_product_attention`

#### 4. Distillation (Distilling Step-by-Step)
- 🔗 [Hsieh 2023](https://arxiv.org/abs/2305.02301) · Figure 1
- 🧠 **요지**: 큰 모델의 **rationale**(reasoning)까지 작은 모델에 전이. Task + Rationale 두 head. 770M 모델이 540B LLM 이김
- 🛠 **실무**: 본인 Fine-tune 파이프라인에 "CoT trace 같이 학습" 추가 가능. Day 13 SFT 데이터에 reasoning 포함

#### 5. Distributed Training (Data / Tensor / Pipeline Parallel)
- 🔗 [GPipe (Huang 2018)](https://arxiv.org/abs/1811.06965) + [Megatron (Shoeybi 2019)](https://arxiv.org/abs/1909.08053) · Figure 각각
- 🧠 **요지**:
  - **Data Parallel**: 배치를 GPU마다 나눠 → all-reduce로 gradient 동기화 (DDP/FSDP)
  - **Tensor Parallel**: 한 레이어의 가중치를 GPU마다 나눔 (Megatron-style)
  - **Pipeline Parallel**: 레이어들을 GPU stage로 나눔 → micro-batch로 pipeline
- 🛠 **실무**: 7B 이하는 DDP만. 70B+는 FSDP or DeepSpeed ZeRO-3. 직접 운영 안 해도 "**왜 70B 서빙이 어려운지**" 이해

#### 6. Ring Attention / Long-context
- 🔗 [Ring Attention (Liu 2023)](https://arxiv.org/abs/2310.01889) · Figure 1
- 🧠 **요지**: Attention을 GPU들 간 ring으로 전달하며 계산 → context 1M+ 가능. Gemini 1M context의 배경
- 🛠 **실무**: 서빙에선 요즘 Gemini / Claude / GPT가 알아서 처리. 본인이 구현할 일 거의 없음. **"왜 1M context가 가능한지" 이해만**

### ⚡ 논문 5편 Figure 수준 (30-40분)

Claude로 한 번에 요약:
```
Summarize these papers in bullets. 3 bullets per paper:
1. Mixtral (arxiv 2401.04088)
2. Medusa (arxiv 2401.10774)
3. FlashAttention (arxiv 2205.14135)
4. Distilling Step-by-Step (arxiv 2305.02301)
5. Ring Attention (arxiv 2310.01889)
```

그 후 본인이 **각 논문 Figure 1을 직접 봄** + `notes/concepts.md`에 3줄 씩.

## 🧩 Part 2 — Mega Portfolio 통합 (9h 본 실습)

### 🎬 "Devlog RAG Copilot ULTRA" 최종 스펙

```
╔═══════════════════════════════════════════════════════════════════╗
║  사용자                                                             ║
║     │                                                                ║
║     ├── Web UI (Streamlit) + 🎤 Voice input (Whisper)               ║
║     └── Claude Desktop (MCP server)                                  ║
║                                                                      ║
║     ↓                                                                ║
║  [Guardrails 3겹] Prompt-Guard → Guardrails AI → NeMo Colang        ║
║     ↓                                                                ║
║  FastAPI (/chat SSE, /ingest)                                        ║
║     ↓                                                                ║
║  LangGraph Multi-Agent State Machine                                 ║
║     ├── Supervisor agent                                             ║
║     ├── Researcher (RAG + Vision)                                    ║
║     ├── Writer (draft + citations)                                   ║
║     └── Critic (Ragas-style self-check)                              ║
║     ↓                                                                ║
║  RAG: Hybrid (dense+BM25+RRF) → Rerank → Contextual Retrieval        ║
║     ↓                                                                ║
║  Qdrant (vectors) + Vision chunks                                    ║
║                                                                      ║
║  LLM Router: OpenAI / Anthropic / Ollama / RunPod vLLM / 🆕Fine-tuned║
║                                                                      ║
║  ◉ Langfuse trace + Ragas score attach (CI gate)                    ║
║  ◉ Prompt caching (Anthropic)                                       ║
║  ◉ Batch API 지원 (offline eval)                                    ║
║  ◉ Deployed on Modal → https://devlog-rag-copilot.modal.run         ║
╚═══════════════════════════════════════════════════════════════════╝
```

### 🔥 통합 체크리스트 (v3 확장)

#### Core (Day 7-8)
- [ ] Hybrid retrieval (dense + BM25 + RRF)
- [ ] Cross-encoder or Cohere rerank
- [ ] Query transform: rewrite + multi-query
- [ ] Contextual Retrieval (Anthropic 2024)
- [ ] Pydantic Answer(text, citations, confidence)

#### Multi-modal (v3 추가)
- [ ] **Vision RAG**: PDF 표/차트 페이지를 Vision fallback
- [ ] **Voice input**: Whisper로 마이크 → agent
- [ ] (Stretch) Realtime API 양방향 음성

#### Multi-agent (v3 확장)
- [ ] LangGraph **Supervisor + 3 workers** (Researcher/Writer/Critic)
- [ ] Reflection loop max 2
- [ ] SqliteSaver checkpoint
- [ ] HITL interrupt

#### Fine-tuned model (v3 추가)
- [ ] Day 13 **LoRA SFT** 결과 → `LLM_PROVIDER=runpod-finetuned`로 라우팅 가능
- [ ] Fine-tune이 특정 쿼리에서 base보다 나은 case 1개 이상 증명

#### MCP
- [ ] `app/mcp/server.py` (Day 11 그대로)
- [ ] Claude Desktop config + 호출 스크린샷

#### Guardrails 3겹 (v3 확장)
- [ ] Input: Prompt-Guard 2 (Day 3)
- [ ] Input + Output: Guardrails AI validators
- [ ] Dialogue: NeMo Colang 규칙 1개
- [ ] (Stretch) LlamaFirewall

#### Observability
- [ ] Langfuse trace (all nodes + LLM + retriever + tool)
- [ ] Prompt Langfuse fetch (hot swap)
- [ ] Ragas score attach
- [ ] Cost/latency/error dashboard

#### Production
- [ ] FastAPI SSE streaming
- [ ] Anthropic prompt caching
- [ ] tenacity retry + aiolimiter + pybreaker + timeout
- [ ] PII 마스킹

#### Deployment (v3 추가)
- [ ] **Modal 배포**: `modal deploy` → public URL
- [ ] (Stretch) Fly.io 또는 Docker 배포 옵션
- [ ] (Stretch) K8s manifest (배포 안 해도 포함)

#### Eval (CI gate)
- [ ] Golden 50+ 건
- [ ] Ragas faithfulness ≥ 0.85 gate
- [ ] GitHub Actions (PR mini-eval, nightly full)

#### Docs
- [ ] README.md (공개용 전체 섹션)
- [ ] ARCHITECTURE.md (상세)
- [ ] decisions.md (ADR 5개+)
- [ ] retrospective.md (14일 회고 — 아래 가이드)

## 🖼 공개 README 섹션

```markdown
# Devlog RAG Copilot ULTRA
> Multi-modal RAG + Multi-agent + Fine-tuned + Guardrails + Deployed

![demo](docs/demo.gif)

## Why
(...본인 동기 1 문단)

## Architecture
![arch](docs/architecture.png)

## Stack
[badges: Python 3.12, FastAPI, LangGraph, Qdrant, Langfuse, Ragas, MCP, Modal, Unsloth]

## 🌐 Live Demo
https://devlog-rag-copilot.modal.run

## Quickstart
```bash
cp .env.example .env
docker compose up -d
./scripts/ingest_local.sh ./data/pdfs
uv run uvicorn app.main:app --reload
# or: uv run streamlit run ui/streamlit_app.py
```

## Eval Results
| Metric | Score |
|---|---|
| Faithfulness | 0.87 |
| Answer Relevancy | 0.89 |
| Context Precision | 0.82 |
| Context Recall | 0.84 |

## Features
- 🎤 Voice input (Whisper)
- 🖼 Vision RAG (표/차트 PDF)
- 🤖 Multi-agent (Supervisor + 3 workers)
- 🎯 Fine-tuned domain model (LoRA on Qwen3-8B)
- 🛡 3-layer Guardrails
- 🔌 MCP server (Claude Desktop)

## MCP (Claude Desktop)
```json
{"mcpServers": {"devlog": {"command":"uv","args":["run","python","-m","app.mcp.server"]}}}
```

## Fine-tuned Model
- Base: Qwen3-8B-Instruct
- LoRA rank: 16, epochs: 3
- Dataset: 150 Q&A from my tech notes
- Improvement: +15% Ragas faithfulness on domain queries

## Limitations (정직)
1. ...
2. ...
3. ...

## Roadmap
- [ ] Multi-user deployment
- [ ] Additional languages
- [ ] Real-time voice (full duplex)

## License
MIT
```

## 📊 최종 수치 목표 (v3)

| 메트릭 | 목표 |
|---|---|
| Ragas Faithfulness (base pipeline) | ≥ 0.85 |
| Ragas Faithfulness (fine-tuned) | ≥ 0.88 |
| Unanswerable 거절률 | ≥ 0.85 |
| p50 E2E | ≤ 5s |
| p95 E2E | ≤ 12s |
| Prompt cache hit ratio | ≥ 70% |
| Guardrails 공격 차단율 | ≥ 95% |
| CI mini-eval 시간 | ≤ 5분 |
| Live demo 가동률 | 100% (Modal scale-to-zero OK) |

## 📝 회고 가이드 (retrospective.md) — 자정 전 완료

1. **14일 중 가장 어려웠던 날** + 그 이유
2. **가장 과대평가된 자료 / 가장 과소평가된 자료** 각 1개
3. **실무에 당장 쓸 수 있는 기술 3개**
4. **Fine-tune vs RAG 선택 기준** — 본인 데이터 기준
5. **Multi-agent가 단일보다 나았던 경우 / 아니었던 경우**
6. **프로덕션에 쓰기 전 반드시 보강할 3가지** — 정직하게
7. **논문 25편 중 실무에 가장 유용했던 3편**
8. **다음 3개월 학습 계획** (extras / later 참고)

## 🎁 Day 15+ 다음 스텝 제안

이 14일로 "**LLM 풀스택 엔지니어 진입**" 완료. 다음:
- 프로덕션 레벨 reliability (load test, incident playbook)
- 본인 도메인 대형 데이터셋으로 fine-tune 반복
- 회사 합류 or 프로젝트 시작
- 논문 읽기 주 1편 → 6개월에 20편
- LLM 컨퍼런스/행사 참석

## 🔒 최종 공개 전 체크

- [ ] API key가 git history에 **없는지** 확인 (`git log -p | grep sk-`)
- [ ] `.env` gitignore 확실
- [ ] Hard limit 모든 provider 설정 확인
- [ ] Modal/Fly.io secrets는 별도 관리
- [ ] Demo gif에 개인 정보 없음 확인
- [ ] License MIT 명시
- [ ] README 30초 안에 이해되는지 스스로 읽기

## 🎊 공개 후

- GitHub repo URL을 **LinkedIn / Twitter / 슬랙 커뮤니티**에 공유
- Product Hunt (선택)
- HN Show (선택 — 부담이면 skip)
- 다음날 쉬기 **최소 하루**. 뇌 회복.

---

**14일 완주. 축하.**

막히면: [`troubleshooting.md`](troubleshooting.md) / [`recovery-playbook.md`](recovery-playbook.md) / `extras.md`.
