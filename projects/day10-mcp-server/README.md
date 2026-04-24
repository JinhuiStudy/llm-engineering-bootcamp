# Day 11 — MCP Server

커리큘럼: `curriculum/week2-day11-mcp.md`

## 체크리스트
- [ ] MCP 공식 문서 + Python SDK 완주
- [ ] 3개 이상 reference server 코드 읽기 (filesystem, fetch, github)
- [ ] `server.py` — FastMCP 사용
- [ ] Tools 3개 이상 (search_pdfs, run_eval, list_projects)
- [ ] Resources 1개 이상 (notes/ 노출)
- [ ] Prompts 1개 이상 (daily_standup 템플릿)
- [ ] Claude Desktop `claude_desktop_config.json` 설정
- [ ] Claude Desktop에서 실제 호출 성공 (스크린샷 또는 로그)
- [ ] MCP vs OpenAI function calling 차이 1문단

## Claude Desktop config 예시
```json
{
  "mcpServers": {
    "ai-study": {
      "command": "python",
      "args": ["/절대경로/server.py"]
    }
  }
}
```
