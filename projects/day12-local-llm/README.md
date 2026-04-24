# Day 13 — Local LLM (Ollama/vLLM) + RunPod Serverless

> **연결**: [`curriculum/week2-day13-local-llm-runpod.md`](../../curriculum/week2-day13-local-llm-runpod.md)
> **의존성**: Day 8 winner RAG pipeline
> **다음**: Day 14 portfolio의 `LLM_PROVIDER=ollama|runpod` 스위치

## 🎯 이 프로젝트로

1. Ollama 로컬에서 3개 모델 실행 + OpenAI SDK로 호출
2. vLLM PagedAttention 의미를 **실측**으로 이해
3. RunPod Serverless에 Qwen3-8B 배포 → 엔드포인트 획득
4. **4-backend benchmark**: OpenAI API / Anthropic API / Ollama / RunPod — 20 쿼리 × Ragas
5. **Quantization 3단계** (Q4/Q5/Q8) VRAM/품질 트레이드오프
6. "월 $X 이상이면 self-host" 본인 기준선

## 📁 디렉토리

```
day12-local-llm/
├── pyproject.toml
├── local/
│   ├── ollama_chat.py             # OpenAI SDK + base_url=localhost:11434/v1
│   ├── ollama_rag.py              # Day 8 RAG의 generator를 Ollama로
│   ├── vllm_local.py              # (Linux+NVIDIA) vllm serve + OpenAI SDK
│   └── mlx_bench.py               # (Mac) MLX 로컬 추론
├── runpod/
│   ├── deploy_notes.md            # 배포 과정 기록 (막혔던 지점 + 해결)
│   ├── vllm_client.py             # OpenAI SDK + RunPod endpoint
│   └── benchmark.py               # cold start / tok/s / cost
├── benchmark/
│   ├── backends.py                # "openai:gpt-4o-mini" / "anthropic:haiku-4-5" / "ollama:qwen3:8b" / "runpod:qwen3-8b"
│   ├── rag_compare.py             # Day 8 RAG × 4 backend → Ragas
│   └── results/
│       └── matrix.md
├── quantization/
│   ├── pull_gguf.sh               # Q4_K_M / Q5_K_M / Q8_0 다운로드
│   └── quality_vs_vram.py
├── decision_matrix.md             # 본인 의사결정 기준
└── README.md
```

## 🚀 시작

```bash
# Ollama (한 번만)
brew install --cask ollama  # 또는 https://ollama.com/download
ollama pull qwen3:8b        # 한국어 강함, 5GB VRAM
ollama pull llama3.3:8b-instruct-q4_K_M
ollama pull gpt-oss:20b     # (선택) 12GB VRAM

cd projects/day12-local-llm
uv sync
uv add openai anthropic requests ragas
```

## ✅ 필수 기능

### Ollama
- [ ] `ollama_chat.py`:
  ```python
  from openai import OpenAI
  client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
  r = client.chat.completions.create(model="qwen3:8b", messages=[...])
  ```
- [ ] `ollama_rag.py` — Day 8 winner pipeline의 `generate.py` 부분을 Ollama로 교체. embedding은 OpenAI (품질 유지)
- [ ] 동일 쿼리에 대해 GPT-4o-mini vs qwen3:8b Ragas 점수

### RunPod
- [ ] 계정 가입 + $10 충전
- [ ] Serverless > New Endpoint > vLLM template 선택
- [ ] Model: `Qwen/Qwen3-8B-Instruct` (또는 `Qwen/Qwen2.5-32B-Instruct-AWQ`)
- [ ] GPU: 24GB (L4) or 48GB (L40S/A40)
- [ ] ENV: `MAX_MODEL_LEN=8192`, `DTYPE=bfloat16`, `TRUST_REMOTE_CODE=1`
- [ ] 배포 완료 후 Endpoint ID + API key
- [ ] `vllm_client.py`:
  ```python
  client = OpenAI(
    base_url=f"https://api.runpod.ai/v2/{ENDPOINT_ID}/openai/v1",
    api_key=RUNPOD_API_KEY
  )
  ```
- [ ] `benchmark.py` — cold start latency, warm tok/s, $/query

### 4-backend benchmark
- [ ] `backends.py` — 통일 인터페이스:
  ```python
  BACKENDS = {
    "openai:4o-mini": ...,
    "anthropic:haiku-4-5": ...,
    "ollama:qwen3:8b": ...,
    "runpod:qwen3-8b": ...,
  }
  ```
- [ ] `rag_compare.py` — Day 8 RAG × 4 backend × 20 쿼리 → Ragas faithfulness/answer_relevancy
- [ ] `results/matrix.md`:
  ```
  Backend                Faith  AnsRel  $/q      p50(s)  tok/s
  openai:4o-mini         0.87   0.89    0.003    1.8     ~70
  anthropic:haiku-4-5    0.85   0.88    0.005    1.2     ~85
  ollama:qwen3:8b        0.78   0.82    0.000    3.0     ~35
  runpod:qwen3-8b        0.82   0.86    0.0003   4.5     ~80
  ```

### Quantization
- [ ] `quality_vs_vram.py`:
  - 같은 Qwen3-8B의 `qwen3:8b-q4_K_M`, `qwen3:8b-q5_K_M`, `qwen3:8b` (fp16) 또는 HF checkpoints
  - VRAM 사용량 (`nvidia-smi` / Activity Monitor)
  - tok/s
  - 20 쿼리 Ragas 점수
  - 파일 사이즈 (GB)

### Decision Matrix
- [ ] `decision_matrix.md` 본인 숫자로:
  ```
  조건                                     → 선택
  월 <$200, 실험 단계                       → API
  월 >$2000, 안정 트래픽, 단일 모델         → RunPod Serverless
  데이터 이탈 금지                          → 온프렘 vLLM
  지연 < 500ms 필수                         → RunPod Dedicated Pod
  오프라인/에어갭                           → Ollama 로컬
  Fine-tuned 모델 배포                      → RunPod + worker-vllm custom
  ```

## 📊 수치 기준 (본인 장비 따라 다름)

| 메트릭 | Mac M2 16GB | RunPod L4 24GB |
|---|---|---|
| qwen3:8b Q4 tok/s | 20-40 | 60-150 |
| TTFT (warm) | ~500ms | 2-40s (cold start) |
| RAG 품질 vs GPT-4o-mini | 80-90% | 85-95% bf16 |
| $/1K output tokens | $0 | ~$0.0001-0.0005 |

## 🧨 실전 함정

1. **Ollama OpenAI-compat이 완전 호환 아님** — tool_calling, response_format 일부 미지원
2. **Q4_K_M 품질 체감 거의 안 떨어짐** — Q3 이하부터 눈에 띔
3. **RunPod cold start 20-60s** — warm pool 설정 필수 (min_worker=1)
4. **vLLM on Mac** — MPS 지원 제한. `llama.cpp` / `Ollama` / `MLX` 권장
5. **Base URL 트릭**이 OpenAI SDK만 동작 — Anthropic/Gemini SDK는 base_url 교체 안 됨
6. **License 이슈** — Llama 상용 제한, Qwen/Gemma는 Apache/커스텀. 배포 전 검토
7. **Chat template 미스매치** — 같은 모델인데 Ollama와 vLLM 템플릿 다르면 tool parsing 실패
8. **자동 context window 초과** — 8k 기본인데 RAG context 8k+ 넣으면 잘림. `MAX_MODEL_LEN=16384` 조정

## 🎁 Stretch

- 🧪 **llama.cpp 직접 빌드** — Metal/CUDA 백엔드 컴파일 + MLX 성능 비교
- 🧪 **Speculative Decoding** — small draft + big target, vLLM 지원
- 🧪 **Tensor parallel 2 GPUs** — RunPod A40 2개로 70B Q4 서빙
- 🧪 **AWQ vs GPTQ vs GGUF** — 같은 모델의 다른 양자화 포맷 품질/속도
- 🧪 **Outlines + Ollama** — 로컬에 grammar-constrained decoding으로 JSON 100% 보장
- 🧪 **TGI** — vLLM vs TGI throughput 벤치

## 🔗 다음에 쓰이는 곳

- Day 14: `app/llm/providers/ollama.py`, `providers/runpod.py` 이식
- `LLM_PROVIDER=ollama` env로 런타임 스위치
