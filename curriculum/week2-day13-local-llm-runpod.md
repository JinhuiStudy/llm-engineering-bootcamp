# Day 13 — Local LLM + Fine-tuning 전일 (ULTRA — 14h 극한)

> **난이도**: ★★★★★★ (v3 최고)
> **총량**: Local 3h + Fine-tuning 9h + Serving 2h + 정리 = **14h**
> **논문**: LoRA (Hu 2021) + QLoRA (Dettmers 2023) + DPO (Rafailov 2023)
> **GPU 예산**: RunPod H100 $15-25 (4-5시간 훈련)

## 🎯 오늘 끝나면

1. Ollama 로컬 실행 + OpenAI SDK 호출 (1-2h로 압축)
2. RunPod Serverless vLLM 엔드포인트 1개 (1h)
3. **Unsloth로 Qwen3-8B LoRA fine-tuning** 성공 (H100 1-2h 훈련)
4. **QLoRA 4-bit** 압축 fine-tuning (Mac에서도 가능한 경로 체험)
5. **DPO (preference 학습)** 간단 실측 — SFT 결과 대비 선호도 개선 측정
6. Fine-tuned 모델을 **RunPod에 vLLM으로 서빙** → OpenAI SDK로 호출
7. 본인 도메인 데이터로 "**fine-tune이 RAG보다 유리한 경우**" 실증
8. 논문 3편 Figure 수준

## 📚 자료

### 🔥 Local LLM (빠르게 1h)
- [Ollama quickstart](https://docs.ollama.com/) — `ollama pull qwen3:8b`
- [Ollama OpenAI compatibility](https://docs.ollama.com/openai) — base_url 트릭
- [vLLM OpenAI server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)

### 🔥 RunPod Serverless (1h)
- [Serverless vLLM get started](https://docs.runpod.io/serverless/vllm/get-started)
- worker-vllm template 선택 → Qwen3-8B → 엔드포인트 URL

### 🔥🔥 Fine-tuning 메인 (7h)

#### 이론 + 논문 (2h)
- **LoRA paper** (Hu 2021) · [arxiv](https://arxiv.org/abs/2106.09685)
  - Figure 1: rank decomposition. 원가중치 freeze, ΔW = BA (low-rank) 학습
  - 파라미터 0.01-1%만 학습. 메모리 3배 절감
- **QLoRA paper** (Dettmers 2023) · [arxiv](https://arxiv.org/abs/2305.14314)
  - 4-bit quantization + LoRA. 65B 모델 single GPU에
  - NF4 / Double Quantization / Paged Optimizers
- **DPO paper** (Rafailov 2023) · [arxiv](https://arxiv.org/abs/2305.18290)
  - RLHF의 PPO 대체. 선호 pairs (chosen vs rejected)로 직접 최적화
  - PPO 복잡성 제거, 실용성 ↑

#### Unsloth 튜토리얼 (1h — Colab 체험)
- [Unsloth docs](https://docs.unsloth.ai/) ⭐ — **2-5x 빠른 LoRA**
- [Unsloth — Qwen3 LoRA notebook](https://github.com/unslothai/notebooks) — 이거 그대로 kickoff
- [HF PEFT](https://huggingface.co/docs/peft/index) — LoRA 이론 backing
- [HF TRL](https://huggingface.co/docs/trl/index) — SFT / DPO trainer

#### 대안 참조
- [Axolotl](https://github.com/axolotl-ai-cloud/axolotl) — 더 체계적, 실무 적합
- [OpenAI Fine-tuning (GPT-4o-mini)](https://platform.openai.com/docs/guides/fine-tuning) — 프로바이더 fine-tune 대안

## 🔬 실습 (9h)

### 프로젝트: `day12-local-llm/` 확장

```
day12-local-llm/
├── local/                          # 1h로 빠르게
│   ├── ollama_chat.py
│   └── ollama_rag.py
├── runpod/                         # 1h
│   └── vllm_client.py
├── finetune/                       # 오늘의 메인 (7-8h)
│   ├── prepare_data.py             # 본인 데이터 → ShareGPT/OpenAI format
│   ├── train_lora.py               # Unsloth LoRA SFT
│   ├── train_qlora.py              # 4-bit QLoRA
│   ├── train_dpo.py                # DPO preference
│   ├── eval_before_after.py        # Ragas로 tuned vs base 비교
│   ├── merge_and_gguf.py           # LoRA merge → GGUF export (Ollama 호환)
│   └── serve_runpod.py             # Fine-tuned 모델 RunPod vLLM 배포
├── data/
│   ├── sft.jsonl                   # SFT 데이터 (본인 도메인 50-200건)
│   └── dpo.jsonl                   # chosen/rejected pairs 30-50건
└── README.md
```

### 🎯 본인 도메인 데이터 (1h)

Fine-tune의 가치 증명을 위해 **RAG로 잘 안 되는 태스크** 고르기:
- 예: "내 블로그 스타일로 기술 질문 답변" (tone/format)
- 예: "특정 회사 내부 약어로 응답" (domain vocabulary)
- 예: "한국어 공식 문서 스타일" (style transfer)

데이터 포맷 (`data/sft.jsonl`):
```json
{"messages": [
  {"role": "user", "content": "Q..."},
  {"role": "assistant", "content": "A (본인 스타일)"}
]}
```

50-200건이면 충분 (Unsloth는 작은 데이터도 OK).

### 🔥 Step 1 — Unsloth LoRA SFT (4h 중 훈련 1-2h + 대기)

```python
# train_lora.py (Unsloth)
from unsloth import FastLanguageModel
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-8B-bnb-4bit",  # 이미 4-bit 양자화된 base
    max_seq_length=4096,
    dtype=torch.bfloat16,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,                            # LoRA rank
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    lora_alpha=16,
    lora_dropout=0.0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
)

# 데이터 로드 + chat template 적용
from datasets import load_dataset
ds = load_dataset("json", data_files="data/sft.jsonl", split="train")
ds = ds.map(lambda x: {"text": tokenizer.apply_chat_template(x["messages"], tokenize=False)})

from trl import SFTTrainer, SFTConfig
trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=ds,
    args=SFTConfig(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        learning_rate=2e-4,
        bf16=True,
        logging_steps=5,
        output_dir="outputs/sft",
        report_to="none",
    ),
)
trainer.train()
model.save_pretrained("outputs/sft/lora")   # adapter만 저장
```

**GPU 선택**: RunPod Pod H100 80GB ($3-4/h). 8B Q4 기준 메모리 여유.
**훈련 시간**: 150 샘플 × 3 epoch → ~30-60분.

### 🔥 Step 2 — QLoRA 비교 (1h)

동일 데이터로 4-bit QLoRA:
```python
# train_qlora.py (BitsAndBytes)
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-8B-Instruct", quantization_config=bnb
)
# ... (LoraConfig + SFTTrainer 동일)
```

**비교**: VRAM 사용량, 훈련 속도, 최종 loss.

### 🔥 Step 3 — DPO Preference 학습 (2h)

SFT 모델을 추가로 선호 pair에 맞게 조정:

```python
# data/dpo.jsonl
{"prompt": "...", "chosen": "좋은 답변", "rejected": "나쁜 답변"}
```

```python
# train_dpo.py
from trl import DPOConfig, DPOTrainer
from unsloth import FastLanguageModel

# SFT 결과 로드
model, tokenizer = FastLanguageModel.from_pretrained(
    "outputs/sft/lora", load_in_4bit=True
)
model = FastLanguageModel.get_peft_model(model, r=16, ...)

trainer = DPOTrainer(
    model=model, tokenizer=tokenizer,
    train_dataset=dpo_ds,
    args=DPOConfig(
        beta=0.1,
        per_device_train_batch_size=2,
        num_train_epochs=1,
        learning_rate=5e-6,
        output_dir="outputs/dpo",
    ),
)
trainer.train()
```

### 🔥 Step 4 — Eval (Before vs After) 1.5h

```python
# eval_before_after.py
from ragas import evaluate
from ragas.metrics import Faithfulness, ResponseRelevancy

# 동일 20 쿼리 × 3 모델 (base / SFT / DPO)
for model_name in ["qwen3:8b", "sft-merged", "dpo-merged"]:
    results = [run_rag(q, model=model_name) for q in queries]
    metrics = evaluate(results, [Faithfulness(), ResponseRelevancy()])
    print(model_name, metrics)
```

**기대**: SFT > base (domain), DPO > SFT (alignment).
**수치 기록**: `results/finetune_eval.md`

### 🔥 Step 5 — Serving (1h)

#### Option A: Ollama 로컬 (GGUF 변환)
```bash
# merge_and_gguf.py — LoRA adapter를 base에 merge → GGUF 변환
python merge_and_gguf.py --adapter outputs/dpo --out qwen3-8b-devlog.gguf

# Ollama Modelfile
FROM ./qwen3-8b-devlog.gguf
PARAMETER temperature 0.3

# 실행
ollama create devlog -f Modelfile
ollama run devlog
```

#### Option B: RunPod vLLM serving
```yaml
# RunPod Serverless Endpoint 설정
MODEL_NAME: "your-hf-username/qwen3-8b-devlog-sft"   # HF Hub push 필요
DTYPE: "bfloat16"
MAX_MODEL_LEN: 8192
```

```python
# 호출
client = OpenAI(
    base_url=f"https://api.runpod.ai/v2/{ENDPOINT_ID}/openai/v1",
    api_key=os.getenv("RUNPOD_API_KEY")
)
r = client.chat.completions.create(model="qwen3-8b-devlog-sft", messages=[...])
```

### 📊 수치 기준 (넘어야 할 선)

| 메트릭 | Base (Qwen3-8B) | SFT 후 | DPO 후 |
|---|---|---|---|
| Style 일치율 (judge) | ~0.3 | ≥ 0.7 | ≥ 0.8 |
| Ragas Faithfulness | ~0.78 | ≥ 0.82 | ≥ 0.85 |
| VRAM (4-bit) | ~5GB | ~6GB | ~6GB |
| 훈련 시간 (H100) | — | 30-60m | +15-30m |
| 총 비용 | — | ~$3-5 | +$1-2 |

## ✅ 체크리스트

- [ ] Ollama `qwen3:8b` 호출 + OpenAI SDK 연결
- [ ] RunPod Serverless endpoint 1개 배포
- [ ] SFT 데이터 50-200건 본인 도메인
- [ ] Unsloth LoRA SFT 훈련 **완료** (loss 수렴)
- [ ] QLoRA 버전도 실행 — VRAM/속도 비교
- [ ] DPO 데이터 30건 + 훈련 1 epoch
- [ ] Ragas eval base vs SFT vs DPO 표
- [ ] LoRA merge + GGUF 변환 + Ollama 서빙 or RunPod 배포
- [ ] `notes/decisions.md` — "RAG vs Fine-tune 선택 기준" 본인 기준선
- [ ] 논문 3편 Figure 수준 요약 (LoRA/QLoRA/DPO)

## 🧨 실전 함정

1. **Unsloth 설치 실패** — Linux + CUDA 11.8+/12 필수. Mac 불가. RunPod Pod에서만
2. **Qwen3-8B FP16 VRAM 부족** — 4-bit QLoRA 필수 or RunPod A100/H100
3. **SFT 데이터 50건 미만** — underfit 또는 overfit. 100건 이상 권장
4. **DPO의 `beta` 파라미터** — 너무 크면 기존 능력 붕괴, 너무 작으면 preference 학습 안 됨. 0.1 권장
5. **GGUF 변환 실패** — `llama.cpp/convert-hf-to-gguf.py` 사용. Unsloth는 지원 모델 제한
6. **훈련 중 interrupt** — RunPod Spot이면 checkpoint 자주. `save_steps=50`
7. **Fine-tuned 모델이 bias 학습** — eval 필수, 맹신 금지
8. **Tokenizer chat template 불일치** — 훈련 시 템플릿과 서빙 시 템플릿 동일해야
9. **H100 예약 실패** — peak 시간 (PT 저녁) 피하기. A40 / L40S도 ok

## 🎁 Stretch

- 🧪 **HF Hub 업로드** — `model.push_to_hub("devlog-qwen3-8b")` → RunPod deploy + 공유
- 🧪 **Axolotl 실행** — Unsloth 대비 체계 비교
- 🧪 **Merge 대신 LoRA 그대로** — vLLM `--enable-lora`로 hot-swap
- 🧪 **Evaluation harness** — `lm-eval-harness`로 MMLU/HellaSwag 점수 변화
- 🧪 **Constitutional AI** — Anthropic 스타일로 "harmful 거절" 학습

## 💰 예산 관리 (v3 중요)

오늘만 최대 **$25 GPU 소비**. 넘어가면 강제 중단:
- H100 80GB: $3.29/h (RunPod 기준)
- 4h 훈련 + 1h 실험 = $16
- Serverless 실험 $5-10
- **총 $20-25 안쪽으로 끊기**

## 📜 논문 요약 ↓ `notes/concepts.md`

각 논문 Figure + Abstract + 3줄 본인 설명. LoRA의 Figure 1 (rank decomposition), QLoRA의 Figure 1 (4-bit NF4), DPO의 Figure 1 (preference probability).

## 🎁 내일(Day 14) 미리보기
**Mega Portfolio + Advanced Topics Rapid Fire**. Fine-tuned 모델을 포트폴리오에 통합 + MoE/Speculative/FlashAttention/Distillation/분산 훈련 **개념 rapid fire** + 논문 5편 + GitHub 공개.
