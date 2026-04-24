"""Day 5: Tool 정의 (Anthropic 포맷).

OpenAI/Gemini용 변환은 각 provider 코드에서.
"""

from __future__ import annotations

TOOLS = [
    {
        "name": "get_weather",
        "description": "현재 날씨 조회. 도시 이름을 받아 섭씨 온도와 상태를 반환.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "영어/한글 도시명"},
            },
            "required": ["city"],
        },
    },
    {
        "name": "calculator",
        "description": "수식 평가. 사칙연산/괄호/지수 지원.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "e.g. '(3+4)*2'"},
            },
            "required": ["expression"],
        },
    },
    {
        "name": "web_search",
        "description": "웹 검색. 쿼리로 상위 결과 요약을 받아옴.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "default": 3},
            },
            "required": ["query"],
        },
    },
    {
        "name": "list_files",
        "description": "디렉토리 안 파일 목록.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "절대 경로 권장"},
            },
            "required": ["path"],
        },
    },
]
