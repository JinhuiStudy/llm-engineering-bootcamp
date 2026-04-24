# Day 7 — 기본 RAG (PDF Q&A v1)

커리큘럼: `curriculum/week1-day07-basic-rag.md`

## 체크리스트
- [ ] RAG From Scratch Part 1-4 노트북 완주
- [ ] `ingest.py` — PDF 파싱(pypdf) → chunk → embed → Qdrant
- [ ] `rag.py` — query → retrieve top-5 → augment prompt → answer
- [ ] 환각 방지 프롬프트 ("모르면 모른다고")
- [ ] 출처 인용 (파일명 + 페이지)
- [ ] `app.py` — CLI 또는 Streamlit
- [ ] 테스트: in-context / not-in-context / paraphrase 각 5개
- [ ] 틀린 케이스 3개 찾아 원인 기록

## Prompt template
```
아래 context에만 근거하여 답하라. 없으면 "모르겠습니다"라고 답하라.
사용한 근거를 [파일명:페이지] 형태로 표시하라.

<context>
{chunks}
</context>

<question>{q}</question>
```

## Stretch
- LlamaIndex로 동일 기능 병행 → 라인 수 비교
- Streaming 답변
