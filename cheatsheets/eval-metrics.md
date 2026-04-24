# Eval Metrics 치트시트

## RAG Metrics (Ragas 기준)

### Faithfulness
- 정의: 답변이 retrieved context에 근거하는가 (0-1)
- 낮을 때: hallucination. 프롬프트에 "context에만 근거" 강화
- 계산: 답변의 claim을 쪼개고, 각 claim이 context에서 검증 가능한지 LLM 판단

### Answer Relevancy
- 정의: 답변이 질문에 답하는가 (0-1)
- 낮을 때: 부분 답변, 빙 돌기. CoT or 프롬프트 명료화
- 계산: 답변으로 가능한 질문을 N개 역생성 → 원 질문과 코사인 유사도 평균

### Context Precision
- 정의: 가져온 chunk 중 실제로 유용한 비율 (0-1)
- 낮을 때: retriever가 쓰레기 가져옴. rerank, better chunking, hybrid
- 계산: 각 retrieved chunk가 ground truth 답에 기여하는지 LLM 판정

### Context Recall
- 정의: ground truth를 뒷받침하는 정보를 다 가져왔는가 (0-1)
- 낮을 때: top-k 부족, 쿼리 부족. multi-query, query rewrite, k 증가
- 계산: ground truth의 각 문장이 retrieved context에서 추론 가능한지

## Non-RAG LLM Metrics

### Accuracy / Exact match
- 분류 태스크용. Structured output이면 완벽 측정 가능.

### Pass@k
- 코드 생성. k번 생성 중 하나라도 통과하는 비율.

### BLEU / ROUGE
- 번역/요약 전통 metric. LLM 시대에는 덜 쓰임 (표현 다양성 벌점).

### G-Eval / MT-Bench style
- LLM-as-a-judge. 1-10점 매기기.
- 위험: LLM별 편향. 여러 judge로 평균, pairwise 사용 권장.

## LLM-as-a-Judge 편향 주의

| 편향 | 증상 | 대응 |
|---|---|---|
| Positional | 첫 번째 답을 더 선호 | 위치 swap 후 평균 |
| Verbosity | 긴 답을 더 선호 | length penalty, 길이 가이드 |
| Self-preference | 같은 모델 답 선호 | judge를 다른 모델로 |
| Bandwagon | 다수 의견에 수렴 | 독립 평가 |
| Refusal bias | 거절도 0점 아닌 기준 필요 | rubric 명시 |

## Golden Dataset 만들기

- 시작: 20-30개 수기 작성 (직접 만들어라)
- 성장: synthetic generation (LLM이 문서 읽고 Q/A 쌍 만들기) + 수기 검수
- 카테고리:
  - ✅ easy (context에 명확한 답)
  - ✅ hard (여러 chunk 조합)
  - ✅ unanswerable (모르겠다고 답해야)
  - ✅ adversarial (prompt injection, ambiguous)

## 평가 파이프라인 구조

```python
for config in [baseline, v1, v2, ...]:
    results = []
    for q in golden_dataset:
        answer, context = run_rag(config, q)
        scores = ragas.evaluate(q, answer, context, ground_truth)
        results.append(scores)
    print(config.name, mean(results))
```

## CI에서 쓰기

- Threshold 설정 (e.g. faithfulness > 0.8)
- PR이 threshold 떨어뜨리면 block
- Cost 계산해두기 — 매 PR마다 eval 돌리면 비쌀 수 있음
- Sample 20-50개로 빠른 eval + nightly full run

## 자주 하는 실수

- [ ] 정답셋이 너무 작음 (<10개)
- [ ] 정답셋에 개발자 본인 편향 (easy한 것만)
- [ ] 정답이 바뀌는데도 정답셋 freeze
- [ ] judge model을 testee model과 같게 (bias)
- [ ] 한 번 돌린 metric으로 결정 (variance 고려 안 함)
- [ ] Cost/latency는 eval 안 함 (품질만)
