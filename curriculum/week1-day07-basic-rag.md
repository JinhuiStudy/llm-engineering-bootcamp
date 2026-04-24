# Day 7 — 기본 RAG + Vision/Multi-modal RAG (Week 1 피날레 ULTRA)

> **난이도**: ★★★★★ (v3 상향)
> **총량**: RAG 9h + Vision RAG 2h + 정리 1h = **12h**.
> **Week 1 총결산** + Multi-modal 진입점.
> **논문**: Lost in the Middle (Liu 2023)

## 🎯 오늘 끝나면

1. RAG 7단계 flow(**Load → Split → Embed → Store → Retrieve → Augment → Generate**)를 **외우지 말고 설명**할 수 있음
2. PDF/Markdown/HTML 소스 → 인덱스 → Q&A가 end-to-end로 동작하는 v1 봇
3. **환각 방지 3종세트**: "근거 없으면 모른다고 답" 프롬프트 + citation 의무화 + LLM이 "어떤 chunk를 썼는지" 명시
4. LangChain vs LlamaIndex vs "직접 짜기" 3가지를 모두 경험해 각자의 비용/유연성 감각
5. **정답셋 20개**를 직접 만들어 내일 eval 준비 (이게 진짜 중요)

## 📚 자료

### 🔥 오늘의 메인 (3h)

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 2h | [RAG From Scratch — GitHub repo (langchain-ai)](https://github.com/langchain-ai/rag-from-scratch) | **15개 notebook 중 Part 1-4**. 각 notebook 15-30분. Part 1(Overview) → 2(Indexing) → 3(Retrieval) → 4(Generation). Part 5+는 내일 Day 8에. |
| 1h | [RAG From Scratch YouTube — Part 1-4](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x) | 영상 버전. 1.5배속 권장. Lance Martin의 코드 라이브 설명. |

### 🔥 필수

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 1h | [LlamaIndex — Understanding RAG](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) | LlamaIndex의 추상화(Node / Index / Retriever / QueryEngine / Response)를 한 번 보고 감 잡기. LangChain 대비 장단. |
| 30m | [OpenAI Cookbook — Q&A using embeddings](https://cookbook.openai.com/examples/question_answering_using_embeddings) | "프레임워크 없이" 직접 짜기. 코드 300줄. 오늘 자기 구현의 레퍼런스. |
| 30m | [OpenAI Cookbook — Parse PDF docs for RAG](https://cookbook.openai.com/examples/parse_pdf_docs_for_rag) | PDF 파싱 수준 3단계 비교. pypdf(순) / pdfplumber(표) / Unstructured(OCR). |

### ⭐ 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [LangChain RAG tutorials — build retrieval chain](https://python.langchain.com/docs/tutorials/rag/) | LCEL (LangChain Expression Language) pipe 문법. 2024-2026 표준. |
| 30m | [LlamaIndex — building a RAG pipeline](https://docs.llamaindex.ai/en/stable/examples/pipeline/query_pipeline/) | pipeline 조립 방식. LangChain LCEL과 비교. |
| 30m | [Weaviate — RAG 101](https://weaviate.io/blog/introduction-to-rag) | 개념/비용/성능 정리. 벤더 중립적 서술. |

### 🎓 선택

- [Haystack docs — RAG pipeline](https://docs.haystack.deepset.ai/docs/rag-pipeline) — deepset의 프레임워크 구경.
- [RAG paper (Lewis et al. 2020)](https://arxiv.org/abs/2005.11401) — RAG라는 용어의 원조. Figure 1, Abstract만.
- [Lost in the Middle paper](https://arxiv.org/abs/2307.03172) — 긴 context 중간 무시 현상. Top-k 배치 전략에 영향.

## 🔬 실습 (5.5h)

### 프로젝트: PDF Q&A 봇 v1 + 정답셋 20개

위치: `projects/day06-basic-rag/`

```
day06-basic-rag/
├── docker-compose.yml       # Qdrant (infra/ 재활용)
├── app/
│   ├── ingest.py            # PDF → text → chunk → embed → upsert
│   ├── retrieve.py          # top-k + score threshold + reranker 스위치
│   ├── augment.py           # context assembly (re-order, deduplicate, truncate)
│   ├── generate.py          # LLM 호출 + citation 추출
│   ├── rag.py               # 전체 파이프라인 조립
│   └── cli.py               # CLI interface
├── implementations/
│   ├── from_scratch.py      # 프레임워크 없이 직접 (OpenAI SDK + Qdrant client)
│   ├── with_langchain.py    # LCEL
│   └── with_llamaindex.py   # VectorStoreIndex + QueryEngine
├── prompts/
│   ├── rag_system.txt
│   └── rag_user.txt
├── data/
│   └── pdfs/                # 기술문서 5개 (회사 문서, arxiv 논문, 툴 매뉴얼)
├── eval/
│   ├── qa_pairs.json        # 20개 수기 작성
│   └── make_golden.py       # 수기 정답셋 생성 도우미 (semi-auto)
└── README.md
```

### 🔥 필수 기능

1. **PDF 파싱 3단계**:
   - pypdf (빠름/단순) — 기본
   - pdfplumber (표) — fallback
   - Unstructured (스캔/이미지) — last resort + vision
2. **Chunking**: `RecursiveCharacterTextSplitter` (LangChain) with `chunk_size=500`, `chunk_overlap=50`. separators에 `"\n\n"`, `"\n"`, `". "`, `" "`
3. **Embedding**: OpenAI `text-embedding-3-small` (빠르고 싸고 충분히 좋음)
4. **Vector store**: Qdrant (Day 6 collection 재사용 or 새로 만들기)
5. **Retrieve**: top-k=5, score threshold 옵션
6. **Prompt**:
   ```
   <role>You are a precise RAG assistant. Answer ONLY from <context>.</role>
   <rules>
     1. If the answer is not in the context, reply: "근거 부족으로 답변 불가."
     2. Every factual claim must have a citation like [1], [2] referring to <context> entries.
     3. Do not use any external knowledge.
   </rules>
   <context>
   [1] file="foo.pdf" page=3: {chunk_text}
   [2] file="bar.md" section=2: ...
   </context>
   <question>{q}</question>
   ```
7. **Citation 추출** — 답변에서 `[1]`, `[2]` 패턴 파싱 → 해당 chunk의 file/page로 매핑 → 응답에 `sources` 필드 포함
8. **3가지 구현** 모두 만들고 라인 수 / 가독성 / 유연성 비교:
   - `from_scratch.py` (200-400 lines)
   - `with_langchain.py` (50-100 lines)
   - `with_llamaindex.py` (30-80 lines)

### 🔥 정답셋 20개 만들기 (30m 이상 투자)

**내일 Day 9 eval의 기반**. 품질이 곧 eval 품질이다.

`eval/qa_pairs.json` 구조:
```json
[
  {
    "id": "q001",
    "question": "qdrant-client로 collection 생성 시 distance 옵션의 기본값은?",
    "ground_truth": "COSINE",
    "source_doc": "qdrant_tutorial.pdf",
    "source_page": 4,
    "category": "factual",
    "difficulty": "easy"
  },
  {
    "id": "q002",
    "question": "RAG에서 chunk overlap을 늘리면 어떤 trade-off?",
    "ground_truth": "맥락 보존 ↑, 중복/비용 ↑, 인덱스 크기 ↑",
    "source_doc": "...",
    "category": "synthesis",   
    "difficulty": "medium"
  },
  {
    "id": "q003",
    "question": "이 문서에 안 나오는 것: 1998년 삼성 반도체 매출",
    "ground_truth": "근거 부족으로 답변 불가",
    "category": "unanswerable",
    "difficulty": "easy"
  }
]
```

**카테고리 분포 권장**:
- factual (단일 chunk 답): 8
- synthesis (여러 chunk 종합): 5
- reasoning (추론): 3
- unanswerable (없는 정보): 2
- adversarial (prompt injection, ambiguous): 2

### 🔥 Stretch

- 🧪 **Streaming 답변** — SSE로 토큰 단위 출력 + citation은 마지막에 붙이기
- 🧪 **Metadata filter** — "PDF 파일 중 2024년 이후 문서만"
- 🧪 **Context re-order** — top-5 결과를 "Lost in the Middle" 피해 고려해 `[가장 중요, ..., 가장 중요]` U자 배치
- 🧪 **PDF 이미지 페이지 처리** — GPT-4o Vision / Claude Vision으로 표/차트 있는 페이지를 이미지로 전달
- 🧪 **LCEL vs 직접 짜기 성능 측정** — 10 쿼리 병렬 호출 시 latency 차이

## ⚖️ 품질 기준 (스스로 채점)

| 항목 | 기준 |
|---|---|
| Context에 있는 사실 질문 정답률 | 90%+ |
| Context에 없는 질문에 "모른다" 응답 | 80%+ |
| Citation 포함률 | 95%+ |
| Citation 정확률 (실제 해당 chunk가 근거) | 85%+ |
| 응답 latency (top-k=5, 4o-mini) | <3s |

내일 Ragas로 숫자화하면 이 기준이 맞았는지 객관 측정.

## ✅ 체크리스트

- [ ] 3가지 구현(from_scratch / langchain / llamaindex) 모두 동작
- [ ] RAG 7단계를 그림으로 본인 노트에 그림
- [ ] 환각 방지 프롬프트 실제 효과 확인 (context 없는 질문에 "모른다"로 80%+)
- [ ] Citation 1개 이상 포함된 답변 생성 확인
- [ ] 정답셋 20건 작성 완료 (카테고리 분포 준수)
- [ ] LangChain LCEL 파이프 `|` 문법 이해
- [ ] LlamaIndex QueryEngine 구조 이해
- [ ] "하드케이스" 3개 기록 (틀린 케이스 + 왜 틀렸는지)
- [ ] `cheatsheets/rag-patterns.md` 본인 수치/관찰 반영

## 🧨 자주 틀리는 개념

1. **"RAG = embedding search + LLM"** — 맞는데, **실제 품질의 80%는 chunk 설계 + prompt + eval**. retrieval은 20%.
2. **"Top-k 크게 할수록 좋다"** — context 오염 + Lost-in-Middle + 비용 증가. k=5가 기본 좋음. k=20+는 rerank 전제.
3. **"LangChain 있으면 다 됨"** — LangChain 자체 버그 + 업데이트 파괴적 변경 잦음. **원리 모르고 쓰면 디버깅 지옥**. 오늘 `from_scratch.py` 필수.
4. **"citation 프롬프트 시키면 됨"** — 시킨다고 잘 따르지 않음. `response_format=Pydantic(answer, citations: list[int])`로 강제해야 안정.
5. **"긴 문서는 chunk 크게"** — 반대. 문서 길이와 chunk 크기는 별개. 정보 밀도 기준.
6. **"답변에 context를 다 붙여야 안전"** — 토큰 낭비 + 모델이 "근거 없으면 모른다고" 못 지키게 됨 (compliance ↓).

## 🧪 산출물

- `projects/day06-basic-rag/` — 전체 완성, 3가지 구현
- `eval/qa_pairs.json` — 20건 (카테고리 분포 준수) — 내일 Day 9 입력
- `results/compare.md` — 3구현 라인 수/latency/가독성 비교
- `notes/daily-log.md` — Week 1 회고: "가장 어려웠던 날 + 가장 의외였던 인사이트"

## 📌 핵심 키워드

- RAG = Retrieval Augmented Generation
- 7단계 flow: Load → Split → Embed → Store → Retrieve → Augment → Generate
- Context window budget, token stuffing
- Citation / grounding / source attribution
- Retriever (dense / sparse / hybrid)
- Augment 단계: deduplication, re-ordering, truncation
- Prompt template, system/user role
- Framework: LangChain (LCEL), LlamaIndex (QueryEngine), Haystack, 직접 짜기
- Pydantic answer schema with citations
- Hallucination, groundedness, faithfulness
- Lost in the Middle

## 🏁 Week 1 종료 회고 (notes/daily-log.md)

Day 1 → Day 7까지 무엇을 할 수 있게 됐는가? 자가진단 [`self-check.md`](self-check.md) 섹션 1-7 체크. 3개 이상 답 못하면 내일 오전 1시간 복습.

**Week 2는 본격 고급 + production. 난이도 급상승.** 오늘은 반드시 **0시 전에 잠**.

## 🖼 v3 추가 — Vision / Multi-modal RAG (2h)

### 🔗 자료
- [OpenAI Vision](https://platform.openai.com/docs/guides/vision) — 4o Vision으로 이미지 + 텍스트 query
- [Anthropic Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision) — Claude 4.x가 Vision에 강함
- [Gemini multimodal](https://ai.google.dev/gemini-api/docs/vision) — 2026 Vision 최강
- [Google Multimodal RAG codelab](https://codelabs.developers.google.com/multimodal-rag-gemini) — step-by-step 90분 실습
- [GCP multimodal RAG notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/use-cases/retrieval-augmented-generation/intro_multimodal_rag.ipynb) — 코드 레퍼런스

### 🔥 필수 구현

기존 `day06-basic-rag/`에 추가:
```
day06-basic-rag/
├── vision/
│   ├── pdf_page_images.py     # pypdf로 텍스트 뽑고 실패 시 페이지 → PNG 렌더
│   ├── vision_rag.py          # 이미지 chunk를 4o Vision에 넘김
│   └── chart_extraction.py    # 표/차트가 있는 페이지를 Vision으로 텍스트화
├── samples/
│   └── pdfs_with_charts/      # 표/차트 있는 PDF 3개 (arxiv / GPU 스펙시트 등)
```

1. PDF 페이지를 `pdf2image` or `pypdf` + `Pillow`로 PNG 렌더
2. 텍스트 추출 실패/약함 감지 → Vision API fallback
3. 이미지를 base64 인코딩 → Vision 모델에 "이 페이지의 정보를 텍스트로 추출" prompt
4. 추출된 텍스트를 일반 RAG pipeline으로 인덱싱
5. 정답셋 확장: "표 4에서 H100 메모리 대역폭?" 같은 vision-required 쿼리 5개

### 📊 비교
| 방식 | 정확도 | 비용 | latency |
|---|---|---|---|
| pypdf only | baseline | $0 | 빠름 |
| pypdf + Vision fallback | +20-40% | 10x | 3-5x |
| Vision only (모든 페이지) | +30-50% | 20x | 5-10x |

**실전 권장**: pypdf 먼저 → confidence 낮거나 표/이미지 키워드 포함 시 Vision fallback

## 📜 논문 — Lost in the Middle (30m)
- [arxiv](https://arxiv.org/abs/2307.03172)
- Figure 1: U-shape accuracy curve (context 앞/뒤는 잘 보고 중간 놓침)
- **대응**: augment 단계에서 중요 chunk를 **앞+뒤 양끝**에 배치 (U-shape 방어)
- 본인 코드 `app/augment.py`의 `reorder_for_lost_in_middle` 반영

## 🎁 내일(Day 8) 미리보기
Advanced RAG — Query rewriting / HyDE / Multi-query / Hybrid / Rerank + **논문 3편** (RAPTOR / ColBERT / Anthropic Contextual Retrieval).
