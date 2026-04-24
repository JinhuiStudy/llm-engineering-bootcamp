# 계정 개설 체크리스트

실제로 키 받기까지 순서 + 주의사항. "가입만 해놓으면 된다"가 아니라 "결제카드 붙이고 실제 호출이 되는가" 까지.

## 1. OpenAI (필수)
1. https://platform.openai.com 가입
2. Billing → Add payment method → 카드 등록
3. Auto-recharge 끄고 **수동 $5** 충전 (Day 1-14 총 $10-20 예상)
4. API keys → Create new secret key → **sk-proj-... 전체 복사**
5. `.env`의 `OPENAI_API_KEY=`에 붙여넣기
6. 주의: 결제 반영까지 수 분 걸릴 수 있음. 첫 호출이 429/403이면 10분 뒤 재시도.

## 2. Anthropic (필수)
1. https://console.anthropic.com 가입
2. Plans & Billing → Buy credits → **$5** 구매
3. Settings → API keys → Create key → **sk-ant-... 전체 복사**
4. `.env`의 `ANTHROPIC_API_KEY=`
5. Rate limit 초기에 낮음 (tier 1). Day 9에 eval 돌리면 429 맞을 수 있음 → backoff 필수.

## 3. Google AI Studio (무료)
1. https://aistudio.google.com 가입 (구글 계정)
2. Get API key → Create API key → 기존 GCP 프로젝트 선택 or 새로
3. `.env`의 `GOOGLE_API_KEY=`
4. 주의: 무료 tier는 RPM 제한 빡빡함. 실험용으로만.

## 4. Tavily (Day 5, 옵션)
- 웹 검색 tool 용. 무료 1000 req/mo.
- https://tavily.com/ → Sign up → API key
- 없으면 DuckDuckGo scraping으로 대체 가능 (코드 수정 필요)

## 5. Cohere (Day 8, 옵션)
- 고급 reranker. 무료 trial key.
- https://dashboard.cohere.com/ → API Keys
- 없으면 로컬 cross-encoder로 충분 (오히려 권장)

## 6. Langfuse (Day 12, self-host 권장)
- self-host하면 계정 불필요. `docker compose` 한 줄로 끝.
- Cloud 쓰고 싶으면: https://cloud.langfuse.com (무료 tier 50k obs/mo)

## 7. RunPod (Day 13, 필수)
1. https://www.runpod.io 가입
2. Billing → 카드 등록
3. **최소 $10 충전** (Day 13에 vLLM Serverless endpoint 실험 $3-5)
4. Settings → API keys → Generate → `.env`의 `RUNPOD_API_KEY=`
5. Day 13에 endpoint 만들면서 `RUNPOD_ENDPOINT_ID=` 채우기

## 8. GitHub (최종 포트폴리오 공개용)
1. https://github.com 가입 (이미 있다면 skip)
2. 새 빈 repo `llm-bootcamp-portfolio` (public or private)
3. Day 14 포트폴리오 push용. 지금은 URL만 메모.

## 9. Claude Desktop (Day 11)
- https://claude.ai/download → 설치
- Claude Pro 계정 없어도 MCP 연결 가능 (무료 tier로도 됨)

---

## 예산 요약 (14일 전체)

| 항목 | 예상 | 비고 |
|---|---|---|
| OpenAI | $10-15 | Structured Output, Eval heavy |
| Anthropic | $10-15 | Tool use, Prompt Caching 쓰면 절감 |
| Gemini | $0 | 무료 tier 내 |
| Tavily | $0 | 무료 |
| Cohere | $0 | 옵션/무료 trial |
| Langfuse | $0 | self-host |
| RunPod | $5-10 | Day 13만 |
| **합계** | **$25-40** | |

## 보안 규칙
- `.env` 커밋 절대 금지 (`.gitignore`에 들어 있음)
- API 키 타인 공유 금지
- 유출 즉시: 공급자 대시보드에서 revoke → 새 키 발급
- GitHub에 실수로 올리면: 즉시 revoke (git 히스토리에서 제거해도 이미 노출됨)
