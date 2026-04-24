# Day 9 — Evaluation (Ragas + OpenAI Evals)

## 목표
- RAG 품질을 **주관적 느낌이 아니라 숫자**로 측정
- Ragas로 faithfulness / answer_relevancy / context_precision / context_recall 계산
- OpenAI Evals로 regression test 파이프라인 구성
- Eval 결과를 근거로 어제의 고급 RAG 변형들 중 최고를 선정

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [Ragas docs](https://docs.ragas.io/) | 2h |
| 필수 | [OpenAI Cookbook — Evals topic](https://developers.openai.com/cookbook/topic/evals) | 2h |
| 필수 | [OpenAI Cookbook — Getting started with OpenAI evals](https://developers.openai.com/cookbook/examples/evaluation/getting_started_with_openai_evals) | 1h |
| 필수 | [Evaluate RAG with LlamaIndex](https://developers.openai.com/cookbook/examples/evaluation/evaluate_rag_with_llamaindex) | 1h |
| 선택 | [LlamaIndex evaluating](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/) | 1h |
| 선택 | [OpenAI Evals repo](https://github.com/openai/evals) | 1h |

## 실습 (4.5h)

### 프로젝트: RAG Eval Pipeline
위치: `projects/day08-rag-eval/`

```
day08-rag-eval/
├── dataset.py          # 어제의 qa_pairs.json 로드 + golden answer 생성
├── run_ragas.py        # Ragas 메트릭 계산
├── run_openai_eval.py  # OpenAI Evals 프레임 (또는 간단 자체 eval)
├── compare_configs.py  # v1 / v2 (dense / hybrid / rerank) 성능 비교표
└── results/
    └── leaderboard.md  # 구성별 점수
```

### 요구사항
1. 어제 `eval/qa_pairs.json` (20쌍) 불러오기
2. 각 질문을 다음 파이프라인에 돌림:
   - baseline (dense only, Day 7)
   - +query rewriting
   - +HyDE
   - +hybrid
   - +reranking
   - 모두 조합
3. Ragas 메트릭 계산:
   - `faithfulness` (답이 context에 근거하는가)
   - `answer_relevancy`
   - `context_precision`
   - `context_recall`
4. 결과를 `results/leaderboard.md`에 표로 저장
5. 어떤 조합이 왜 이겼는지 분석 1-2문단

### Stretch
- 틀린 케이스를 `failure_cases.md`에 모으고 공통 패턴 분석
- LLM-as-a-judge 직접 구현 (custom eval)

## 체크리스트

- [ ] Ragas 4가지 메트릭의 의미를 설명 가능
- [ ] "LLM-as-a-judge"의 편향 문제 설명 가능 (positional bias, verbosity bias 등)
- [ ] 수치 기반 의사결정 경험 1회 이상 ("숫자 보고 이 구성 골랐다")
- [ ] `cheatsheets/eval-metrics.md` 작성
- [ ] 정답셋 확보의 어려움을 몸으로 체감 (여기가 LLM 앱 개발의 진짜 병목)

## 핵심 키워드
- faithfulness, groundedness, answer relevancy, context precision, context recall
- golden dataset, synthetic eval generation, test set 오염 (leak)
- LLM-as-a-judge, pairwise comparison, reference-free / reference-based eval
- BLEU, ROUGE (전통 NLP — LLM에서는 잘 안 씀, 이름만)
- Regression test, eval harness, A/B framework

## 중요한 원칙
- **Eval 없는 RAG 개선은 미신**. 체감으로 "좋아진 것 같다"는 절대 믿지 말 것.
- 정답셋 20개면 최소 시작점. Production은 200개+ 필요.
