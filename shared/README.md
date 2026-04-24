# shared/ — 공통 유틸리티 패키지

모든 day-프로젝트가 공유하는 의존성/유틸. `ai_study.*`로 import.

## 설치
```bash
cd shared
uv sync          # 최초
uv sync --upgrade # 의존성 업데이트
```

## 구조
```
shared/
├── pyproject.toml          # 모든 deps (openai/anthropic/gemini/qdrant/langfuse 등)
├── ai_study/
│   ├── __init__.py
│   ├── config.py           # .env 로딩
│   ├── llm.py              # Provider-agnostic chat client
│   ├── tokens.py           # 토큰 카운팅 + 비용 계산
│   ├── logging.py          # loguru 설정
│   ├── retry.py            # tenacity wrapper
│   └── vectors.py          # Qdrant helper
```

## 사용 (각 day 프로젝트에서)
```python
# day별 프로젝트가 shared를 참조하려면 editable install
# 루트에서:
#   uv pip install -e ./shared
# 또는 프로젝트 pyproject.toml에 path dep 추가

from ai_study.llm import chat
from ai_study.tokens import count_tokens, estimate_cost

r = chat("openai", "Say hi")
print(r)
```

## 왜 공통 패키지인가
- 13개 프로젝트가 각자 `load_dotenv()` 반복할 필요 없음
- LLM provider 분기 한 곳에서
- 비용/토큰 계산 일관
- 나중 Day 14 포트폴리오에서 그대로 끌어쓰기
