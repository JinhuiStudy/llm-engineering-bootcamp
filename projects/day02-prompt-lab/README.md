# Day 3 — Prompt Lab

커리큘럼: `curriculum/week1-day03-prompt-engineering.md`

10가지 프롬프트 패턴을 **동일한 태스크**에 적용해 결과를 비교하는 연구실.

## 체크리스트
- [ ] Anthropic Interactive Tutorial 9챕터 완주 (`notebooks/` 안에 실행 기록)
- [ ] `prompts/01-zero-shot.txt` ~ `10-negative.txt` 작성
- [ ] 공통 태스크 정의: 이메일 → 불만사항+우선순위 추출
- [ ] `runner.py` — 각 prompt를 동일 input에 적용, 결과 `results/`에 JSON 저장
- [ ] `README.md`에 각 패턴의 강점/약점 1줄씩
- [ ] 가장 잘 먹은 패턴 top 3와 이유

## 공통 태스크 예시 input
```
제목: 주문 배송 관련 문의
본문: 지난주 금요일에 주문한 상품이 아직도 안 왔어요. 원래 3일 안에 온다고 했는데 일주일째입니다. 환불 받고 싶고, 앞으로 이 사이트는 안 쓸 것 같네요. 답변 빨리 부탁드립니다.
```

Expected output: 불만 목록, 우선순위, 권장 대응
