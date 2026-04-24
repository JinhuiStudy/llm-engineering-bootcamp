# Day 1-2 — 3-Provider CLI Chatbot

커리큘럼: `curriculum/week1-day01-llm-basics.md`, `week1-day02-api-providers.md`

## 체크리스트
- [ ] `uv init` + deps (openai, anthropic, google-genai, tiktoken, python-dotenv)
- [ ] `.env`에 3사 API key
- [ ] `tokens.py` — tiktoken으로 토큰 카운트 실험
- [ ] `temperature_demo.py` — temperature 0/0.5/1.2 비교
- [ ] `providers/base.py` — Provider 인터페이스
- [ ] `providers/openai_client.py` / `anthropic_client.py` / `gemini_client.py`
- [ ] `chat.py` — CLI (--provider, --stream, multi-turn, token usage)
- [ ] `--compare` 모드 (동일 쿼리 3사 동시)
- [ ] Rate limit error 관찰 기록

## 확장 아이디어
- 대화 저장/복원 (json)
- 모델 스위치 (Sonnet/Haiku, GPT-4o/mini)
