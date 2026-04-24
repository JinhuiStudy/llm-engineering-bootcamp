# 나머지 7개 패턴 template 작성 가이드

3개는 샘플로 있음 (01, 03, 05). 나머지는 직접 작성:

- `02-few-shot.txt` — 예시 2-3개 삽입 후 `{{INPUT}}` 넘기기
- `04-role-play.txt` — "You are a senior customer success manager..."로 시작
- `06-prefill.txt` — Anthropic 전용. assistant 메시지를 `{`로 prefill 하도록 runner.py 수정
- `07-self-critique.txt` — "먼저 답 → 비평 → 재작성" 3단계
- `08-chain-of-density.txt` — 요약을 3번 반복하며 정보 밀도 높이기
- `09-delimiter.txt` — `###` 구분자로 입력 경계
- `10-negative.txt` — "Do NOT include markdown. Do NOT start with 'Sure,...'"

각 template은 반드시 `{{INPUT}}` placeholder 포함.

실행 후 `results/` 의 JSON들을 비교하며 어떤 패턴이 가장 정확한지/짧은지/구조화되었는지 `README.md`에 기록.
