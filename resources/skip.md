# ⏭ 스킵/중복/비효율 자료

> "남들이 추천해도 이 14일 안에선 **보지 말라**"는 리스트.
> 이유 없이 스킵 아니고, **대안이 더 효율적**이거나 **중복**이거나 **구식**이라서.

## ❌ 중복되는 튜토리얼

### LangChain 구 Chain 기반 튜토리얼
- **스킵**: `LLMChain`, `ConversationChain`, `RetrievalQA` 쓰는 2022-2023 자료
- **이유**: LangChain 0.3+ LCEL (`|` pipe) 표준. 구 API deprecated
- **대안**: [LangChain RAG tutorials](https://python.langchain.com/docs/tutorials/rag/)

### OpenAI `text-davinci-003` 예제
- **스킵**: 2024년 retire
- **대안**: `gpt-4o-mini` / `gpt-4o`

### Anthropic Claude 2.x / 3.x 튜토리얼
- **호환 가능**이지만 모델명은 `claude-haiku-4-5` / `claude-sonnet-4-6` / `claude-opus-4-7`로
- **주의**: Prompt Caching / Extended Thinking 등 신기능은 4.x 전용

### 구 Gemini SDK `google-generativeai`
- **스킵**: 레거시
- **대안**: `google-genai` (2024-후반+)

### OpenAI Assistants API
- **스킵**: Responses API로 대체됨 (2024-후반)
- **대안**: [Responses API migration](https://platform.openai.com/docs/guides/migrate-to-responses)

## ❌ 비효율 경로

### CrewAI를 Day 10에
- **스킵**: 2주 안에선 LangGraph로 충분
- **재방문**: [later.md B4](later.md#b4-advanced-agents)

### DSPy / AutoGen
- **스킵**: 개념은 유용하지만 핵심 경로 이탈
- **재방문**: 14일 이후

### "LLM 밑바닥부터" 시리즈 (2h+ 비디오)
- **스킵**: 학술/연구 목적
- **재방문**: 주말 취미

### TensorFlow 기반 자료
- **스킵**: 2026 LLM 생태계는 PyTorch/HF 중심

### 한국어 블로그 검색 기본값
- **스킵**: 공식 문서가 훨씬 최신/정확
- **예외**: 한국어 특화 문제만 (KoNLPy / 한국어 embedding)

## ❌ 과대평가

### "Advanced Prompt Engineering" 장문 블로그들
- 99% Anthropic Interactive Tutorial과 중복
- **대안**: [Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)

### "Top 100 LLM Tools" 류
- 나열식. 실전 의사결정에 무의미

### LLM 비교 벤치마크 포스트
- 빠르게 outdated
- **대안**: [Chatbot Arena](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard)

### "AI의 미래" / "AGI 가능성" 에세이
- 엔지니어링과 무관

## ❌ 기간에 안 맞음

### Fine-tuning 전체
- 2주에 의미있게 불가. LoRA 1회 = 하루
- **재방문**: [later.md B1](later.md#b1-fine-tuning)

### Vision Transformer 원리
- Day 14 이미지 RAG 맛보기 OK, 원리는 later

### RLHF / PPO / DPO 수식
- 2주 밖
- **재방문**: Fine-tuning 파이프라인 구축 시

### 대형 모델 분산 훈련 (Megatron / DeepSpeed)
- inference만 다루는 부트캠프

## ❌ 포맷 비효율

### 4시간 유튜브 라이브 코딩
- **대안**: 블로그 포스트 or 공식 docs

### 1000+ 페이지 종합 서적
- 14일 통독 불가
- **대안**: 목차 훑고 발췌

### Discord / Slack 로그
- 시간 대비 정보 밀도 낮음
- **대안**: GitHub Issues resolved 검색

## 🔒 지금은 절대 손대지 마

### Production 배포 / Kubernetes / IaC
- Day 14는 `docker compose up` 충분

### Custom CUDA / 모델 훈련 최적화
- LLM 연구 영역 (엔지니어링 아님)

### Web3 / AI + Crypto
- 주제 다름

### "Claude로 게임 만들기" 취미
- 14일 후 휴식용

## ⚠️ 지금은 약하게, 나중에 깊게

### Paper 원문 통독
- **지금**: Figure + Abstract + Conclusion만
- **나중**: [later.md B6](later.md#b6-논문-정독)

### LangSmith / Phoenix 깊이
- **지금**: Langfuse 충분
- **나중**: 회사에서 LangChain 생태계면

### Multi-agent
- **지금**: Day 10 개념만
- **나중**: CrewAI / OpenAI Swarm

## 🎯 원칙

1. **공식 문서 > 블로그** — 항상
2. **한 주제에 1개 자료** — 중복 금지
3. **실습 > 읽기** — 1h 읽기 + 2h 실습 >> 2h 읽기
4. **수치로 측정** — Eval 없는 개선은 미신
5. **2주 집중** — 욕심 내면 완주 못함

스킵 리스트 반대 의견은 `notes/decisions.md`에 근거와 함께 기록 후 본인 경로로.
