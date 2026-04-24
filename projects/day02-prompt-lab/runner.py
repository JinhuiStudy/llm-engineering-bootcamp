"""Day 3: Prompt Lab — 10가지 패턴을 동일 태스크에 적용.

사용:
    python runner.py                 # 전체 돌리고 results/에 저장
    python runner.py --pattern cot   # 특정 패턴만
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_study.llm import chat

ROOT = Path(__file__).parent
PROMPTS = ROOT / "prompts"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# 공통 태스크: 고객 이메일에서 불만 + 우선순위 추출
USER_INPUT = """제목: 주문 배송 관련 문의
본문: 지난주 금요일에 주문한 상품이 아직도 안 왔어요. 원래 3일 안에 온다고 했는데 일주일째입니다.
환불 받고 싶고, 앞으로 이 사이트는 안 쓸 것 같네요. 답변 빨리 부탁드립니다."""


def run(pattern_file: Path) -> dict:
    template = pattern_file.read_text(encoding="utf-8")
    prompt = template.replace("{{INPUT}}", USER_INPUT)
    try:
        out = chat("anthropic", prompt, temperature=0.2, max_tokens=800)
    except Exception as e:  # noqa: BLE001
        out = f"ERROR: {e}"
    return {"pattern": pattern_file.stem, "prompt": prompt, "output": out}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", help="특정 패턴 파일명 (확장자 없이)")
    args = parser.parse_args()

    files = sorted(PROMPTS.glob("*.txt"))
    if args.pattern:
        files = [f for f in files if args.pattern in f.stem]
        if not files:
            print("매칭되는 패턴 없음")
            return

    for pf in files:
        r = run(pf)
        out_path = RESULTS / f"{pf.stem}.json"
        out_path.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✔ {pf.stem}")
    print(f"\n→ {RESULTS}")


if __name__ == "__main__":
    main()
