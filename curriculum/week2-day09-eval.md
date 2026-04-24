# Day 9 — Eval + Multi-Agent (ULTRA)

> **난이도**: ★★★★★ (v3 상향)
> **총량**: Ragas 8h + Multi-agent 3h + 정리 1h = **12h**.
> **철학**: "Eval 없는 개선은 미신" + 오늘 **Multi-agent 3 프레임워크 비교**도 끼워넣음.
> **논문**: ReAct + Reflexion + Tree of Thoughts + Judging LLM-as-a-Judge

## 🎯 오늘 끝나면

1. Ragas 4대 메트릭(faithfulness / answer_relevancy / context_precision / context_recall) **각각 어떻게 계산되는지** 설명
2. 어제 만든 5-6개 pipeline을 수치로 순위화 + **어느 구성이 왜 이겼는지** 인과 설명
3. **LLM-as-a-judge의 4대 편향**(positional / verbosity / self-preference / refusal) 인지 + 완화 기법 1개 이상 적용
4. **Golden dataset 확장 전략** — synthetic + 수기 검수로 30 → 100+ 스케일링
5. CI에 eval threshold gate 붙이기 (실제 GitHub Actions workflow까지 작성)
6. **Regression test suite** — prompt/모델 변경 시 자동 감지

## 📚 자료

### 🔥 필수

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 1.5h | [Ragas docs](https://docs.ragas.io/en/stable/) | 메트릭 수학적 정의 + API. v0.2는 API 변경 많음 주의. `evaluate()` + `EvaluationDataset` + `LLMContextPrecisionWithReference` 등. |
| 30m | [Ragas — Metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) | 30+ 메트릭 한눈에. 필수 4개 외에 `NoiseSensitivity`, `ResponseRelevancy`, `AnswerCorrectness`. |
| 30m | [Ragas — Synthetic Test Data Generation](https://docs.ragas.io/en/stable/concepts/test_data_generation/) | 문서에서 자동 QA 생성. 난이도 분포(simple/reasoning/multi-context) 조절. **수기 검수 필수**. |
| 1h | [OpenAI Cookbook — Evals hub](https://cookbook.openai.com/topic/evals) | OpenAI Evals 프레임워크 튜토리얼 모음. `pip install openai-evals` 이후. |
| 30m | [Evaluate RAG with LlamaIndex + Ragas](https://cookbook.openai.com/examples/evaluation/evaluate_rag_with_llamaindex) | end-to-end 예제. 파이프라인 튜닝에서 eval driven 개선 과정. |
| 30m | [LlamaIndex Evaluating — overview](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/) | LlamaIndex 자체 eval 모듈. Ragas 대안 시나리오. |

### ⭐ 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [Judging LLM-as-a-Judge (Zheng 2023)](https://arxiv.org/abs/2306.05685) | LLM 채점관 편향 실험. **Abstract + Table 3만**. positional bias 실측 수치. |
| 30m | [Arize Phoenix — Evals](https://docs.arize.com/phoenix/evaluation/llm-evals) | Phoenix eval API. observability와 eval 통합 시각화. |
| 20m | [Braintrust docs](https://www.braintrust.dev/docs) | Eval SaaS. Dataset / Experiment / Scorer. ladder 비교 UI 좋음. |
| 20m | [DeepEval](https://docs.confident-ai.com/docs/getting-started) | `pytest` 스타일 LLM 테스트. CI 친화적. |
| 20m | [Jason Liu — RAG Improvement Loop](https://jxnl.co/writing/2024/08/19/rag-flywheel/) | 실무 팁: 데이터 먼저, metric 먼저, 그다음에 기법. |

### 🎓 선택

- [OpenAI Evals GitHub](https://github.com/openai/evals) — 2022년부터의 축적된 evals 스펙. 현재는 maintenance mode이지만 레퍼런스로 가치.
- [Trulens docs](https://www.trulens.org/) — Ragas 대안 / 보완.
- [MT-Bench / AlpacaEval](https://arxiv.org/abs/2306.05685) — 오픈 LLM 벤치 스탠다드.

## 🔬 실습 (5.5h)

### 프로젝트: RAG Eval Pipeline + CI Gate

위치: `projects/day08-rag-eval/`

```
day08-rag-eval/
├── dataset/
│   ├── qa_pairs.json             # Day 8에서 30+
│   ├── synthetic.py              # Ragas TestsetGenerator로 +50 합성
│   ├── review.py                 # 합성된 것 수기 검수 UI (CLI)
│   └── merged.json               # 최종 80-100건
├── run_ragas.py                  # 4 메트릭 × 5-6 pipeline
├── judges/
│   ├── custom_faithfulness.py    # 자체 구현 (이해 목적)
│   ├── pairwise.py               # A vs B 승률 (positional bias 제거)
│   └── llm_judge.py              # custom rubric scoring
├── reports/
│   ├── leaderboard.md            # 구성별 점수표
│   ├── failure_cases.md          # 공통 실패 패턴
│   └── cost_analysis.md          # 품질 vs 비용 Pareto
├── ci/
│   ├── gate.py                   # threshold 체크 스크립트
│   └── github_action.yml         # PR마다 mini-eval
└── README.md
```

### 🔥 필수 기능

1. **골든셋 확장 (80-100건)**:
   - Day 8 30건 유지
   - Ragas TestsetGenerator로 50건 합성 (`simple` / `reasoning` / `multi_context` / `conditional`)
   - 수기로 적어도 20건 검수해서 `reviewed: true` 표시
   - `adversarial` 10건 추가 (prompt injection 시도, unanswerable 등)
2. **Ragas 4대 메트릭** 계산 — 6개 pipeline × 80건:
   - `Faithfulness` — 답변이 retrieved context에 근거하는가
   - `ResponseRelevancy` (구 answer_relevancy) — 답변이 질문에 답하는가
   - `LLMContextPrecisionWithReference` — 가져온 chunk 중 유용한 비율
   - `LLMContextRecall` — 정답을 뒷받침하는 정보를 다 가져왔는가
3. **Judge 모델 편향 완화**:
   - **Positional** — A/B 비교 시 순서 swap 후 평균
   - **Self-preference** — judge를 testee와 다른 모델로 (testee=4o-mini면 judge=claude-sonnet 또는 반대)
   - **Verbosity** — "길수록 좋은 답"으로 편향. rubric에 "간결성" 명시
4. **Leaderboard 생성** — 구성별 메트릭 평균 + std + cost + latency:
   ```
   | Pipeline        | Faith | AnsRel | CtxP  | CtxR  | $/q   | p50 (s) |
   | baseline        | 0.74  | 0.80   | 0.65  | 0.70  | 0.002 | 2.1     |
   | +rewrite        | 0.78  | 0.82   | 0.72  | 0.75  | 0.003 | 2.6     |
   | +hybrid         | 0.80  | 0.85   | 0.74  | 0.81  | 0.004 | 2.4     |
   | +rerank         | 0.84  | 0.86   | 0.82  | 0.80  | 0.005 | 3.1     |
   | full_stack      | 0.87  | 0.88   | 0.84  | 0.83  | 0.012 | 4.5     |
   | contextual      | 0.89  | 0.90   | 0.88  | 0.84  | 0.008 | 3.0     |
   ```
5. **Failure analysis** — 틀린 케이스 10+건 공통 패턴 추출 ("질문이 숫자를 요구하는데 chunk에 범위만 있음" 등). `failure_cases.md`에 기록.
6. **CI gate**:
   - `gate.py`: mini-eval (20건 샘플) faithfulness < 0.75면 exit 1
   - `github_action.yml`: PR마다 실행
7. **Cost vs quality Pareto** — 각 pipeline을 (faithfulness, cost)로 플롯 → Pareto frontier 선정

### 🔥 Custom Judge 구현 (이해 목적)

`custom_faithfulness.py`로 Ragas 내부를 직접 따라하기:

```python
# 1. 답변을 claim 리스트로 쪼개기 (LLM)
# 2. 각 claim이 context에서 검증되는지 판단 (LLM)
# 3. claims_supported / total_claims = faithfulness score
```

돌려보고 Ragas 결과와 비교해 오차 확인.

### 🔥 Pairwise judging (선택 Stretch)

`pairwise.py` — 두 pipeline의 답변을 동시에 보여주고 "어느 게 더 나은가" judge에게 물음. **순서 swap + 다수결**. 절대평가보다 noise 낮음.

### 📊 실전 수치 감각

- Faithfulness > 0.8 = production ready
- Faithfulness < 0.7 = hallucination 빈번, 쓰면 안 됨
- Context Precision > 0.8 = retrieval 품질 good
- Context Recall > 0.8 = 지식 커버리지 good
- 실제 OpenAI 논문 기준 GPT-4 + strong retriever가 대략 0.85-0.90 수준

### 🔥 Stretch

- 🧪 **LLM-as-a-judge 모델 4종 비교** (Claude Sonnet / GPT-4o / Gemini Pro / 로컬 Qwen)의 채점 일치도 (inter-rater agreement, Kappa)
- 🧪 **Category-weighted 메트릭** — factual 문제는 faithfulness에 2x 가중, synthesis는 answer_relevancy에 2x
- 🧪 **Langfuse scoring 연동** — Day 12 내용 당겨쓰기. Langfuse trace에 Ragas score attach.
- 🧪 **BERTScore / BLEU baseline** 비교 — Ragas 없이 전통 메트릭만 썼다면 어떤 결론?

## ✅ 체크리스트

- [ ] Golden dataset 80-100건 (수기 검수된 20+ 포함)
- [ ] 6개 pipeline × Ragas 4 메트릭 매트릭스 완성
- [ ] Judge 모델 편향 완화 1개 이상 적용 (position swap / pairwise / 다른 judge)
- [ ] Custom faithfulness 구현해서 Ragas 결과 ±0.05 이내 재현
- [ ] **수치 근거로** "내 production 후보 pipeline 1개" 결정 + 근거 2문단
- [ ] Failure 10+ 케이스 패턴 분류
- [ ] Cost vs quality Pareto 그래프 (텍스트 표로도 OK)
- [ ] `gate.py` 실행 → threshold 미만이면 exit 1
- [ ] GitHub Action YAML 작성 (실제 push는 Day 14)
- [ ] `cheatsheets/eval-metrics.md` 본인 수치/관찰 반영

## 🧨 자주 틀리는 개념

1. **"Ragas 점수 높으면 실제 사용자 만족"** — 상관관계 있지만 동일 아님. 최종적으로 사용자 UX 테스트 필수.
2. **"golden dataset은 크면 다 좋다"** — 품질 > 수량. **20개 수기** > **200개 쓰레기 synthetic**. 수기 검수 없는 synthetic은 편향 증폭.
3. **"Judge는 큰 모델일수록 좋다"** — 대체로 맞지만 **비용**. 작은 judge를 여러 번(ensemble) 쓰는 전략도.
4. **"자기 자신을 judge로 쓰면 안 됨"** — self-preference bias. 반드시 **다른 모델 or human**.
5. **"Faithfulness 1.0 목표"** — 현실적이지 않음. 0.85-0.90가 상위권 기준. 1.0은 대체로 eval이 너무 관대하다는 뜻.
6. **"Context Recall 높으면 답 품질 보장"** — 아님. Recall 높아도 LLM이 이상한 chunk를 고르면 faithful ≠ correct.
7. **"한 번 돌린 메트릭으로 결정"** — Variance 있음. 최소 3회 평균, 또는 큰 샘플.

## 🧪 산출물

- `projects/day08-rag-eval/` — 전체
- `reports/leaderboard.md` — 6 pipeline 결과표
- `reports/failure_cases.md` — 10+ 공통 실패 패턴
- `ci/gate.py` + `ci/github_action.yml` — 실동 가능한 gate
- `cheatsheets/eval-metrics.md` — 본인 수치 반영
- `notes/decisions.md` — "내가 고른 production pipeline + 이유 (수치 + 정성)" ADR 스타일

## 📌 핵심 키워드

- Faithfulness, Groundedness
- Response Relevancy (Answer Relevancy)
- Context Precision (LLMContextPrecisionWithReference)
- Context Recall (LLMContextRecall)
- Noise Sensitivity, Answer Correctness
- Golden dataset, Ground truth
- Synthetic test generation, Data quality
- LLM-as-a-judge, Rubric scoring
- Positional bias, Verbosity bias, Self-preference bias, Bandwagon bias
- Pairwise comparison, Elo rating
- Inter-rater agreement (Kappa)
- Regression test, CI gate, threshold
- Pareto frontier (quality-cost)
- Eval drift, test set contamination

## ⚠️ 프로덕션 주의

- **Eval 비용 관리** — 매 PR마다 풀 eval 돌리면 월 $수백. **샘플(20건) PR-time + nightly full**.
- **Golden set freeze** — 데이터가 계속 바뀌면 점수 비교 무의미. Version 태그로 고정.
- **Leakage 방지** — testset 질문/답이 training에 유출되면 점수 부풀림. Synthetic 생성 시 주의.
- **Cost/latency도 metric** — 품질만 보고 고르면 돈 터짐.

## 🤖 v3 추가 — Multi-Agent 프레임워크 3종 비교 (3h)

Day 10의 Single-agent LangGraph **선행학습**. 단일 vs 멀티 언제?

### 🔗 자료
- [LangGraph — Multi-agent collaboration](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/)
- [LangGraph Supervisor pattern](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)
- [CrewAI docs](https://docs.crewai.com/) — 역할 기반 dynamic multi-agent
- [OpenAI Swarm (experimental)](https://github.com/openai/swarm) — handoff 패턴

### 🔥 실습 — 같은 task를 3 프레임워크로

**Task**: "Devlog RAG에 2026-04 최신 Ragas 소식을 추가하고 어떻게 업데이트할지 plan 생성"

1. **LangGraph Supervisor** (1h): supervisor + researcher + writer + critic 4 노드
2. **CrewAI** (1h): Researcher/Writer/Critic 역할 정의 + Process.sequential
3. **OpenAI Swarm** (1h): agent 간 handoff — Researcher가 Writer로 명시적 넘김

### 📊 비교표 (`notes/concepts.md`)
| 프레임 | 라인 수 | 실행 시간 | 토큰 비용 | 품질 | 장점 | 단점 |
|---|---|---|---|---|---|---|
| LangGraph Supervisor | | | | | 명시적 state | 복잡 |
| CrewAI | | | | | role-based 직관적 | blackbox |
| Swarm | | | | | handoff 단순 | experimental |

## 📜 논문 4편 Figure 수준 (v3 추가, 1h)

- **ReAct** ([Yao 2022](https://arxiv.org/abs/2210.03629)) — Figure 1 Thought/Action/Observation
- **Reflexion** ([Shinn 2023](https://arxiv.org/abs/2303.11366)) — Figure 1 self-reflection loop
- **Tree of Thoughts** ([Yao 2023](https://arxiv.org/abs/2305.10601)) — Figure 1-2 tree search
- **Judging LLM-as-a-Judge** ([Zheng 2023](https://arxiv.org/abs/2306.05685)) — Table 3 positional bias 실측 수치

## 🎁 내일(Day 10) 미리보기
LangGraph single-agent 깊이 + **Voice input (Whisper)** 추가.
