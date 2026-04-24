# Day 1 — LLM 기초 / Transformer 감각 장착

## 목표
- "LLM이 뭐고 왜 이렇게 동작하는지"를 엔지니어 수준으로 설명 가능
- Token, Context window, Temperature, Top-p, Attention, Transformer 핵심어 숙지
- API를 치기 전에 모델의 "입력-출력" 멘탈 모델을 잡는다

## 자료 (우선순위 순)

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [Google ML Crash Course — LLM](https://developers.google.com/machine-learning/crash-course/llm) | 2h |
| 필수 | [Google ML Crash Course — Transformers](https://developers.google.com/machine-learning/crash-course/llm/transformers) | 1h |
| 필수 | Attention Is All You Need — Claude한테 요약 시키고 Figure 1, 2만 봐라 ([arxiv](https://arxiv.org/abs/1706.03762)) | 0.5h |
| 선택 | 3Blue1Brown "But what is a GPT?" 유튜브 | 0.5h |
| 선택 | [Hugging Face NLP course — ch1](https://huggingface.co/learn/nlp-course) | 1h |

## 실습 (3–4h)

### Task 1. 토큰 감각 잡기
```bash
cd /Users/parkjinhui/Desktop/dev/ai-study/projects/day01-chatbot-cli
uv init  # 또는 poetry/venv
uv add tiktoken anthropic openai google-genai python-dotenv
```

- `tokens.py` 작성: "안녕하세요" / "Hello world" / 긴 한글 문단을 각각 tiktoken으로 카운트
- OpenAI, Anthropic, Gemini의 토크나이저 차이 관찰
- 결과를 `notes/concepts.md`에 표로 기록

### Task 2. Temperature / Top-p 실험
- 동일 프롬프트 "Write a haiku about debugging"을 temperature 0 / 0.5 / 1.2로 5번씩 호출
- 결과 다양성 체감
- `notes/daily-log.md`에 관찰 기록

## 체크리스트

- [ ] Transformer의 encoder/decoder 차이를 한 문장으로 설명 가능
- [ ] "Self-attention이 왜 필요한가"를 설명 가능
- [ ] Token이 글자/단어가 아니라는 걸 실제로 확인
- [ ] `.env`에 3사 API 키 다 넣음
- [ ] `notes/keywords.md`에 용어 10개 이상 정리
- [ ] `daily-log.md`에 "오늘 가장 헷갈린 것" 1줄 기록

## 산출물
- `projects/day01-chatbot-cli/tokens.py`
- `projects/day01-chatbot-cli/temperature_demo.py`
- `notes/keywords.md` 에 token, context window, temperature, top-p, top-k, sampling, attention, self-attention, decoder-only, encoder-decoder, logit, softmax 정리
