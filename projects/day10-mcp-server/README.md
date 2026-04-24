# Day 11 — MCP Server (Tools/Resources/Prompts/Sampling)

> **연결**: [`curriculum/week2-day11-mcp.md`](../../curriculum/week2-day11-mcp.md) · [`cheatsheets/mcp-cheatsheet.md`](../../cheatsheets/mcp-cheatsheet.md)
> **의존성**: Day 8 RAG + Day 5 Tools + Day 9 Eval
> **다음**: Day 14 portfolio에 MCP 서버 포함 → Claude Desktop에서 직접 호출

## 🎯 이 프로젝트로

1. FastMCP로 **4대 primitive** 서버 구현 — Tools / Resources / Prompts / Sampling
2. stdio + Streamable HTTP 2가지 transport
3. Claude Desktop / Claude Code / Cursor 3종 호스트에 등록 + 실제 호출 증명
4. Day 5 tools / Day 8 RAG / Day 9 eval을 MCP로 노출
5. **샌드박스 roots** + **OAuth 2.1** (Stretch)

## 📁 디렉토리

```
day10-mcp-server/
├── pyproject.toml
├── server.py                          # FastMCP stdio 엔트리
├── server_http.py                     # Streamable HTTP `/mcp`
├── tools/
│   ├── __init__.py
│   ├── search_pdfs.py                 # Day 8 RAG을 MCP tool로
│   ├── run_assessment.py              # Day 9 Ragas mini
│   ├── list_project_files.py          # sandbox 탐색
│   └── calc_safe.py                   # asteval expression parser
├── resources/
│   ├── notes.py                       # notes://keywords, notes://daily-log
│   ├── curriculum.py                  # curriculum://day/{n}
│   └── config.py                      # config://model-prices
├── prompts/
│   ├── daily_standup.py
│   ├── rag_answer.py
│   └── code_review.py                 # git diff 기반
├── sampling/
│   └── summarize_via_host.py          # 서버 → 호스트 LLM 역호출
├── auth/
│   ├── roots.py                       # SANDBOX_ROOT check
│   └── oauth.py                       # Stretch: Bearer/OAuth 2.1
├── configs/
│   ├── claude_desktop_config.json     # 등록 스니펫
│   ├── claude_code_config.jsonc
│   └── cursor_mcp.json
├── test_inspector.sh                  # npx inspector 띄우기
└── README.md
```

## 🚀 시작

```bash
cd projects/day10-mcp-server
uv sync
uv add mcp asteval
# 또는 FastMCP wrapper
uv add fastmcp

# MCP Inspector (디버깅 필수)
npx @modelcontextprotocol/inspector uv run python server.py
```

## ✅ 필수 기능

### Tools (최소 4개)
- [ ] `search_pdfs(query: str, top_k: int = 5, pipeline: str = "full_stack") -> list[Hit]`
  - Day 8 pipeline 호출 → chunks + scores 반환
- [ ] `run_assessment(pipeline: str, sample: int = 20) -> Report`
  - Day 9 Ragas mini → {faithfulness, answer_relevancy, ...}
- [ ] `list_project_files(subdir: str = ".") -> list[str]`
  - SANDBOX_ROOT 아래만 realpath 검사
- [ ] `calc_safe(expression: str) -> float`
  - asteval 기반

### Resources (최소 3개)
- [ ] `notes://{name}` → `notes/{name}.md` 내용
- [ ] `daily-log://recent/{days}` → 최근 N일 log
- [ ] `curriculum://day/{n}` → 해당 day 커리큘럼

### Prompts (최소 2개)
- [ ] `daily_standup(days: int = 1)` — "어제 한 것 / 오늘 할 것" 템플릿
- [ ] `rag_answer(context: str, question: str)` — 표준 RAG 프롬프트
- [ ] `code_review(git_ref: str = "HEAD~1")` — git diff 기반 리뷰 (Stretch)

### Sampling (최소 1개)
- [ ] `summarize_via_host(path: str) -> str`:
  ```python
  @mcp.tool()
  async def summarize_file(ctx: Context, path: str) -> str:
      text = Path(path).read_text()
      # 호스트 LLM 역호출
      result = await ctx.sample(
          messages=[{"role":"user","content":f"3줄 요약:\n{text}"}],
          model_preferences={"intelligence_priority": 0.6},
          max_tokens=300,
      )
      return result.content
  ```

### Transport
- [ ] `server.py` — `mcp.run()` (stdio default)
- [ ] `server_http.py`:
  ```python
  from mcp.server.fastmcp import FastMCP
  mcp = FastMCP("ai-study")
  # ... tools/resources ...
  app = mcp.streamable_http_app()  # Starlette app
  # uvicorn으로 띄움
  ```

### Host 등록 + 호출 증명
- [ ] **Claude Desktop**:
  ```json
  {
    "mcpServers": {
      "ai-study": {
        "command": "uv",
        "args": ["run","python","/absolute/path/server.py"],
        "env": {"OPENAI_API_KEY": "...", "ANTHROPIC_API_KEY": "..."}
      }
    }
  }
  ```
  Claude Desktop 재시작 → 설정에서 connected 확인 → 대화에서 tool 호출
- [ ] **Claude Code**:
  ```bash
  claude mcp add ai-study -- uv run python /absolute/path/server.py
  claude mcp list
  ```
- [ ] **Cursor**: `.cursor/mcp.json` 에 추가 또는 설정 UI

### Inspector 검증
- [ ] `npx @modelcontextprotocol/inspector ...`
- [ ] `tools/list`, `tools/call`, `resources/read`, `prompts/get` 모두 호출 확인

## 📊 수치 기준

| 메트릭 | 기준 |
|---|---|
| 4 primitive 모두 Inspector에서 성공 | 100% |
| 3 호스트 중 Claude Desktop 등록 + 호출 | 필수 |
| stdio + HTTP transport 모두 동작 | 필수 |
| SANDBOX_ROOT 바깥 접근 차단율 | 100% |
| Sampling 호출 성공 (지원 호스트) | 1회 이상 |

## 🧨 실전 함정

1. **stdio 서버가 `print()` 쓰면 JSON-RPC 깨짐** — logger → stderr만
2. **`@mcp.tool()` docstring = description** — 공란이면 정확도 뚝
3. **Pydantic 모델 인자 자동 JSON Schema** — plain dict는 schema 부실
4. **Sampling은 host capability 있을 때만** — Claude Desktop은 지원 여부 확인 필요
5. **Claude Desktop config 변경 후 재시작 필수**
6. **절대경로 써야** — `~/path` 는 expand 안 됨
7. **Resource URI에 `/` 포함하면 parsing 이슈** — `{}` placeholder 단일 토큰 권장
8. **Streamable HTTP는 2025 spec** — 구 SSE 쓰면 호환성 이슈. FastMCP 최신 버전 사용

## 🎁 Stretch

- 🧪 **OAuth 2.1** — Bearer token + `/auth/*` 엔드포인트
- 🧪 **Docker image** — Dockerfile + compose로 원격 HTTP
- 🧪 **GitHub MCP** — 자기 repo CI 상태 조회 tool
- 🧪 **Multi-server aggregation** — Day 14에서 이 서버 + 공식 filesystem MCP 동시 사용
- 🧪 **TypeScript 버전** — 작은 tool 하나만 TS로 — cross check
- 🧪 **Streaming tool** — tool 응답을 chunk 단위

## 🔗 다음에 쓰이는 곳

- Day 14 portfolio: `app/mcp/server.py` 로 이식
- 자기 Claude Desktop 상시 MCP로 부트캠프 자료 질의
