# Day 3 — Prompt Engineering (하드코어 날)

## 목표
- Anthropic Interactive Prompt Tutorial 9챕터 전부 통과
- Prompt 패턴 10가지 체화: role, few-shot, CoT, structured, XML tags, prefill, delimiter, negative instruction, example-driven, self-critique
- "프롬프트가 안 먹을 때 뭘 손봐야 하는지" 직관 확보

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [Anthropic Interactive Prompt Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) — **오늘의 메인**. 9챕터 + 연습문제 전부 | 4h |
| 필수 | [Anthropic prompt-engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) | 1h |
| 필수 | [Prompting Guide — techniques](https://www.promptingguide.ai/techniques) | 1h |
| 선택 | [OpenAI Cookbook — prompting examples 2개](https://cookbook.openai.com/) | 1h |
| 선택 | [Prompting Guide — applications](https://www.promptingguide.ai/applications) | 후일 |

## 실습 (3h)

### 프로젝트: Prompt Lab
위치: `projects/day02-prompt-lab/`

```
day02-prompt-lab/
├── prompts/
│   ├── 01-zero-shot.txt
│   ├── 02-few-shot.txt
│   ├── 03-cot.txt
│   ├── 04-role-play.txt
│   ├── 05-xml-structured.txt
│   ├── 06-prefill.txt
│   ├── 07-self-critique.txt
│   ├── 08-chain-of-density.txt
│   ├── 09-delimiter.txt
│   └── 10-negative.txt
├── runner.py            # 각 프롬프트를 동일 task에 적용해서 결과 비교
├── results/             # 결과 저장
└── README.md            # 각 패턴의 효과 관찰 기록
```

### 과제
- 공통 태스크: "다음 이메일에서 불만 사항과 우선순위를 뽑아라"
- 10가지 패턴을 동일 태스크에 적용
- 결과를 `results/`에 저장하고 어떤 패턴이 가장 잘 먹었는지 `README.md`에 기록
- **중요**: 한 패턴이라도 실패하면 왜 실패했는지 기록

## 체크리스트

- [ ] Anthropic 튜토리얼 9챕터 모두 완주 + 연습문제 풀이
- [ ] XML 태그 프롬프트의 장점 설명 가능 (`<context>` 등)
- [ ] Prefill 기법 실제로 작성 (assistant 메시지를 `{` 로 시작시키기)
- [ ] CoT와 "answer first" 의 차이를 설명 가능
- [ ] `cheatsheets/prompt-patterns.md` 10가지 패턴 요약

## 핵심 키워드
- zero-shot, few-shot, CoT (chain-of-thought), role prompting, system vs user instruction
- prefill, delimiter, XML tags, structured input, example-driven
- self-critique, self-consistency, least-to-most, tree-of-thought (이름만 알기)
- Prompt injection, jailbreak (개념만)

## 주의
- CoT를 production 앱에 그대로 노출하지 말 것 — reasoning을 user-facing 출력으로 쓰면 UX 망가지고 토큰 낭비. 내부 reasoning과 최종 답을 분리 설계.
