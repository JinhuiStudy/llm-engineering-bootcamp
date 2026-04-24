# Day 7 — 기본 RAG v1 (3 프레임워크 병렬 구현 + 정답셋 20)

> **연결**: [`curriculum/week1-day07-basic-rag.md`](../../curriculum/week1-day07-basic-rag.md)
> **의존성**: Day 6의 Qdrant collection, Day 4 Pydantic schema 감각
> **다음**: Day 8 고급 RAG가 이 코드베이스를 복사해서 확장

## 🎯 이 프로젝트로

1. RAG 7단계 (**Load → Split → Embed → Store → Retrieve → Augment → Generate**)를 3 프레임워크로 병렬 구현 → 라인 수/가독성/유연성 비교
2. **환각 방지 3종세트**: "근거 없으면 모른다" 프롬프트 + Pydantic citation 강제 + "lost in the middle" 배치
3. **Pydantic Answer schema** — `Answer(text, citations: list[Citation], confidence: float)` 로 citation 100% 보장
4. **정답셋 20개** 수기 작성 — 카테고리 분포 (factual / synthesis / reasoning / unanswerable / adversarial)

## 📁 디렉토리

```
day06-basic-rag/
├── pyproject.toml
├── docker-compose.yml              # Qdrant
├── app/
│   ├── ingest.py                   # PDF/MD/HTML → chunk → embed → upsert
│   ├── retrieve.py                 # top-k + score threshold
│   ├── augment.py                  # re-order (lost-in-middle 대응) + dedup + truncate
│   ├── generate.py                 # LLM call + citation 추출
│   ├── rag.py                      # 전체 pipeline 조립
│   └── cli.py
├── implementations/
│   ├── from_scratch.py             # OpenAI SDK + Qdrant client — 300 lines 내외
│   ├── with_langchain.py           # LCEL pipe 문법
│   └── with_llamaindex.py          # VectorStoreIndex + QueryEngine
├── schemas/
│   └── answer.py                   # Pydantic Answer / Citation
├── prompts/
│   ├── rag_system.txt
│   └── rag_user.txt                # jinja-ish: <context> + <question>
├── data/
│   └── pdfs/                       # 5개 기술문서 (qdrant manual, arxiv, etc.)
├── eval/
│   ├── qa_pairs.json               # 20건 수기 — 내일 Day 9 eval 입력
│   └── make_golden.py              # semi-auto 생성 도우미
├── results/
│   └── compare.md                  # 3구현 라인수/latency/가독성
└── README.md
```

## 🚀 시작

```bash
cd projects/day06-basic-rag
uv sync
uv add qdrant-client openai langchain langchain-openai langchain-qdrant llama-index llama-index-vector-stores-qdrant pypdf pdfplumber

docker compose up -d    # Day 6 collection 재사용이면 skip
```

## ✅ 필수 기능

### 파이프라인 (`app/`)
- [ ] `ingest.py` — pypdf 먼저, 실패/표 있으면 pdfplumber, 스캔이면 Unstructured. `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, separators=["\n\n","\n",". "," "])`
- [ ] `retrieve.py` — top_k=5, optional `score_threshold=0.3`
- [ ] `augment.py`:
  - Dedup: 같은 문서/페이지 chunk 중복 제거
  - Truncate: 총 context 8k tokens 넘으면 뒤부터 잘라냄
  - Re-order: 가장 relevant은 앞+뒤 양끝에 (U-shape for lost-in-middle)
- [ ] `generate.py`:
  - Pydantic `response_format=Answer` 강제 (OpenAI strict)
  - Prompt에 context chunks를 `[1] file=foo.pdf p=3: ...` 번호 붙임
  - 답변 text에서 `[1][2]` 파싱해서 Citation 리스트 만들기

### 3 구현
- [ ] `from_scratch.py` — 프레임워크 없이 직접. 300줄 내외. 기본 원리 이해의 기준점
- [ ] `with_langchain.py`:
  ```python
  chain = (
      {"context": retriever | format_docs, "question": RunnablePassthrough()}
      | prompt
      | llm.with_structured_output(Answer)
  )
  ```
- [ ] `with_llamaindex.py`:
  ```python
  index = VectorStoreIndex.from_vector_store(QdrantVectorStore(...))
  query_engine = index.as_query_engine(similarity_top_k=5, response_mode="compact")
  ```

### 정답셋 (중요!)
- [ ] `qa_pairs.json` 20건 구조:
  ```json
  {
    "id": "q001",
    "question": "...",
    "ground_truth": "...",
    "source_doc": "qdrant_tutorial.pdf",
    "source_page": 4,
    "category": "factual|synthesis|reasoning|unanswerable|adversarial",
    "difficulty": "easy|medium|hard"
  }
  ```
- [ ] 카테고리 분포: factual 8 / synthesis 5 / reasoning 3 / unanswerable 2 / adversarial 2
- [ ] 내일 Day 9 Ragas 입력으로 쓸 것이므로 품질이 곧 eval 품질

## 📊 수치 기준

| 메트릭 | 기준 |
|---|---|
| Context에 있는 정답 질문 정답률 | ≥ 90% |
| Unanswerable 질문 "모른다" 응답 | ≥ 80% |
| Citation 포함률 | ≥ 95% |
| Citation 정확률 (실제 근거 chunk) | ≥ 85% |
| p50 latency (top-5, 4o-mini, streaming OFF) | ≤ 3s |
| 3 구현 간 응답 동일성 (temp 0) | 80%+ |

## 🧨 실전 함정

1. **LangChain API가 자주 바뀜** — LCEL pipe `|`는 표준화됐으니 OK. legacy `LLMChain`은 피하기
2. **Citation 프롬프트로만 요구하면 빠짐** — Pydantic Answer로 강제 필수
3. **Top-k 크면 좋다 (X)** — k=5가 sweet. k=20은 rerank 있을 때만
4. **Prompt에 context 너무 길게** — lost-in-middle + 비용. augment에서 dedup/truncate 필수
5. **PDF 스캔 파일** — pypdf가 빈 문자열 반환. pdfplumber도 실패. Vision fallback 필요
6. **같은 질문 여러 번 테스트 시 Qdrant 캐시 의심** — 실제로는 없음. 응답 차이는 LLM 비결정성
7. **환각 방지 프롬프트 있는데도 환각** — 모델이 small하거나 context가 혼란스러울 때. 모델 승급 or rerank
8. **source_page가 0-indexed vs 1-indexed** — pypdf는 0-index. 사용자 표시는 1-index

## 🎁 Stretch

- 🧪 Streaming 답변 (SSE) — 토큰 단위 출력 + citation은 종료 시 일괄
- 🧪 Query-dependent chunk size — factual 200 / synthesis 800
- 🧪 Metadata filter로 "최근 1년 문서만"
- 🧪 Vision fallback — 스캔 PDF 페이지 → PNG → Claude/4o Vision
- 🧪 Korean NER 기반 entity filter — 질문의 entity가 retrieval 결과에 포함되는지 후처리 검증

## 🔗 다음에 쓰이는 곳

- Day 8: 이 코드 복사 후 hybrid/rerank/query-transform 추가
- Day 9: `eval/qa_pairs.json` 그대로 사용 (30+로 확장)
- Day 10: LangGraph `retriever` 노드 = 이 `rag.py` wrap
- Day 14: `app/rag/pipelines/baseline.py`
