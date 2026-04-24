# Day 5 — 멀티툴 에이전트

커리큘럼: `curriculum/week1-day05-function-calling.md`

## 체크리스트
- [ ] Anthropic `tool_use` 코스 6강 노트북 완주
- [ ] `tools/` 4개: weather, calculator, web_search, file_io
- [ ] `tools_schema.py` — JSON schema 정의
- [ ] `agent.py` — tool loop (call → execute → result → next)
- [ ] 최대 반복 10회 제한
- [ ] Tool error → 에러 메시지를 tool_result로 (재시도 가능하게)
- [ ] Parallel tool use 케이스 확인
- [ ] `tool_choice` 옵션 실험 (auto/any/specific)
- [ ] 로그 JSON으로 저장 (Day 12 Langfuse 연결용)

## 테스트 쿼리
1. "서울 날씨 알려주고 화씨로 변환"
2. "오늘 AI 뉴스 3개 요약"
3. "tools/ 디렉토리 목록"
4. 무한 루프 유발 시도 (방어 확인)
