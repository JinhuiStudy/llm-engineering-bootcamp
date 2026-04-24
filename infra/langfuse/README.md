# Langfuse self-hosted (Day 12)

Observability + Prompt Management + Eval. 모든 건 로컬.

## 최초 기동 (2-3분 걸림)
```bash
make langfuse-up
# 또는
docker compose -f infra/langfuse/docker-compose.yml up -d
```

컨테이너 5개 뜸: web / worker / postgres / clickhouse / redis / minio.

## 첫 접속
1. http://localhost:3000 열기
2. "Sign up" → 아무 이메일/비번 (**로컬만 사용, 실제 가입 아님**)
3. "New organization" → 이름 아무거나
4. "New project" → 이름 아무거나
5. **Settings → API Keys → Create** → public/secret 키 복사
6. `.env`에 붙여넣기:
   ```
   LANGFUSE_HOST=http://localhost:3000
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   ```

## 점검
- Dashboard 상단 "Tracing" 클릭 → 빈 상태면 OK
- SDK로 한 건 쏴보고 Traces 탭에 뜨는지 확인

## 포트
- **3000**: web UI
- **9090**: minio S3 (데이터 업로드용, 직접 건드릴 일 없음)
- **9091**: minio console

## 중지 / 초기화
```bash
make langfuse-down                        # 중지만
rm -rf infra/langfuse/volumes            # 완전 초기화
```

## 리소스
- RAM 2-3GB 씀 (clickhouse가 제일 배고픔)
- 디스크 수백MB ~ 수GB (trace 양에 따라)
- Mac 발열 좀 있음 — Day 12에만 켜고 Day 13-14는 필요시만

## 문제 해결
- `postgres` 가 unhealthy: volumes/postgres 삭제 후 재기동
- web이 안 뜸: `docker logs ai-study-langfuse-web` 로 에러 확인
- SALT/ENCRYPTION_KEY 경고: production 아니니 무시. 공개 배포 시에는 반드시 교체.
