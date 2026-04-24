# 계정 개설 체크리스트 (2026-04 기준)

> "가입만 해놓으면 된다"가 아니라 **결제 카드 붙이고 실제 호출 200 응답**까지.
> 순서대로 하면 30-60분. VPN/프록시 뒤에서는 좀 더 걸림.

## 💳 결제 보안 규칙 (먼저 읽어)

- **Auto-recharge OFF** — 수동 충전만. (학습 중 잠든 agent가 $수백 태울 수 있음)
- **일일 Usage limit** 설정 — OpenAI/Anthropic 대시보드에서 $5-10 설정
- **카드 별도 발급 권장** — 학습 전용 가상/선불 카드 (한도 $50)
- **.env 절대 커밋 금지** — `.gitignore` 재확인. 실수 시 즉시 키 revoke

---

## 1️⃣ OpenAI (필수, 14일 $10-15)

1. https://platform.openai.com/signup 가입
2. **Billing → Add payment method** → 카드 등록
3. **Usage limits → Hard limit $20** 설정 (safety)
4. **Credit balance → Add $5** 수동 충전 (auto-recharge OFF)
5. **API keys → Create new secret key (Project)** → `sk-proj-...` 전체 복사 (한 번만 볼 수 있음)
6. `.env`의 `OPENAI_API_KEY=sk-proj-...`
7. 반영까지 수 분 대기 (429/403 뜨면 10분 뒤 재시도)
8. 확인: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY" | head`

**모델 접근**
- 기본 tier에서 `gpt-4o`, `gpt-4o-mini` 접근 가능
- **o-series (o1/o3 계열)** 는 사용량 누적 필요할 수 있음
- Organization 여러 개면 default 확인

## 2️⃣ Anthropic (필수, 14일 $10-15)

1. https://console.anthropic.com 가입
2. **Plans & Billing → Buy credits → $5**
3. **Settings → Spend limits → $20/mo**
4. **Settings → API keys → Create Key** → `sk-ant-...` 복사
5. `.env`의 `ANTHROPIC_API_KEY=sk-ant-...`
6. 확인: `curl https://api.anthropic.com/v1/models -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" | head`

**Tier / Rate Limit**
- 초기 tier 1 (RPM 50, TPM 50k) — Day 9 eval 대량 호출 시 429 가능
- 충전 누적 + 시간 지나면 tier 2/3 자동 상승
- **Prompt Caching** 적극 활용 → 토큰 비용 90% 절감

**모델 선택 (2026-04)**
- `claude-opus-4-7` — flagship
- `claude-sonnet-4-6` — workhorse
- `claude-haiku-4-5` — 빠른/저렴 (default)

## 3️⃣ Google AI Studio (필수, $0)

1. https://aistudio.google.com 접속 (구글 계정)
2. **Get API key → Create API key**
3. 기존 GCP 프로젝트 선택 또는 새로
4. `.env`의 `GOOGLE_API_KEY=AIza...`
5. 확인: curl `https://generativelanguage.googleapis.com/v1beta/models?key=$GOOGLE_API_KEY`

**Free tier 제한 (2026)**
- RPM 15 (flash), 2 (pro)
- 실험용으로만 충분. 대량 호출은 Vertex AI로 결제 연동
- **Safety filter 엄격함** — 응답이 빈 content면 finish_reason `SAFETY` 체크

## 4️⃣ Voyage AI (선택, Day 6 embedding)

- Anthropic 공식 권장 임베딩. 무료 credit 제공
- https://www.voyageai.com/ → Dashboard → API key
- `.env`의 `VOYAGE_API_KEY=pa-...`
- OpenAI `text-embedding-3`로 대체 가능

## 5️⃣ Tavily (선택, Day 5 web search)

- 무료 1000 req/month
- https://tavily.com/ → Sign up → API Keys
- `.env`의 `TAVILY_API_KEY=tvly-...`
- 없으면 DuckDuckGo HTML 스크래핑으로 대체 가능

## 6️⃣ Cohere (선택, Day 8 rerank)

- 무료 trial — 한국어 reranker 품질 좋음
- https://dashboard.cohere.com → API Keys → Create Trial Key
- `.env`의 `COHERE_API_KEY=...`
- 없으면 로컬 `cross-encoder/ms-marco-MiniLM-L-6-v2`로 충분

## 7️⃣ Langfuse (Day 12, self-host 기본 무료)

- **self-host 권장** — 계정 불필요. `docker-compose up`
- Cloud 쓰고 싶으면:
  - https://cloud.langfuse.com (무료 tier 50k observations/mo)
  - API keys → `LANGFUSE_PUBLIC_KEY=pk-lf-...`, `LANGFUSE_SECRET_KEY=sk-lf-...`
  - `.env`의 `LANGFUSE_HOST=https://cloud.langfuse.com`

## 8️⃣ RunPod (필수, Day 13 $5-10)

1. https://www.runpod.io 가입
2. **Billing → 카드 등록 → $10 충전** (Serverless vLLM 실험 $3-5)
3. **Settings → API Keys → Generate** → `.env`의 `RUNPOD_API_KEY=`
4. Day 13에 Serverless endpoint 만든 후 `RUNPOD_ENDPOINT_ID=` 추가

**비용 감각**
- Serverless L4 24GB: ~$0.0001/sec 활성
- 엔드포인트 idle은 0 (scale-to-zero)
- Cold start 20-60s — warm worker 1개 유지하려면 추가 비용

## 9️⃣ GitHub (Day 14 포트폴리오 공개)

1. github.com 가입 (이미 있으면 skip)
2. 빈 repo 생성 — 이름 예: `devlog-rag-copilot`
3. README/gitignore/license 체크 해제 (Day 14 push 충돌 방지)
4. SSH key 등록 (`ssh-keygen` → `~/.ssh/id_ed25519.pub` → GitHub Settings)
5. 또는 `gh auth login`으로 HTTPS token 로그인

## 🔟 Claude Desktop + Claude Code (Day 11 MCP)

- https://claude.ai/download (macOS/Windows)
- Pro 계정 없어도 MCP 연결 가능 (free tier OK)
- Claude Code: `npm install -g @anthropic-ai/claude-code`
- 설정은 Day 11에

---

## 📊 예산 요약 (14일 전체)

| 항목 | 최저 | 현실 | 비고 |
|---|---|---|---|
| OpenAI | $8 | $15 | Structured + Eval |
| Anthropic | $8 | $15 | Tool + Caching (절감) |
| Gemini | $0 | $0 | 무료 tier |
| Voyage | $0 | $0 | Free credit |
| Tavily | $0 | $0 | Free |
| Cohere | $0 | $0 | Trial |
| Langfuse | $0 | $0 | Self-host |
| RunPod | $5 | $10 | Day 13만 |
| **합계** | **$21** | **$40** | |

실수로 agent loop 잘못 짜면 하루 $수백 가능 → 반드시 **Usage limit 설정**.

## 🛡 보안 규칙

- `.env` 커밋 절대 금지 (`.gitignore` 확인)
- API 키 채팅/이슈/공유 링크 금지
- 유출 즉시:
  1. 공급자 대시보드에서 **revoke**
  2. 새 키 발급
  3. `.env` 교체
  4. GitHub 히스토리에 올랐으면 — 이미 노출. revoke 최우선
- **pre-commit hook** 고려: [`gitleaks`](https://github.com/gitleaks/gitleaks) / [`detect-secrets`](https://github.com/Yelp/detect-secrets)

## ✅ 최종 점검

```bash
source .env  # 또는 direnv 사용
echo $OPENAI_API_KEY | head -c 20       # sk-proj-...
echo $ANTHROPIC_API_KEY | head -c 20    # sk-ant-...
echo $GOOGLE_API_KEY | head -c 20       # AIzaSy...

make verify  # 실제 호출 검증
```

모두 ✔ 이면 Day 1 시작 OK.
