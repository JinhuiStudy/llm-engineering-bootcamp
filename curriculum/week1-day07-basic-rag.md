# Day 7 — 기본 RAG 파이프라인

## 목표
- RAG의 전체 flow (Load → Split → Embed → Store → Retrieve → Augment → Generate) 직접 구현
- LangChain RAG From Scratch Part 1-4 완주
- LlamaIndex와 LangChain의 접근 차이 감각

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [LangChain — RAG From Scratch (repo)](https://github.com/langchain-ai/rag-from-scratch) | 2h |
| 필수 | [RAG From Scratch YouTube playlist — Part 1-4](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x) | 1.5h |
| 필수 | [LlamaIndex — Understanding RAG](https://developers.llamaindex.ai/python/framework/understanding/rag/) | 1.5h |
| 필수 | [OpenAI Cookbook — Question answering using embeddings](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb) | 1h |
| 선택 | [OpenAI — Parse PDF docs for RAG cookbook](https://developers.openai.com/cookbook/examples/parse_pdf_docs_for_rag) | 1h |
| 선택 | [Weaviate — Starter Guides / Generative](https://docs.weaviate.io/weaviate/starter-guides/generative) | 1h |

## 실습 (5h — 오늘 집중)

### 프로젝트: PDF Q&A 봇 v1
위치: `projects/day06-basic-rag/`

```
day06-basic-rag/
├── docker-compose.yml
├── ingest.py           # PDF → text → chunk → embed → Qdrant
├── rag.py              # query → retrieve → build prompt → LLM answer
├── app.py              # CLI 또는 간단한 Streamlit/FastAPI
├── data/
│   └── pdfs/           # 기술 문서 3-5개 (회사 문서, arxiv 논문 등)
├── prompts/
│   └── rag_template.txt
└── README.md
```

### 요구사항
1. PDF 파싱: `pypdf` 또는 `unstructured` (표/이미지 있으면 후자)
2. Chunking: `RecursiveCharacterTextSplitter` (LangChain) 또는 직접 구현
3. Embedding: OpenAI `text-embedding-3-small`
4. Vector store: Qdrant (Day 6 그대로 이어서)
5. Retrieval: top-k=5
6. Prompt template:
   ```
   아래 context를 근거로만 답하라. 모르면 "모르겠다"고 답하라.
   <context>{chunks}</context>
   <question>{q}</question>
   ```
7. **출처 표시**: 답변에 사용된 chunk의 문서명 + 페이지를 함께 출력

### 테스트 케이스
- Context에 있는 정보 묻기 → 맞춰야 함
- Context에 없는 정보 묻기 → "모르겠다" 답해야 함 (환각 방지 확인)
- 같은 의미 다른 표현의 쿼리 (paraphrase) → 잘 찾아야 함

### Stretch
- LlamaIndex로 동일 기능 구현 → 코드 라인 수 비교
- Streaming으로 답변 출력

## 체크리스트

- [ ] RAG 7단계 flow를 화이트보드 없이 설명 가능
- [ ] 환각 방지 프롬프트 패턴 확보 ("근거가 없으면 모른다고 답하라")
- [ ] 출처 표시 동작
- [ ] 정답이 틀린 케이스 최소 3개 찾고 이유 기록 (chunk 쪼개기 실패? embedding 부족? prompt 부족?)
- [ ] LangChain vs LlamaIndex 차이 한 줄 정리

## 핵심 키워드
- RAG flow: load → split → embed → store → retrieve → augment → generate
- context window 관리, token budget, prompt stuffing
- source citation, grounded answer, hallucination
- Retriever, Reader (old QA 용어지만 개념은 유효)
- LangChain: `Document`, `Retriever`, `Chain` / LlamaIndex: `Node`, `Index`, `QueryEngine`

## 이번 주 마무리
- Week 1 회고: `notes/daily-log.md` 에 "가장 어려웠던 것 / 가장 재미있었던 것" 2줄
- Week 2부터는 본격 고급 + production. 쉽지 않으니 오늘 컨디션 조절
