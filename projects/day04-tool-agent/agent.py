"""Day 5: Anthropic tool-use agent loop."""

from __future__ import annotations

import json
import sys

import anthropic

from ai_study.config import settings
from ai_study.logging import logger
from tools import dispatch
from tools_schema import TOOLS

MAX_ITER = 10


def run(user_msg: str) -> str:
    client = anthropic.Anthropic()
    messages: list[dict] = [{"role": "user", "content": user_msg}]

    for step in range(MAX_ITER):
        logger.info(f"── step {step + 1} ──")
        r = client.messages.create(
            model=settings.anthropic_model,
            max_tokens=2048,
            tools=TOOLS,
            messages=messages,
        )

        # append assistant turn
        messages.append({"role": "assistant", "content": r.content})

        if r.stop_reason == "end_turn":
            # final text
            texts = [b.text for b in r.content if getattr(b, "type", "") == "text"]
            return "\n".join(texts)

        if r.stop_reason == "tool_use":
            tool_results = []
            for block in r.content:
                if getattr(block, "type", "") != "tool_use":
                    continue
                logger.info(f"tool: {block.name}({json.dumps(block.input, ensure_ascii=False)})")
                result = dispatch(block.name, block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False, default=str),
                    }
                )
            messages.append({"role": "user", "content": tool_results})
            continue

        return f"<unexpected stop_reason={r.stop_reason}>"

    return "<max iterations reached>"


if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or "서울 현재 날씨를 알려주고 섭씨를 화씨로 변환해줘."
    print(run(msg))
