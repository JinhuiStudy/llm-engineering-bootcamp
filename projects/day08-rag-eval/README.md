# Day 9 — RAG Eval Pipeline (Ragas + Custom Judge + CI Gate)

> **연결**: [`curriculum/week2-day09-eval.md`](../../curriculum/week2-day09-eval.md)
> **의존성**: Day 8 benchmark 결과 JSONL + 정답셋 30+
> **다음**: Day 12 Langfuse에 score attach, Day 14 CI gate

## 🎯 이 프로젝트로

1. Ragas **4대 메트릭** (faithfulness / answer_relevancy / context_precision / context_recall) 6 pipeline 비교
2. **Golden dataset 80-100건** — Day 8 30 + 합성 50 + 검수
3. **LLM-judge 편향 완화** — positional swap / 다른 judge model / verbosity rubric
4. **CI gate** — threshold 미만이면 exit 1, GitHub Actions workflow 작성
5. **Cost vs Quality Pareto** — 최적 pipeline 수치 기반 선정

## 📁 디렉토리

```
day08-rag-eval/
├── pyproject.toml
├── dataset/
│   ├── qa_pairs.json                  # Day 8 30건
│   ├── synthetic.py                   # Ragas TestsetGenerator로 +50
│   ├── review.py                      # 합성 건 CLI 수기 검수 도우미
│   └── merged.json                    # 최종 80-100건 (reviewed: true 마킹)
├── run_ragas.py                       # 전체 파이프라인 실행
├── judges/
│   ├── custom_faithfulness.py         # Ragas 내부를 직접 따라 구현 (이해 목적)
│   ├── pairwise.py                    # A vs B 승률 (positional bias 제거)
│   ├── multi_judge.py                 # 4 judge ensemble (Claude/GPT/Gemini/Qwen)
│   └── rubric.py                      # 자체 rubric 1-5 scoring
├── reports/
│   ├── leaderboard.md                 # pipeline × metric 표
│   ├── failure_cases.md               # 10+ 공통 실패 패턴
│   ├── cost_analysis.md               # $/quality Pareto
│   └── judge_agreement.md             # inter-rater (Cohen's Kappa)
├── ci/
│   ├── gate.py                        # threshold 체크 → exit code
│   └── github_action.yml              # PR마다 mini-eval (20), nightly full
└── README.md
```

## 🚀 시작

```bash
cd projects/day08-rag-eval
uv sync
uv add ragas datasets pandas
```

## ✅ 필수 기능

### Golden Dataset
- [ ] Day 8 30건 import
- [ ] `synthetic.py` — Ragas `TestsetGenerator`로 `simple(20) + reasoning(15) + multi_context(10) + conditional(5)` 생성
- [ ] `review.py` — 합성 건 CLI로 1개씩 훑어보며 y/n/edit → `reviewed: true`
- [ ] Adversarial 10건 추가 (prompt injection / unanswerable / 시간 지난 정보)
- [ ] 최종 `merged.json` 80-100건

### Ragas 실행
- [ ] `run_ragas.py`:
  - 6 pipeline × N 쿼리 = benchmark JSONL → Ragas `EvaluationDataset`
  - Metrics: `Faithfulness`, `ResponseRelevancy`, `LLMContextPrecisionWithReference`, `LLMContextRecall`
  - `evaluator_llm` = Claude Sonnet (or GPT-4o). testee와 다른 provider
- [ ] 결과 `reports/leaderboard.md` 자동 생성:
  ```
  | Pipeline     | Faith | AnsRel | CtxP | CtxR | $/q   | p50(s) |
  |--------------|-------|--------|------|------|-------|--------|
  | baseline     | 0.74  | 0.80   | 0.65 | 0.70 | 0.002 | 2.1    |
  | +rewrite     | 0.78  | 0.82   | 0.72 | 0.75 | 0.003 | 2.6    |
  | +hybrid      | 0.80  | 0.85   | 0.74 | 0.81 | 0.004 | 2.4    |
  | +rerank      | 0.84  | 0.86   | 0.82 | 0.80 | 0.005 | 3.1    |
  | +contextual  | 0.89  | 0.90   | 0.88 | 0.84 | 0.008 | 3.0    |
  | full_stack   | 0.87  | 0.88   | 0.84 | 0.83 | 0.012 | 4.5    |
  ```

### Judge Bias 완화
- [ ] `pairwise.py` — A/B 두 답변 judge에게 보임. 순서 swap 후 두 번 → 다수결
- [ ] `multi_judge.py` — 4 judge 앙상블 → majority vote
- [ ] `judge_agreement.md` — Cohen's Kappa로 judge 간 일치도

### Custom Judge (이해 목적)
- [ ] `custom_faithfulness.py`:
  ```python
  # 1) 답변을 claim 리스트로 쪼개기 (LLM)
  # 2) 각 claim이 context에서 검증 가능한가 (LLM)
  # 3) score = supported / total
  ```
  Ragas와 ±0.05 이내 일치 확인

### Failure Analysis
- [ ] 틀린 케이스 10+ 공통 패턴 분류:
  - "질문은 숫자 요구, chunk엔 범위만"
  - "citation은 올바른데 추론 단계 빠짐"
  - "context 내 모순 정보 → 최신 순서 몰라서 옛날 걸 씀"
- [ ] `failure_cases.md`에 카테고리별 예시

### CI Gate
- [ ] `gate.py`:
  ```python
  import sys
  thresholds = {"faithfulness": 0.85, "context_precision": 0.80, "response_relevancy": 0.85}
  results = load_leaderboard()
  for pipeline, scores in results.items():
      for metric, threshold in thresholds.items():
          if scores[metric] < threshold:
              print(f"FAIL: {pipeline}.{metric} = {scores[metric]} < {threshold}")
              sys.exit(1)
  ```
- [ ] `github_action.yml`:
  ```yaml
  on: [pull_request]
  jobs:
    mini-eval:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - run: uv sync
        - run: uv run python run_ragas.py --sample 20 --pipeline full_stack
        - run: uv run python ci/gate.py
  ```

### Cost vs Quality Pareto
- [ ] 각 pipeline을 (faithfulness, cost_per_q) 로 플롯 (matplotlib 또는 text art)
- [ ] Pareto frontier 선정 — "이 비용에서 품질 상한"

## 📊 수치 기준

| 메트릭 | 기준 |
|---|---|
| Golden reviewed: true 비율 | ≥ 20% |
| Ragas 4 metric 모두 계산 성공 | 100% |
| Judge agreement Kappa | ≥ 0.7 |
| Faithfulness (best pipeline) | ≥ 0.85 |
| CI gate 실행 시간 (sample 20) | ≤ 5분 |
| Pareto frontier 상 pipeline 식별 | 1개 |

## 🧨 실전 함정

1. **Ragas v0.2 API 변경 잦음** — docs 정확한 버전 확인
2. **judge = testee 모델** — self-preference bias. 반드시 다른 provider
3. **정답셋 20 이하** — variance 큼. 비교 의미 없음. 80+ 권장
4. **synthetic 수기 검수 안 함** — 합성 자체 오류 증폭 (쓰레기 in, 쓰레기 out)
5. **faithfulness 1.0** — judge가 너무 관대함의 신호. rubric 엄격하게
6. **CI 매 PR 풀 eval** — 비싸다. sample 20 PR-time + nightly full 구조
7. **Cost 계산 빠짐** — 품질만 보면 "비싼 pipeline이 정답"으로 편향
8. **judge도 temperature 0 필수** — 점수 노이즈 줄임

## 🎁 Stretch

- 🧪 Category-weighted metric — factual 2x faithfulness, synthesis 2x answer_relevancy
- 🧪 BERTScore / BLEU baseline 비교 — 전통 metric만 쓰면 결론 달라지는가?
- 🧪 Langfuse score attach — trace_id로 매핑 (Day 12 연결)
- 🧪 Regression test suite — 과거 winner pipeline 점수 저장 → 신 버전이 떨어뜨리는지

## 🔗 다음에 쓰이는 곳

- Day 10 agent: winner pipeline을 retriever 노드로
- Day 12: Ragas scores → Langfuse score attach
- Day 14: `eval/` 와 CI gate 그대로 포팅
