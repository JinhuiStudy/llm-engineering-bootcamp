# Day 11 — MCP (Model Context Protocol)

## 목표
- MCP 프로토콜이 "tool-use의 표준화" 임을 이해
- 자체 MCP 서버 작성 (Python SDK)
- Claude Desktop에 연결해서 실제로 동작 확인
- 기존 Day 5의 tool들을 MCP 서버로 이식

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [modelcontextprotocol.io](https://modelcontextprotocol.io/) | 1.5h |
| 필수 | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | 2h |
| 필수 | [Anthropic MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) | 1h |
| 필수 | [MCP reference servers](https://github.com/modelcontextprotocol/servers) — 읽을 것: filesystem, fetch, github | 1.5h |
| 선택 | [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) | 나중에 |

## 실습 (5h)

### 프로젝트: 자체 MCP 서버
위치: `projects/day10-mcp-server/`

```
day10-mcp-server/
├── server.py                 # MCP 서버 (stdio transport)
├── tools/
│   ├── search_pdfs.py        # Day 7-8의 RAG를 MCP tool로 노출
│   ├── run_eval.py           # Day 9의 eval을 tool로 노출
│   └── list_projects.py      # ai-study 하위 디렉토리 리스트
├── resources/
│   └── notes.py              # notes/ 디렉토리의 파일을 resource로 노출
├── prompts/
│   └── daily_standup.py      # daily-log.md 기반 회고 프롬프트 템플릿
├── claude_desktop_config.json # Claude Desktop 연결 설정
└── README.md
```

### 요구사항
1. **Tools**: 최소 3개 MCP tool 구현
2. **Resources**: MCP resource (LLM이 읽을 수 있는 read-only data)로 notes 노출
3. **Prompts**: MCP prompt template (매크로 같은 재사용 프롬프트) 1개
4. Claude Desktop 의 `claude_desktop_config.json` 에 서버 등록
5. Claude Desktop 에서 실제로 tool 호출 확인

### 설정 예시
```json
{
  "mcpServers": {
    "ai-study": {
      "command": "python",
      "args": ["/Users/parkjinhui/Desktop/dev/ai-study/projects/day10-mcp-server/server.py"]
    }
  }
}
```

### Stretch
- SSE transport로 전환 (HTTP 기반)
- MCP server를 Docker 이미지로 빌드
- OAuth 기반 인증 (문서만 보고 개념 파악)

## 체크리스트

- [ ] MCP의 3가지 primitive (tools / resources / prompts) 구분 가능
- [ ] stdio vs SSE transport 차이 이해
- [ ] Claude Desktop에서 본인 tool 호출 성공 (스크린샷 or 로그)
- [ ] MCP가 OpenAI function calling과 어떻게 다른지 설명 가능 (답: MCP는 client/server 표준. function calling은 단일 provider의 호출 규약)
- [ ] 기존 Day 5 tool agent의 도구를 MCP로 옮기기

## 핵심 키워드
- MCP (Model Context Protocol), JSON-RPC 2.0
- Tools / Resources / Prompts (3 primitives)
- Transport: stdio, SSE, HTTP (streamable)
- Client / Server / Host (Claude Desktop, Cursor 등)
- Sampling (서버가 클라이언트의 LLM을 역호출)
- Roots, capabilities negotiation
