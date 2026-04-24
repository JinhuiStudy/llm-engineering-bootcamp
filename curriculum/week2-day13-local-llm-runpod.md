# Day 13 — Local LLM + RunPod (Self-Hosting)

## 목표
- 로컬에서 Ollama로 LLM 돌리고 OpenAI SDK로 그대로 호출
- vLLM OpenAI-compatible 서버 이해
- RunPod Serverless로 vLLM 엔드포인트 띄워서 클라우드 GPU 인퍼런스 경험
- 언제 API vs self-hosted를 써야 하는지 의사결정 기준 확보

## 자료

### Local LLM
| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [Ollama 공식 사이트](https://ollama.com/) | 0.5h |
| 필수 | [Ollama docs](https://docs.ollama.com/) | 1h |
| 필수 | [Ollama API docs](https://github.com/ollama/ollama/blob/main/docs/api.md) | 0.5h |
| 필수 | [vLLM docs](https://docs.vllm.ai/) | 1h |
| 필수 | [vLLM OpenAI-compatible server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server/) | 0.5h |
| 선택 | [llama.cpp](https://github.com/ggml-org/llama.cpp) | 0.5h |
| 선택 | [llama-cpp-python server](https://llama-cpp-python.readthedocs.io/en/latest/server/) | 0.5h |
| 선택 | [HF Transformers docs](https://huggingface.co/docs/transformers/index) | 나중에 |
| 선택 | [HF Text Generation Inference (TGI)](https://huggingface.co/docs/text-generation-inference/index) | 나중에 |

### RunPod
| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [RunPod 공식](https://www.runpod.io/) | 0.5h |
| 필수 | [RunPod docs](https://docs.runpod.io/) | 1h |
| 필수 | [RunPod Pods overview](https://docs.runpod.io/pods/overview) | 0.5h |
| 필수 | [RunPod Serverless overview](https://docs.runpod.io/serverless/overview) | 0.5h |
| 필수 | [RunPod Serverless vLLM — get started](https://docs.runpod.io/serverless/vllm/get-started) | 1h |
| 필수 | [RunPod Serverless vLLM — configuration](https://docs.runpod.io/serverless/vllm/configuration) | 0.5h |
| 필수 | [vLLM on RunPod deployment](https://docs.vllm.ai/en/latest/deployment/frameworks/runpod/) | 0.5h |
| 선택 | [runpod-workers/worker-vllm](https://github.com/runpod-workers/worker-vllm) | 0.5h |

### 모델 찾기
| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [HF Models](https://huggingface.co/models) | 0.5h |
| 필수 | [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) | 0.5h |
| 필수 | [Chatbot Arena Leaderboard](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard) | 0.5h |
| 선택 | [LMArena](https://lmarena.ai/) | 0.5h |
| 선택 | [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) | — |

## 실습 (5h)

### 프로젝트: 로컬 + RunPod 이중 백엔드
위치: `projects/day12-local-llm/`

```
day12-local-llm/
├── local/
│   ├── ollama_chat.py         # OpenAI SDK → Ollama (base_url=http://localhost:11434/v1)
│   ├── ollama_rag.py          # Day 6 RAG을 Ollama로 교체
│   └── compare.py             # 동일 쿼리로 GPT-4o-mini vs qwen2.5:7b 비교
├── runpod/
│   ├── deploy_notes.md        # RunPod Serverless vLLM 배포 기록
│   ├── vllm_client.py         # OpenAI SDK → RunPod endpoint
│   └── benchmark.py           # 토큰/초, 지연, 비용 측정
└── README.md
```

### 요구사항
1. **Ollama 설치** + `ollama pull qwen2.5:7b` (또는 llama3.1:8b / phi3.5)
2. OpenAI 파이썬 SDK로 `base_url="http://localhost:11434/v1"`, `api_key="ollama"` 설정해서 로컬 호출
3. Day 6 RAG을 embedding은 OpenAI / generation은 Ollama로 바꿔 비용 제로 RAG 구성
4. **RunPod Serverless 배포**:
   - RunPod 계정 가입 (무료, 크레딧 없어도 문서는 다 봄)
   - Serverless endpoint에 `worker-vllm` template으로 Qwen/Llama 배포
   - API key 받아서 OpenAI SDK로 호출
5. 같은 쿼리로 비용/속도/품질 3개 백엔드 비교표:
   - OpenAI API
   - Ollama (local)
   - RunPod Serverless vLLM

### Stretch
- `llama.cpp` 또는 `llama-cpp-python` 로 GGUF 모델 서빙
- TGI로 Hugging Face 모델 서빙 비교
- 동일 프롬프트의 Ollama/vLLM temperature 재현성 비교 (seed 효과)

## 체크리스트

- [ ] Ollama 로컬에서 모델 다운로드 + 호출
- [ ] OpenAI SDK로 Ollama 호출 (API 호환성 실증)
- [ ] vLLM 로컬 실행 (Mac에서는 MPS 이슈, CPU fallback) 또는 RunPod에서 실증
- [ ] RunPod Serverless endpoint 1개 이상 배포 성공
- [ ] "언제 self-host인가" 의사결정 기준 작성 (`notes/concepts.md`)

## 의사결정 기준 (작성해 둘 것)
- API: 실험 단계, 트래픽 변동 큼, 최신 모델 필요 → 시간 대비 비용 최저
- Self-host (RunPod/vLLM): 대량 호출 (월 수천만 토큰+), 데이터 이탈 금지, 지연 제어, fine-tuned 모델 사용
- Ollama 로컬: 개발/테스트, 오프라인 데모
- 참고 경계선: 월 <$200 → API, 월 >$1000 → self-host 검토, 월 >$5000 → 거의 확실히 self-host

## 핵심 키워드
- Ollama, llama.cpp, GGUF, quantization (Q4_K_M, Q8_0)
- vLLM, PagedAttention, continuous batching
- OpenAI-compatible endpoint (base_url 트릭)
- Cold start, warm pool, autoscaling to zero (RunPod Serverless)
- GPU class (A100/H100/L40S), VRAM 요구 (7B Q4 ≈ 5GB, 70B Q4 ≈ 40GB)
- TGI, vLLM, Ollama, llama.cpp 선택 기준
- RunPod: Pod (persistent), Serverless (event-driven), Network Volume
