# Prompt Patterns 치트시트

패턴 10가지 + 언제 쓰고 언제 피해야 하는가.

## 1. Zero-shot
```
Classify the sentiment of this review: "The food was okay."
```
- 👍 간단한 태스크, 모델이 이미 잘 하는 것
- 👎 도메인 특수 포맷 필요할 때

## 2. Few-shot
```
Review: "Loved it" → positive
Review: "Terrible" → negative
Review: "Meh" → ?
```
- 👍 특정 포맷/스타일 고정, 도메인 edge case 예시
- 👎 토큰 낭비, 예시 2-5개면 충분 (더 늘려도 수익 체감)

## 3. Chain-of-Thought (CoT)
```
Solve step by step: If a train leaves at 2pm ...
```
- 👍 수학/추론 문제
- 👎 프로덕션 user-facing 출력 (UX 망가짐). **내부 reasoning**은 분리해야.
- Anthropic: `<thinking>` 태그로 분리 권장

## 4. Role prompting
```
You are a senior security auditor. Review this code for vulnerabilities.
```
- 👍 스타일/전문성 고정
- 👎 role만으로 능력이 생기지는 않음. 구체적 지시와 병행 필요.

## 5. XML structured (Anthropic 권장)
```
<context>{docs}</context>
<question>{q}</question>
<output_format>JSON with keys: answer, confidence</output_format>
```
- 👍 Claude에서 특히 강력. 입력 부위 명확히 구분.
- 👎 OpenAI에서는 불필요한 경우 있음 (JSON Schema 사용)

## 6. Prefill (Anthropic 전용 트릭)
```
assistant: {  ← 이렇게 시작 글자 넣어두면 JSON 강제
```
- 👍 JSON/특정 접두어 출력 강제
- 👎 OpenAI는 이 방식 지원 안 함

## 7. Delimiter
```
Analyze the text below.
###
{text}
###
```
- 👍 사용자 입력 경계 분리 (prompt injection 완화)
- 👎 모델이 구분자 자체를 출력에 포함하는 실수

## 8. Self-critique
```
First draft an answer.
Then critique it.
Then rewrite.
```
- 👍 품질이 낮으면 자주 쓸 가치 있음 (특히 작은 모델)
- 👎 3배 토큰. 가성비 나쁠 때 많음.

## 9. Chain of Density (요약용)
여러 번 반복하며 정보 밀도 점점 높이기. 요약 태스크 특화.
- 👍 긴 문서 요약
- 👎 범용성 낮음

## 10. Negative instruction
```
Do NOT include any markdown formatting.
Do NOT start with "Sure, here is".
```
- 👍 특정 나쁜 습관 제거
- 👎 "don't think of X"는 오히려 X를 생각하게 할 수 있음 — 긍정형으로 바꾸는 게 보통 낫다

---

## 디버깅 체크리스트 (프롬프트가 안 먹을 때)
- [ ] 지시가 서로 모순되지 않나
- [ ] Few-shot 예시가 원하는 포맷과 정확히 일치하나
- [ ] 입력/맥락/지시가 구분자로 분리됐나
- [ ] Temperature가 태스크에 맞나 (structured=0)
- [ ] max_tokens가 너무 작지 않나
- [ ] 더 큰 모델로 바꾸면 해결되나 (그럼 프롬프트 문제 아님)
- [ ] 역순 (지시를 prompt 끝에) 해봤나 — 긴 컨텍스트에서 "lost in the middle" 대비
- [ ] Structured output으로 강제했나

## Provider별 주의점

| | OpenAI | Anthropic | Gemini |
|---|---|---|---|
| System prompt | messages[0] | top-level `system` | system_instruction |
| Prefill | ❌ | ✅ | ❌ |
| XML tag 선호 | 중립 | **강하게 선호** | 중립 |
| JSON 강제 | `response_format` | `tool_use` 트릭 or strict SO | `response_schema` |
| Role 이름 | system/user/assistant | user/assistant only | user/model |

## 우선 시도 순서
1. Zero-shot + 명확한 지시
2. XML/delimiter로 입력 구조화
3. Few-shot (2-5개)
4. Structured output 강제
5. (필요 시) CoT
6. (필요 시) Self-critique
7. 아직도 안 되면 모델 교체 또는 RAG/tool 추가
