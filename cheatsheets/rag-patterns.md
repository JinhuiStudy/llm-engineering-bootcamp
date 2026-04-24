# RAG Patterns 치트시트

## 기본 플로우
```
Load → Split → Embed → Store → Retrieve → Augment → Generate
                                     ↓
                         (Rerank / Filter / Expand)
```

## Chunk 설계 (품질의 50%)

| Chunk size | 장점 | 단점 |
|---|---|---|
| 128-256 tokens | 정밀 검색, 인덱싱 가성비 | 맥락 부족 |
| 500-800 tokens | 표준. 균형 | — |
| 1500+ tokens | 맥락 풍부 | 검색 정확도↓, 비용↑ |

- Overlap: 10-20% (너무 크면 중복)
- 의미 단위(문단/헤더) 우선 → `RecursiveCharacterTextSplitter` 권장
- 표/코드는 별도 전략 (자르지 않음)

## Retrieval 전략

### 1. Dense (embedding)
- 의미 기반. 표준.
- 약점: 고유명사, 숫자, 새로운 용어

### 2. Sparse (BM25)
- 키워드 매칭. 빠르고 해석 가능.
- 약점: 동의어, paraphrase

### 3. Hybrid (RRF)
- Dense + Sparse 결합. Reciprocal Rank Fusion로 병합.
- 거의 항상 단일보다 나음

### 4. Reranking
- Top-50 → Cross-encoder → Top-5
- `cross-encoder/ms-marco-MiniLM-L-6-v2` (무료, 작음)
- Cohere Rerank API (유료, 강함)
- 비용/지연 대비 정확도 ⬆⬆

## Query Transformation

| 기법 | 언제 유용 | 주의 |
|---|---|---|
| Query rewriting | 구어체 질문 | LLM 비용 추가 |
| HyDE | 검색어와 문서 어휘가 다를 때 | 잘못된 가설 시 역효과 |
| Multi-query | 다관점 질문 | 결과 병합 필요 (RRF) |
| Step-back | 복잡한 구체 질문 | 답이 너무 일반화될 수 있음 |
| Decomposition | 복합 질문 (A이면서 B) | 각 sub-Q 따로 RAG |

## Prompt 패턴 (답변 생성)

### 표준 (환각 방지)
```
아래 context에만 근거하여 답하라.
없으면 "모르겠다"고 답하라.
답 끝에 사용된 문서/페이지를 [1] [2] 형태로 인용하라.

<context>
[1] file_a.pdf p.3: ...
[2] file_b.md §2: ...
</context>

<question>{q}</question>
```

### 고급 (confidence + citations)
- Pydantic 모델로 `{answer, citations: list[Citation], confidence: float}` 강제

## 평가 (Ragas 기준)

| 지표 | 의미 | 어떻게 개선 |
|---|---|---|
| **Faithfulness** | 답이 context에 있는가 | 프롬프트 강화, "모르면 모른다고" |
| **Answer relevancy** | 답이 질문에 답하는가 | 프롬프트, CoT |
| **Context precision** | 가져온 chunk 중 쓸만한 비율 | rerank, hybrid |
| **Context recall** | 정답에 필요한 걸 다 가져왔나 | chunk size, top-k, query expansion |

## 성능 향상 순서 (cost 대비 효과)

1. **Chunk/overlap 튜닝** (무료) — 대부분 여기서 큰 개선
2. **Reranker 추가** (cpu) — 정확도 크게 ↑
3. **Hybrid search** (저렴) — 어휘 커버리지 ↑
4. **Query rewriting** (LLM 호출 1회) — 대화형 쿼리 품질 ↑
5. **Multi-query / HyDE** (LLM 호출 다수) — 마진 이득
6. **Fine-tuning embedding** (노가다) — 도메인 특화 시

## 안티패턴 (하지 마)

- [ ] Eval 없이 RAG 개선 시도
- [ ] Chunk 크기 무턱대고 크게 (8k+ 같은 극단)
- [ ] Top-k 20+ 로 무작정 늘리기 (컨텍스트 오염)
- [ ] Source citation 없는 답변
- [ ] Raw user input을 sanitize 없이 검색 쿼리로 (prompt injection)
- [ ] Embedding 모델을 주기적으로 바꾸면서 기존 인덱스 재생성 안 함
