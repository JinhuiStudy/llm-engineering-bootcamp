# Day 13 — Local LLM (Ollama + vLLM) + RunPod Serverless

> **난이도**: ★★★ (원래 ★★에서 상향)
> **총량**: 읽기 4h + 실습 5h + 정리 1h = 10h.
> **이정표**: "API만 쓰는 LLM 개발자"에서 "GPU 알고 모델도 고르는 LLM 엔지니어"로.

## 🎯 오늘 끝나면

1. Ollama 로컬에서 GGUF 모델 실행 + OpenAI SDK (base_url 트릭)로 호출
2. vLLM의 **PagedAttention + Continuous Batching**이 왜 throughput 10배인지 설명
3. GGUF 양자화(Q4_K_M / Q5_K_M / Q8_0)의 VRAM/품질 트레이드오프를 **본인 machine으로 실측**
4. RunPod Serverless에 vLLM 배포 → 클라우드 GPU 엔드포인트 획득
5. 동일 RAG 쿼리를 **API vs Ollama vs RunPod** 3사 비교 (품질/latency/비용 표)
6. "월 $X 이상이면 self-host" 의사결정 기준을 본인 숫자로 정의

## 📚 자료

### 🔥 필수 — Local LLM

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [Ollama 공식](https://ollama.com/) + [docs](https://docs.ollama.com/) | `ollama run qwen3:8b`. macOS/Linux/Windows. OpenAI-compatible `http://localhost:11434/v1`. |
| 20m | [Ollama — OpenAI compatibility](https://docs.ollama.com/openai) | SDK 그대로 base_url 바꿔 사용. Dummy `api_key="ollama"`. |
| 30m | [Ollama — Model Library](https://ollama.com/library) | `qwen3`, `llama3.3`, `gpt-oss`, `gemma3`, `deepseek-r1`. 모델 카드에 VRAM 요구량 표기. |
| 1h | [vLLM docs — Getting started](https://docs.vllm.ai/) | `pip install vllm`. 5분이면 OpenAI-compatible server. Linux+NVIDIA 권장 (Mac MPS 부분지원). |
| 30m | [vLLM — OpenAI Compatible server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html) | `vllm serve Qwen/Qwen3-8B --port 8000`. chat_template, tool_calling 지원. |
| 30m | [PagedAttention paper (Kwon 2023)](https://arxiv.org/abs/2309.06180) | vLLM의 핵심. KV cache를 OS의 paging 기법으로 관리해 GPU 메모리 단편화 해결. **Figure 1-2만**. |
| 30m | [llama.cpp README](https://github.com/ggml-org/llama.cpp) | GGUF 포맷의 본가. CPU 추론/Apple Silicon 강함. `llama-server` OpenAI-compat. |
| 20m | [HF TGI](https://huggingface.co/docs/text-generation-inference/index) | vLLM 경쟁. 엔터프라이즈 친화. |

### 🔥 필수 — RunPod

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [RunPod 공식](https://www.runpod.io/) + [docs](https://docs.runpod.io/) | GPU cloud. **Pods (persistent VM)** vs **Serverless (event-driven, scale-to-zero)**. |
| 30m | [RunPod Serverless Overview](https://docs.runpod.io/serverless/overview) | 요청당 과금. Cold start 20-60s (GPU). 대부분 쓰지 않을 때 요금 0. |
| 30m | [RunPod Serverless vLLM — Getting started](https://docs.runpod.io/serverless/vllm/get-started) | Template "worker-vllm" 선택 → HF model ID 입력 → endpoint 생성. OpenAI-compat URL 제공. |
| 20m | [RunPod Serverless vLLM — Configuration](https://docs.runpod.io/serverless/vllm/configuration) | Env vars: `MODEL_NAME`, `MAX_MODEL_LEN`, `DTYPE`, `TENSOR_PARALLEL_SIZE`, `QUANTIZATION`. |
| 30m | [vLLM on RunPod deployment guide](https://docs.vllm.ai/en/latest/deployment/frameworks/runpod/) | vLLM 쪽 문서. |
| 20m | [runpod-workers/worker-vllm](https://github.com/runpod-workers/worker-vllm) | Template 소스. 커스텀 환경 구성 참고. |

### 🔥 모델 선택

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 20m | [HF Models](https://huggingface.co/models) | 필터: text-generation + size + license. Qwen3 / Llama 3.3 / gpt-oss / Mixtral / DeepSeek-R1 주력. |
| 20m | [Open LLM Leaderboard v2](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) | Bench 점수. IFEval / BBH / GPQA / MATH. |
| 20m | [Chatbot Arena Leaderboard](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard) | 인간 선호 Elo. 실제 품질 체감에 가까움. |
| 20m | [LMArena](https://lmarena.ai/) | 라이브 pairwise 투표. 실험용 모델 품질 가늠. |
| 20m | [GGUF quantization 비교 (TheBloke / bartowski)](https://huggingface.co/bartowski) | 모델마다 Q4/Q5/Q6/Q8 파일 제공. VRAM 요구량 README 정독. |

### ⭐ 강력 권장

- [llama-cpp-python — server](https://llama-cpp-python.readthedocs.io/en/latest/server/) — llama.cpp OpenAI-compat Python 서버.
- [Unsloth — inference](https://docs.unsloth.ai/basics/inference) — 4-bit 최적화 + fine-tuned 모델 서빙.
- [MLX](https://github.com/ml-explore/mlx) — Apple Silicon native. M2+ Mac에서 강력.
- [LM Studio](https://lmstudio.ai/) — GUI 앱. 비개발자 테스트용.

## 🔬 실습 (5h)

### 프로젝트: Triple Backend RAG + Benchmark

위치: `projects/day12-local-llm/`

```
day12-local-llm/
├── local/
│   ├── ollama_chat.py          # OpenAI SDK + base_url=localhost:11434/v1
│   ├── ollama_rag.py           # Day 8 RAG의 generator를 Ollama로 교체
│   ├── vllm_local.py           # (Linux/NVIDIA) vllm serve + OpenAI SDK 호출
│   └── mlx_bench.py            # (Mac) MLX 로컬 추론
├── runpod/
│   ├── deploy_notes.md         # RunPod Serverless vLLM 배포 과정 기록
│   ├── vllm_client.py          # https://api.runpod.ai/v2/<endpoint>/openai/v1
│   └── benchmark.py            # latency / tok/s / 비용
├── benchmark/
│   ├── backends.py             # "openai" / "anthropic" / "ollama:qwen3:8b" / "runpod:qwen3-32b"
│   ├── rag_compare.py          # Day 8 RAG을 4개 백엔드로 돌려 Ragas 점수
│   └── results/
├── quantization/
│   ├── pull_gguf.sh            # Q4_K_M / Q5_K_M / Q8_0 다운로드
│   └── quality_vs_vram.py      # 동일 20 쿼리 × 3 quantization 품질 차이
├── decision_matrix.md          # "언제 API / 언제 self-host" 본인 기준
└── README.md
```

### 🔥 필수 기능

1. **Ollama 설치 + 3개 모델 pull**:
   - `qwen3:8b` (한국어 강함, 5GB VRAM)
   - `llama3.3:8b-instruct-q4_K_M` (3.8GB)
   - `gpt-oss:20b` (큰 모델 양자화, 12GB)
2. **OpenAI SDK로 Ollama 호출**:
   ```python
   client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
   r = client.chat.completions.create(model="qwen3:8b", messages=[...])
   ```
3. **Day 8 RAG 교체** — embedding은 OpenAI(품질) / generation은 Ollama(무료) 하이브리드. Day 9 Ragas 돌려 품질 낙폭 측정
4. **RunPod Serverless 배포**:
   - 계정 생성 + $10 충전 (실습용)
   - Serverless > vLLM template → `Qwen/Qwen3-8B-Instruct` 또는 `Qwen/Qwen2.5-32B-Instruct-AWQ` (AWQ 양자화)
   - GPU 선택: 24GB VRAM 등급 (A5000 or L4)
   - MAX_MODEL_LEN=8192, DTYPE=bfloat16
   - Endpoint URL + API key 받음
5. **동일 코드 3개 백엔드**:
   ```python
   for backend in ["gpt-4o-mini", "claude-haiku-4-5", "ollama:qwen3:8b", "runpod:qwen3-8b"]:
       answer, usage, latency = run_rag(backend, question)
   ```
6. **Benchmark matrix** — 20 쿼리 × 4 backend:
   - Answer quality (Ragas faithfulness / answer_relevancy)
   - Latency p50/p95
   - TTFT
   - $/query (실비용)
   - tok/s
7. **Quantization 실험** — 같은 base model(Qwen3-8B)의 Q4_K_M vs Q5_K_M vs Q8_0 (or FP16):
   - VRAM 사용량
   - tok/s
   - 20 쿼리 품질 비교 (Ragas)
   - 사이즈 (GB)

### 🧪 Decision Matrix (본인이 만드는 것)

`decision_matrix.md` 예시:
```
조건                              → 선택
월 <$200 예상, 실험 단계           → API (4o-mini / haiku / flash)
월 >$2000, 안정 트래픽, 단일 모델   → RunPod Serverless vLLM
데이터 이탈 금지 (의료/금융)       → 온프렘 vLLM + RunPod private
응답 지연 <500ms 요구              → RunPod Dedicated Pod (no cold start)
오프라인/에어갭                    → Ollama 로컬
개인 개발 환경, 즉시 테스트         → Ollama 로컬
Fine-tuned 모델 배포               → RunPod + worker-vllm custom
```

### 🔥 Stretch

- 🧪 **llama.cpp 직접 빌드** — Mac에서 `LLAMA_METAL=1 make` → MLX와 성능 비교
- 🧪 **Speculative Decoding** — small draft model + big target로 2-3배 가속 (vLLM 지원)
- 🧪 **Tensor parallel 2 GPUs** — RunPod 다중 GPU에 70B 모델 띄우기
- 🧪 **AWQ / GPTQ / GGUF 비교** — 같은 모델의 다른 양자화 포맷 품질/속도 비교
- 🧪 **TGI 병행** — vLLM vs TGI 동일 모델 throughput 벤치
- 🧪 **Outlines + Ollama** — Day 4 structured output을 로컬 모델에서 문법 강제로 100% 보장

## ⚖️ 수치 기준

| 메트릭 | Ollama local (M2 Mac 16GB 예시) | RunPod Serverless (L4 24GB) |
|---|---|---|
| qwen3:8b Q4 tok/s | 20-40 | 60-150 |
| TTFT | ~500ms | 2-40s (cold start 영향) |
| RAG answer quality vs GPT-4o-mini | 80-90% | 85-95% (bf16) |
| $/1K output tokens | $0 (전기비만) | ~$0.0001-0.0005 |

## ✅ 체크리스트

- [ ] Ollama 3개 모델 pull + `ollama run`으로 대화 성공
- [ ] OpenAI SDK로 Ollama 호출 (base_url 트릭)
- [ ] Day 8 RAG을 Ollama로 generator 교체 후 Ragas 점수 비교
- [ ] RunPod 계정 생성 + Serverless vLLM 배포 성공 + API 호출 확인
- [ ] 4개 백엔드 × 20 쿼리 벤치마크 표
- [ ] Quantization 3단계 실험 (VRAM + 품질)
- [ ] `decision_matrix.md` 본인 기준 작성
- [ ] `cheatsheets/` — `self-host-decision.md` 선택 생성
- [ ] `notes/decisions.md` — "API vs self-host 내 기준선 (월 $X)" 기록

## 🧨 자주 틀리는 개념

1. **"Ollama로 GPT-4 품질 나옴"** — 8B 양자화 모델은 4o-mini 급에 근접. GPT-4o 급은 70B+ 필요 + RunPod에서 AWQ로 겨우.
2. **"Quantization Q4면 품질 붕괴"** — Q4_K_M / Q5_K_M는 일반 RAG에선 체감 차이 거의 없음. Q3 이하부터 눈에 띔.
3. **"vLLM이 Ollama보다 무조건 빠름"** — 대량 동시 요청에선 맞음. 단일 요청은 비슷하거나 Ollama가 나을 수 있음.
4. **"Serverless는 항상 싸다"** — Cold start 많으면 오히려 Dedicated가 쌀 수도. 트래픽 패턴 따라 다름.
5. **"RunPod base_url만 바꾸면 OpenAI SDK 그대로"** — 대부분 맞지만 tool_calling 구현 차이 가끔. 모델 별 chat_template 이슈.
6. **"M-series Mac은 vLLM 불가"** — 현재(2026-04) vLLM의 MPS 지원 제한적. `llama.cpp` / `Ollama` / `MLX`가 Mac 최적.
7. **"PagedAttention 몰라도 됨"** — 개념은 "KV cache를 OS paging처럼" 한 줄이면 충분. 디테일은 필요할 때.

## 🧪 산출물

- `projects/day12-local-llm/` — 전체
- `benchmark/results/matrix.md` — 4 backend × 20 쿼리
- `quantization/results.md` — Q4/Q5/Q8 비교
- `decision_matrix.md` — 본인 기준
- `notes/decisions.md` — self-host 경계선 본인 숫자

## 📌 핵심 키워드

- Ollama — stdlib for local LLM. OpenAI-compatible endpoint.
- llama.cpp / GGUF — CPU/GPU 통합 추론. Q2_K ~ Q8_0 / FP16 / FP32.
- MLX — Apple Silicon native framework.
- vLLM — GPU 중심 throughput serving. PagedAttention + continuous batching + speculative decoding
- TGI (Text Generation Inference) — HuggingFace 엔터프라이즈 서버
- KV cache, PagedAttention, prefix caching
- Continuous batching, in-flight batching
- Quantization: Q4_K_M / Q5_K_M / Q8_0 (GGUF), AWQ / GPTQ (weight-only 4bit)
- Tensor parallel, pipeline parallel, sequence parallel
- RunPod: **Pod** (persistent VM) / **Serverless** (event-driven), Network Volume, GPU classes (L4 / L40S / A100 / H100)
- Cold start, scale-to-zero, autoscale workers
- OpenAI-compatible endpoint (`base_url` 트릭)
- tok/s, TTFT, TBT
- VRAM 요구량 (7B@Q4 ≈ 5GB, 8B@FP16 ≈ 16GB, 70B@Q4 ≈ 40GB)

## ⚠️ 프로덕션 주의

- **Tokenizer 다름** — `Qwen3`은 OpenAI 호환이지만 token 카운트 다름. 비용 계산 유의.
- **Tool calling 지원 편차** — 같은 모델도 vLLM/Ollama의 chat_template 설정 따라 tool parsing 실패.
- **Cold start 대응** — RunPod Serverless는 warm pool 설정 + keep-alive ping으로 완화.
- **Fine-tuned 모델** — LoRA merged로 GGUF 만들기 / vLLM `--enable-lora`로 hot-swap.
- **License 확인** — Llama는 상용 제한 조건, Qwen/Gemma는 Apache/커스텀. 배포 전 license 검토 필수.

## 🎁 내일(Day 14) 미리보기
최종 포트폴리오. 14일 동안 배운 것을 "Devlog RAG Copilot"으로 통합. GitHub 공개 가능한 품질로.
