# Day 9 — RAG Evaluation (Ragas)

커리큘럼: `curriculum/week2-day09-eval.md`

## 체크리스트
- [ ] Ragas 설치 + 첫 metric 성공
- [ ] `dataset.py` — 어제 qa_pairs.json 로드
- [ ] `run_ragas.py` — faithfulness/answer_relevancy/context_precision/context_recall
- [ ] 어제의 6가지 config 모두 평가
- [ ] `results/leaderboard.md` — 결과표
- [ ] `failure_cases.md` — 공통 실패 패턴 분석
- [ ] LLM-as-a-judge의 편향 (positional/verbosity) 1개 실증

## 교훈 기록
- 점수가 체감과 다른 케이스
- 정답셋을 늘리니 달라진 순위
- Metric 1개만 보면 안 되는 이유
