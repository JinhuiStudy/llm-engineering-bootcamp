# Day 11 — MCP + Batch API + Guardrails 풀스택 (ULTRA)

> **난이도**: ★★★★★ (v3 상향)
> **총량**: MCP 7h + Batch API 2h + Guardrails 풀스택 2h + 정리 1h = **12h**.
> **중요도**: MCP는 2024-말 Anthropic 표준. Guardrails는 프로덕션 진입점. Batch는 50% 비용 절감.

## 🎯 오늘 끝나면

1. MCP의 **4대 primitive** (Tools / Resources / Prompts / Sampling) 구분 + 각 용도
2. Python SDK(`mcp`/FastMCP)로 서버 직접 구현 — stdio + Streamable HTTP 둘 다
3. Claude Desktop + Claude Code + Cursor 3종 호스트에 서버 등록, 실제 호출 증명
4. Day 8 RAG + Day 5 Tool + Day 10 Agent를 **MCP tool / resource**로 노출
5. **Sampling** — 서버가 호스트의 LLM을 역호출하는 패턴 구현
6. **보안** — tool allowlist, roots, capability negotiation, consent prompts

## 📚 자료

### 🔥 필수

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 1h | [modelcontextprotocol.io](https://modelcontextprotocol.io/) | 공식 홈. "Introduction / Core concepts / Tools / Resources / Prompts / Sampling" 섹션 순차. |
| 1h | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | `FastMCP` 고수준 API. `@mcp.tool()`, `@mcp.resource("...")`, `@mcp.prompt()`. README만 읽고 `examples/` 가기. |
| 45m | [Anthropic — MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) | Claude Desktop/API에서 MCP 쓰는 법. |
| 30m | [MCP Specification](https://spec.modelcontextprotocol.io/) | JSON-RPC 2.0 기반 프로토콜 스펙. 메시지 타입 (request/response/notification) 구조. |
| 45m | [MCP Reference Servers](https://github.com/modelcontextprotocol/servers) | filesystem / fetch / github / memory / postgres 등 20+ 구현체. 오늘 참고: `filesystem`, `fetch`, `memory`. |
| 30m | [FastMCP docs](https://gofastmcp.com/getting-started/welcome) | `FastMCP` 서버 프레임워크 (Jeremy Howard 팀). 보일러 플레이트 최소. |

### ⭐ 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 20m | [Claude Desktop config schema](https://modelcontextprotocol.io/quickstart/user) | `claude_desktop_config.json` 경로 (mac: `~/Library/Application Support/Claude/`). env var, args 주입 방법. |
| 20m | [MCP — Security best practices](https://modelcontextprotocol.io/specification/basic/security) | Consent prompts, roots, tool categorization (trusted / untrusted). |
| 30m | [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) | 필수 아니지만 읽어두면 크로스 생태계 감각. Claude Code가 TS MCP도 잘 씀. |
| 30m | [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | MCP 서버 디버그용 웹 UI. `npx @modelcontextprotocol/inspector python server.py`. **개발 필수 도구**. |

### 🎓 선택

- [Block / Cline / Windsurf / Zed — MCP client 목록](https://modelcontextprotocol.io/clients) — 지원 호스트 스냅샷.
- [Anthropic — Introducing MCP (announcement)](https://www.anthropic.com/news/model-context-protocol) — 왜 만들었는가. 2024-11.
- [MCP Auth](https://modelcontextprotocol.io/specification/basic/authorization) — OAuth 2.1 flow. Enterprise 쓸 때.

## 🔬 실습 (5.5h)

### 프로젝트: `ai-study-mcp` — 다기능 MCP 서버

위치: `projects/day10-mcp-server/`

```
day10-mcp-server/
├── server.py                     # FastMCP 엔트리 (stdio 기본)
├── server_http.py                # Streamable HTTP transport 버전
├── tools/
│   ├── search_pdfs.py            # Day 7-8 RAG을 MCP tool로
│   ├── run_assessment.py         # Day 9 Ragas mini
│   ├── list_projects.py          # 본 레포 디렉토리 탐색
│   └── math_safe.py              # safe expression parser (asteval)
├── resources/
│   ├── notes.py                  # notes/*.md 파일 read-only
│   ├── daily_log.py              # daily-log 최근 N일
│   └── curriculum.py             # curriculum/*.md
├── prompts/
│   ├── daily_standup.py          # "오늘 log + 내일 할 일"
│   ├── rag_answer.py             # RAG 프롬프트 템플릿
│   └── code_review.py            # 오늘 diff 리뷰
├── sampling/
│   └── summarize_via_host.py     # 서버가 클라이언트 LLM 역호출
├── auth/
│   └── roots.py                  # root 경로 allowlist
├── test_inspector.sh             # MCP Inspector 띄우기
├── claude_desktop_config.json    # 등록 스니펫
├── claude_code_config.jsonc      # Claude Code 등록
├── cursor_config.json            # Cursor 등록
└── README.md
```

### 🔥 필수 기능

1. **FastMCP 서버** — `mcp = FastMCP("ai-study-mcp")` + `@mcp.tool()` / `@mcp.resource()` / `@mcp.prompt()`
2. **Tools 최소 4개**:
   - `search_pdfs(query: str, top_k: int = 5) -> list[Hit]` — Day 8 최고 pipeline 호출
   - `run_assessment(pipeline: str, sample: int = 20) -> Report` — Day 9 Ragas mini
   - `list_project_files(subdir: str = ".") -> list[str]` — 샌드박스 내 탐색
   - `calc_safe(expression: str) -> float` — asteval 기반
3. **Resources 최소 3개** — read-only:
   - `notes://keywords` → `notes/keywords.md`
   - `notes://daily-log` → 최근 7일 로그
   - `curriculum://day/{n}` → 해당 day 파일 반환
4. **Prompts 최소 2개**:
   - `daily_standup(days: int = 1)` — 회고 템플릿
   - `rag_answer(context: str, question: str)` — 오늘 배운 RAG 프롬프트 재사용
5. **Sampling 1개** — `summarize_file(path)` 서버 내부에서 호스트 LLM에 "이 파일 3줄 요약" 요청 → 호스트가 모델 선택 + 응답. Capability negotiation으로 sampling 지원 확인 선행.
6. **Transport 2종**:
   - stdio (Claude Desktop 기본)
   - Streamable HTTP (원격 서버 / 멀티 클라이언트). `/mcp` 엔드포인트.
7. **Roots 제한** — `SANDBOX_ROOT` 외부 접근 금지
8. **MCP Inspector**로 로컬 테스트 → 3개 호스트(Claude Desktop / Claude Code / Cursor)에 각각 등록 후 실제 호출

### 🧪 테스트 시나리오

1. Claude Desktop에서 "오늘 daily_standup 프롬프트 써서 회고" → 서버 prompt 호출 + resource 읽기
2. Cursor에서 "search_pdfs로 qdrant 관련 부분 찾기" → tool 호출 → RAG 결과
3. Claude Code에서 "curriculum://day/8 리소스 읽고 요약" → resource + sampling 연계
4. Inspector로 JSON-RPC 메시지 직접 확인: `tools/list`, `tools/call`, `resources/read`, `prompts/get`

### 🔥 Stretch

- 🧪 **OAuth flow** — MCP server에 간단 auth (Bearer token)
- 🧪 **Docker image** — `Dockerfile` + docker-compose로 HTTP 서버 배포
- 🧪 **GitHub MCP 리모트 예시** — 자기 레포 CI log 읽는 tool
- 🧪 **Multi-server aggregation** — Day 14 portfolio에서 ai-study-mcp + 공식 filesystem MCP 두 서버 동시 사용
- 🧪 **TypeScript로도 구현** — 작은 tool 하나만 TS로, Python과 크로스체크
- 🧪 **Streaming tool** — tool 응답을 chunk 단위로 (진행률 UI)

## 🔐 보안 체크리스트

- [ ] `file_io` tool은 SANDBOX_ROOT 바깥 접근 차단 (realpath 검사)
- [ ] tool description에 실제 경로 / API key 노출 금지
- [ ] `run_shell` 같은 위험 tool 안 만듦 (만들면 docker/firejail 격리 + allowlist)
- [ ] 호스트 consent prompt가 뜨는지 확인 (파일 쓰기 등)
- [ ] Sampling 사용 시 요청 LLM 목록을 제한 (모델 whitelist)

## ✅ 체크리스트

- [ ] FastMCP로 `tools/resources/prompts/sampling` 4개 primitive 전부 구현
- [ ] stdio + Streamable HTTP 2가지 transport 동작
- [ ] Claude Desktop `claude_desktop_config.json` 에 서버 등록 + 재시작 후 호출 성공
- [ ] Claude Code CLI (`claude mcp add`) 등록 성공
- [ ] Cursor settings에 서버 등록 성공 (적어도 1개 호스트면 OK)
- [ ] MCP Inspector로 4개 primitive 모두 호출 확인 (스크린샷 or 로그)
- [ ] Day 5 tool과 MCP tool을 비교해 **MCP로 바꾸는 이득** 1문단 정리
- [ ] `notes/concepts.md` — "MCP vs function calling의 정확한 차이" 1 문단

## 🧨 자주 틀리는 개념

1. **"MCP == function calling"** — 아니다. function calling은 **하나의 provider 내부 호출 규약**. MCP는 **클라이언트/서버 표준** — 다른 LLM, 다른 호스트가 같은 서버 재사용 가능.
2. **"stdio 간단해서 stdio만 쓰면 됨"** — 로컬만 가능. 원격 / 다중 클라이언트는 HTTP Streamable 필수.
3. **"Resources는 tool의 GET 버전"** — 비슷하지만 **호스트가 미리 목록을 알고 attach**할 수 있다는 게 tool과 다름. "사용자가 컨텍스트에 붙여 넣는 자료"에 더 가까움.
4. **"Prompts는 그냥 system prompt"** — **호스트 UI에서 명령어처럼** 보여져 사용자가 명시 호출. Quick-slash 같은 느낌.
5. **"Sampling은 덜 중요"** — 서버가 클라 LLM을 쓸 수 있게 해주는 강력 기능. 예: 서버가 "문서 요약을 호스트 Claude로" → 사용자 quota 사용. 권한 남용 주의.
6. **"JSON-RPC 몰라도 됨"** — 고수준 SDK로 가능. 디버깅할 때는 JSON-RPC 메시지 직접 보게 됨 → Inspector 필수.
7. **"Claude Desktop 재시작 없이 반영"** — config 변경은 재시작 필수. 서버 코드 바뀌면 host가 재연결 자동. (호스트마다 다름)

## 🧪 산출물

- `projects/day10-mcp-server/` — 완성
- 3개 호스트 config 파일 (`claude_desktop_config.json`, `claude_code_config.jsonc`, `cursor_config.json`)
- Inspector 스크린샷 1장 (notes에 첨부)
- `notes/concepts.md` — MCP 4 primitive 비교 표
- `cheatsheets/` — 신규 `mcp-cheatsheet.md` (선택)

## 📌 핵심 키워드

- MCP = Model Context Protocol (2024-11, Anthropic open-source)
- JSON-RPC 2.0 — request / response / notification / error
- 4 primitives: **Tools** (execute) / **Resources** (read) / **Prompts** (templates) / **Sampling** (server → client LLM)
- Transports: **stdio** (local only) / **Streamable HTTP** (remote, 2025 spec) / **SSE** (legacy)
- Host (Claude Desktop/Code/Cursor/Zed) / Client (SDK) / Server (이 프로젝트)
- Capabilities negotiation — `initialize` handshake로 지원 기능 교환
- Roots — 서버가 접근 가능한 경로 (샌드박스)
- Consent prompts — 민감 operation 실행 전 사용자 승인
- FastMCP — Python 고수준 프레임워크

## ⚠️ 프로덕션 주의

- **MCP 서버가 받는 input을 무조건 검증** — prompt injection 벡터.
- **Secret을 tool description / resource에 넣지 말 것**.
- **Resource URI scheme 통일** (예: `notes://`, `db://`) — 호스트 UI에서 정렬/필터에 유리.
- **Sampling 남용 금지** — 사용자 quota 소비. 옵트인으로.
- **OAuth 는 MCP 2025 spec이 표준화**. Enterprise에서는 매우 중요.

## 📦 v3 추가 — Batch API 실측 (2h)

50% 비용 절감. 대량 eval/classification/extraction에 필수.

### 🔗 자료
- [OpenAI Batch](https://platform.openai.com/docs/guides/batch) — `.jsonl` 업로드 → 24h SLA → 결과 download
- [Anthropic Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing)
- [Gemini Batch](https://ai.google.dev/gemini-api/docs/batch-mode)

### 🔥 실습
Day 9 golden dataset 80건을 **3사 Batch API**로 돌리기:

```python
# OpenAI Batch
import json
from openai import OpenAI

client = OpenAI()
with open("batch_input.jsonl", "w") as f:
    for i, q in enumerate(questions):
        f.write(json.dumps({
            "custom_id": f"q-{i}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": q}]
            }
        }) + "\n")

batch_file = client.files.create(file=open("batch_input.jsonl", "rb"), purpose="batch")
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)
# 24h 기다리고 결과 download
```

### 📊 비용 비교표
| Provider | 즉시 호출 (80건) | Batch (24h) | 절감 |
|---|---|---|---|
| OpenAI (4o-mini) | $0.80 | $0.40 | 50% |
| Anthropic (haiku-4-5) | $0.90 | $0.45 | 50% |
| Gemini (flash) | $0.30 | $0.15 | 50% |

→ `results/batch_cost.md` 본인 숫자 표

### 💡 사용 원칙
- 실시간 UX X (24h 대기) → 오프라인 eval / 배치 분석에만
- Day 9 Ragas eval을 batch로 돌리면 매 PR nightly CI 저렴하게

## 🛡 v3 추가 — Guardrails 풀스택 3겹 (2h)

Day 3의 Prompt-Guard + Day 5의 safety rails를 **프로덕션 수준**으로 통합.

### 🔗 자료
- [Guardrails AI](https://www.guardrailsai.com/docs) — validators 라이브러리 + RAIL spec
- [NeMo Guardrails (NVIDIA)](https://github.com/NVIDIA/NeMo-Guardrails) — Colang 기반 dialogue flow
- [LlamaFirewall (Meta)](https://github.com/facebookresearch/llamafirewall) — 통합 방어 프레임
- [Anthropic — Strengthen Guardrails](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/overview)

### 🔥 3겹 구조

```
사용자 입력
    ↓
[겹 1] Prompt-Guard 2 (Day 3 재사용) — INJECTION/JAILBREAK 탐지 → reject
    ↓
[겹 2] Guardrails AI — input validators (PII / profanity / topic)
    ↓
LLM 호출
    ↓
[겹 3] Output validators — PII mask / 출력 schema / factuality check / 유해 content
    ↓
사용자에게
```

### 🔥 실습 구조

```
day10-mcp-server/
├── guardrails/
│   ├── input_prompt_guard.py    # Day 3 Prompt-Guard 2 wrap
│   ├── guardrails_ai_spec.py    # Guardrails AI validators
│   ├── nemo_colang/             # NeMo Colang 규칙 1-2개
│   └── output_filters.py        # PII mask + factuality
└── eval/
    └── attack_set.json           # 공격 50건 × 3겹 통과율
```

### 🔥 요구 기능
1. Guardrails AI로 input validator:
   ```python
   from guardrails import Guard
   from guardrails.hub import ToxicLanguage, DetectPII

   guard = Guard().use_many(ToxicLanguage(), DetectPII())
   result = guard.validate(user_input)
   if not result.validation_passed:
       raise ValueError("input rejected")
   ```
2. NeMo Colang 규칙 1개 (예: "회사 내부 문서 외 질문 거절")
3. Output PII mask (regex + LLM classifier)
4. Factuality check (Ragas faithfulness 실시간)

### 📊 수치 기준
| 메트릭 | 목표 |
|---|---|
| 공격 50건 → 3겹 통과율 | ≤ 5% (95%+ 차단) |
| Benign 50건 → false reject | ≤ 3% |
| 추가 latency | ≤ 500ms |
| Prompt-Guard만 vs 3겹 | 차단율 +10-15% |

## 🎁 내일(Day 12) 미리보기
Observability + Production + **Deployment (Modal/Fly.io/Docker/K8s basics)**. 오늘 MCP 서버를 Modal에 배포해서 public URL 만들기.
