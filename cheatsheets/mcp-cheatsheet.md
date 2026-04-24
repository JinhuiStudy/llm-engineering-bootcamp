# MCP (Model Context Protocol) 치트시트

## 한눈에

- **MCP = LLM용 USB-C** — 2024-11 Anthropic 오픈 표준
- **JSON-RPC 2.0** 기반 클라이언트/서버 프로토콜
- 4 primitives: **Tools / Resources / Prompts / Sampling**
- 3 transports: **stdio / Streamable HTTP / SSE(legacy)**
- Host 예: Claude Desktop, Claude Code, Cursor, Windsurf, Zed

## 역할

- **Host**: 유저가 쓰는 앱 (Claude Desktop)
- **Client**: Host 내부 SDK가 생성한 MCP 클라이언트
- **Server**: 이 프로젝트. tool/resource/prompt 노출

## 4 Primitives

### Tools (execute)
```python
@mcp.tool()
def get_weather(city: str) -> dict:
    """Return current weather for a city."""
    return {"temp": 22, "condition": "sunny"}
```
- 함수 호출
- JSON Schema 자동 생성 (Pydantic)
- 호스트가 LLM에 tool_use로 제시

### Resources (read)
```python
@mcp.resource("notes://{name}")
def get_note(name: str) -> str:
    return Path(f"notes/{name}.md").read_text()
```
- 정적/동적 콘텐츠
- URI scheme으로 정리 (`notes://`, `db://table/row/id`)
- 호스트가 목록을 미리 알고 UI에서 attach 가능

### Prompts (templates)
```python
@mcp.prompt()
def code_review(diff: str) -> list[dict]:
    return [
        {"role": "user", "content": f"Review this diff:\n{diff}"}
    ]
```
- 재사용 가능한 프롬프트 (호스트 UI에 `/command` 형태)
- 파라미터 받아서 메시지 리스트 반환

### Sampling (server → client LLM)
```python
async def summarize(ctx: Context, text: str):
    result = await ctx.sample(
        messages=[...],
        model_preferences={"intelligence_priority": 0.7}
    )
    return result.content
```
- 서버가 호스트의 LLM을 역호출
- 호스트가 모델 선택 / 승인 / quota 관리
- 강력 but 권한 남용 주의

## FastMCP 최소 서버

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.resource("config://{name}")
def config(name: str) -> str:
    return f"config for {name}"

if __name__ == "__main__":
    mcp.run()  # stdio 기본
```

## Transport 선택

| Transport | 사용 |
|---|---|
| stdio | 로컬 전용. Claude Desktop이 subprocess로 실행. 가장 쉬움. |
| Streamable HTTP | 원격/멀티클라이언트. `/mcp` 엔드포인트. 2025 spec 권장. |
| SSE | Streamable HTTP 이전 표준. 새 코드는 Streamable HTTP. |

## Claude Desktop 등록

`~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "ai-study": {
      "command": "uv",
      "args": ["run", "python", "/path/to/server.py"],
      "env": {"OPENAI_API_KEY": "..."}
    }
  }
}
```
Claude Desktop **재시작** 필수.

## Claude Code 등록

```bash
claude mcp add ai-study -- uv run python /path/to/server.py
```

## Cursor 등록

`.cursor/mcp.json` 또는 설정 UI:
```json
{
  "ai-study": {
    "command": "uv",
    "args": ["run", "python", "/path/to/server.py"]
  }
}
```

## Inspector (디버깅 필수)

```bash
npx @modelcontextprotocol/inspector python server.py
```
- 웹 UI로 서버 호출 테스트
- JSON-RPC 메시지 raw로 확인
- tools/list, resources/list, prompts/list 자동

## 보안

### Roots — 샌드박스
```python
def is_path_allowed(path):
    real = os.path.realpath(path)
    return real.startswith(os.path.realpath(SANDBOX_ROOT))
```

### Tool description
- API key / 내부 URL / 파일 경로 비밀 금지
- 공개 가능한 설명만

### Consent
- 민감 operation 실행 전 호스트가 사용자에게 확인
- FastMCP / SDK가 기본 처리

### OAuth (MCP 2025 spec)
- Enterprise / multi-tenant 용
- Bearer token, OAuth 2.1 flow
- `/auth/*` 엔드포인트

## 함정

- stdio 서버가 **stdout에 print 금지** — JSON-RPC 깨짐. logger로 stderr만.
- `@mcp.tool()` docstring이 **description**으로 들어감. 비어있으면 정확도 ↓
- Pydantic 모델 받으면 자동 JSON Schema 생성. 일반 dict 받으면 schema 부실.
- Sampling은 호스트 capability 있을 때만. 없는 호스트도 많음 → graceful fallback.
- Resource URI는 **호스트 UI에서 정렬/필터**에 씀 → scheme 일관되게.

## 레퍼런스 서버 (재활용)

- `@modelcontextprotocol/server-filesystem` — 파일 R/W
- `@modelcontextprotocol/server-fetch` — HTTP GET
- `@modelcontextprotocol/server-memory` — 대화 메모리
- `@modelcontextprotocol/server-github` — GH API
- `@modelcontextprotocol/server-postgres` — 읽기 전용 DB

## 참고

- [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP](https://gofastmcp.com/)
- [Specification](https://spec.modelcontextprotocol.io/)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [Reference servers](https://github.com/modelcontextprotocol/servers)
