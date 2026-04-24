# Day 1 — LLM 기초 / Transformer / 논문 2편 (ULTRA)

> **난이도**: ★★★ (v3에서 재상향)
> **총량**: 읽기 4h + 실습 5h + 논문 2편 2h + 정리 1h = **12h**.
> **전제**: Python 3.11+, `uv`/`pip` 능숙, 터미널 익숙.
> **논문**: Attention Is All You Need + Chinchilla (Figure 수준)

## 🎯 오늘 끝나면 할 수 있어야 하는 것

1. "GPT는 무엇을 예측하는가"를 **30초**에 설명 (정답: *다음 토큰의 확률 분포*, `argmax`가 아닌 `sampling`)
2. "왜 Transformer가 RNN/LSTM을 대체했는가"를 3가지 수치 근거로 답변 (병렬화 / long-range dependency / 학습 안정성)
3. "한국어 1000자 = 대략 몇 토큰?"을 **실측 데이터로** 답 (답: cl100k 기준 ~1200, o200k는 ~600~700, Claude BPE는 ~1400)
4. Temperature / Top-p / Top-k / frequency_penalty / presence_penalty **각각이 분포의 어디를 건드리는지** 설명
5. KV cache가 왜 존재하고, context 길어질수록 왜 메모리가 제곱이 아닌 선형으로 증가하는지 설명 (paged attention은 내일 맛보기)

## 📚 자료 (우선순위 + TL;DR)

### 🔥 필수 (4.5h)

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 1.5h | [Google ML Crash Course — LLM 섹션](https://developers.google.com/machine-learning/crash-course/llm) | LLM 작동 원리 코스. 전반부는 n-gram → RNN → Transformer 진화 스토리, 후반부는 pretraining/fine-tuning/prompt distinction. **한국어 버전 있음**. |
| 1h | [Google ML CC — Transformers](https://developers.google.com/machine-learning/crash-course/llm/transformers) | Self-attention의 "query / key / value가 왜 3개인가"를 직관으로 설명. 수식 없이 시작해서 점진적으로. |
| 0.5h | [3Blue1Brown — "But what is a GPT?"](https://www.youtube.com/watch?v=wjZofJX0v4M) | 시각화 천재 Grant Sanderson의 27분. Attention이 "단어가 서로 쳐다보며 의미를 업데이트하는 것"이라는 멘탈 모델 1회 박아버리기. |
| 0.5h | [3Blue1Brown — Attention 편](https://www.youtube.com/watch?v=eMlx5fFNoYc) | 위 영상 심화. softmax(QK^T/√d)V를 그림으로. 수식 공포증 치유. |
| 0.5h | [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) | 교과서. Figure 한 장 = 논문 섹션 하나. multi-head / positional encoding 감각 체득. |
| 0.5h | [Attention Is All You Need](https://arxiv.org/abs/1706.03762) ([PDF](https://arxiv.org/pdf/1706.03762)) | **읽지 말고 훑어라.** Abstract + Figure 1(architecture) + Figure 2(attention) + Table 1(벤치). 풀텍스트는 나중에. Claude한테 "이 논문의 3대 기여를 bullet 5개로"라고 요약 시키는 게 더 효율적. |

### ⭐ 강력 권장 (1.5h)

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [Karpathy — Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) | 2h짜리지만 **처음 30분만**. BPE(Byte-Pair Encoding)가 왜 이 모양이 됐는지 — 공백/유니코드/emoji/code가 어떻게 토큰화되는지 직접 돌려봄. |
| 30m | [tiktokenizer.vercel.app](https://tiktokenizer.vercel.app/) | OpenAI tokenizer 실시간 비주얼라이저. 한국어/코드/이모지 붙여보며 "왜 한국어가 비싼지" 체감. cl100k_base vs o200k_base 비교 UI 있음. |
| 30m | [HF NLP Course Ch 1](https://huggingface.co/learn/nlp-course/chapter1) | HuggingFace 생태계 진입 토큰. pipeline, model hub 구경. |

### 🎓 선택 (여력 있을 때)

- [Karpathy — Let's build GPT from scratch (nanoGPT)](https://www.youtube.com/watch?v=kCc8FmEb1nY) — 2h. GPT-2 ~100 lines로 짜기. **Week 2 이후에 보상용**.
- [Formal Algorithms for Transformers (DeepMind)](https://arxiv.org/abs/2207.09238) — 수식으로 정확히 정의된 판본. 엔지니어가 1회쯤 읽으면 모호함이 사라진다.
- [RoPE Explained (Su et al.)](https://arxiv.org/abs/2104.09864) — 현대 LLM(LLaMA/Qwen 등)의 positional encoding. Week 2 고급.

## 🔬 실습 (4.5h)

### Task 1 — 토큰 해부학 (1h)

```bash
cd /Users/parkjinhui/Desktop/dev/ai-study/projects/day01-chatbot-cli
uv venv && source .venv/bin/activate
uv pip install tiktoken anthropic openai google-genai python-dotenv rich
```

`tokens.py` 작성 요구사항:

1. 3사 토크나이저(`tiktoken cl100k_base`, `tiktoken o200k_base`, Claude는 `anthropic` SDK의 `count_tokens` / Gemini는 `client.models.count_tokens`)로 같은 텍스트 카운트
2. 텍스트 세트: 한국어(500자 에세이) / 영어(500단어) / Python 코드 / JSON / emoji/ 한자 섞은 문장
3. **토큰/글자 비율**(CPT, Chars-per-Token) 표로 출력
4. **비용 추정**: 각 provider의 모델별 $/1M tokens (직접 매핑 dict 관리) × 토큰 수 → 실비용 추정

출력 예시 (기대):
```
                 cl100k  o200k  Claude  Gemini-Flash
한국어 500자       ~600   ~330   ~700    ~550
영어  500단어      ~650   ~620   ~680    ~700
Python 200 line   ~2100  ~1800  ~2300   ~2000
```

💡 **관찰 포인트**: OpenAI의 `o200k_base`(GPT-4o)가 한국어에 대해 `cl100k_base`(GPT-3.5/4)보다 **거의 2배 효율**. 같은 한국어 RAG 시스템을 GPT-4 → 4o로 바꾸는 것만으로 토큰 비용이 반토막 나는 이유.

### Task 2 — Sampling 파라미터 지도 (1.5h)

`temperature_demo.py`에서 같은 프롬프트를 다음 그리드로 5회씩 호출하여 Hamming/edit distance로 **출력 다양성 점수화**:

| Grid | temperature | top_p | top_k | 기대 |
|---|---|---|---|---|
| Deterministic | 0.0 | 1.0 | — | 5/5 identical |
| Default | 0.7 | 1.0 | — | 미세 변주 |
| Creative | 1.2 | 1.0 | — | 다양 |
| Nucleus cut | 0.7 | 0.5 | — | 변주 적음 |
| Top-k cut | 0.7 | 1.0 | 10 | 변주 적음 |
| Chaos | 1.8 | 0.95 | — | 붕괴(glitch) 관찰 |

프롬프트 3종:
- "Write a haiku about debugging" (창의)
- "What is 127 * 83? Output only the number." (사실)
- "List 5 causes of deadlocks in Python." (구조적 knowledge)

📊 **수치 기준**: 같은 프롬프트 5회 출력의 평균 normalized Levenshtein distance를 구하고, `results.md`에 표로 기록. **temp=0인데도 0이 아닌 경우**는 왜일까? (힌트: batch inference, mixture-of-experts routing, floating point non-determinism)

### Task 3 — 토큰 레벨 확률 들여다보기 (1h) 🔥 **하드**

OpenAI `logprobs=True, top_logprobs=5` 옵션으로 "I'm feeling" 뒤에 오는 top-5 토큰과 확률을 로그로 저장. 같은 문장을 temperature 0/1/2로 돌려서:
- 분포 엔트로피 계산 (`-Σ p log p`)
- top-1과 top-5의 확률 gap 관찰
- "temperature가 logit을 나누는 것"이라는 개념을 실측으로 확인 (T 올리면 분포가 평평해짐)

참고: [OpenAI Cookbook — Logprobs](https://cookbook.openai.com/examples/using_logprobs) — "Token probability를 classifier score로 쓰는 법" 소개. **이 쿡북 자체를 읽을 것**.

### Task 4 — KV 캐시 체감 (1h, Stretch)

Ollama로 `qwen2.5:3b` 띄우고 (Day 13 내용 당겨쓰기):
1. 짧은 prompt(100 tokens) + 짧은 generation(50 tokens) × 10회 — 총 레이턴시 기록
2. 긴 prompt(4000 tokens) + 짧은 generation(50 tokens) × 10회 — TTFT만 길어지고 tok/s는 유사함을 관찰
3. **Prefill vs Decode 단계 분리**: TTFT = prefill 시간, 나머지 = decode 시간. 엔지니어링 최적화가 어디 걸리는지 체감.

## ✅ 체크리스트

- [ ] Transformer의 encoder/decoder 차이를 **예시와 함께** 설명 (번역/임베딩/생성 각각)
- [ ] "Self-attention이 왜 필요한가"를 RNN의 정보 전달 한계와 비교해 설명
- [ ] 한국어 한 문장이 모델마다 다른 토큰 수를 냄을 실측 파일로 증명
- [ ] Temperature 0과 1.5의 분포 변화를 logprob 수치로 설명
- [ ] `.env`에 OPENAI / ANTHROPIC / GEMINI 키 3종 로드 확인 (`make verify` 통과)
- [ ] `notes/keywords.md`에 Tier S 용어 15개 이상 본인 말로 정리
- [ ] `daily-log.md` — "오늘 가장 의외였던 것 1개 + 내일 복수하고 싶은 개념 1개"

## 🧨 자주 틀리는 개념 (스스로 채점용)

1. **"Temperature 0은 결정적이다"** → 부분적으로 false. Tie-breaking, batch routing, FP 비결정성으로 같은 temp 0이어도 다른 출력 가능.
2. **"Context window 128k면 128k 다 써도 품질 유지"** → false. **Lost in the Middle** 현상 — 중간에 넣은 정보는 무시되는 경향. ([Liu et al. 2023](https://arxiv.org/abs/2307.03172) — "Lost in the Middle: How Language Models Use Long Contexts")
3. **"Token ≈ 글자 / 4"** → 영어만. 한국어는 글자당 0.5-1.5 토큰, 공백 유무도 영향.
4. **"Attention은 2차 복잡도라서 long-context 못함"** → 2024-2026년 Flash Attention / Sliding Window / Ring Attention / Infini-attention 등으로 1M+ 실용화. 복잡도는 여전히 O(n²) 계열이지만 상수가 확 줄었다.
5. **"temperature 올리면 창의적"** → temperature 자체는 **분포를 평평하게** 만들 뿐. 분포 자체가 평범하면 평범한 결과만 다양하게 나온다.

## 🧪 산출물

- `projects/day01-chatbot-cli/tokens.py` — 3사 토크나이저 비교 + 비용 추정
- `projects/day01-chatbot-cli/temperature_demo.py` — sampling 파라미터 그리드 + 다양성 수치화
- `projects/day01-chatbot-cli/logprobs_demo.py` — logprob 엔트로피 분석
- `notes/keywords.md` — 최소 15개 (token, context window, temperature, top-p, top-k, sampling, attention, self-attention, cross-attention, multi-head attention, decoder-only, encoder-decoder, logit, softmax, logprob, KV cache, positional encoding, layer norm, residual, embedding dim)
- `notes/daily-log.md` — Day 1 섹션

## 🎁 내일(Day 2) 미리보기
3사 API의 실제 호출 차이. OpenAI `chat.completions` vs `responses`, Anthropic `messages` + top-level `system`, Gemini `generate_content`. Streaming 3사의 SSE 포맷 다름.

## 📌 핵심 키워드 (Tier S → Tier A)

**Tier S (입에 붙어야 함)**: token, context window, temperature, top-p, top-k, logit, softmax, sampling, embedding, attention, self-attention, decoder-only, KV cache, TTFT, tok/s

**Tier A (설명 가능해야 함)**: positional encoding(absolute/RoPE), layer normalization, residual connection, feed-forward, multi-head attention, causal mask, autoregressive, BPE/SentencePiece, logprob, perplexity, n-gram baseline, RNN/LSTM 한계, Flash Attention(이름만), sliding window attention(이름만)

## 📜 논문 2편 Figure 레벨 (v3 추가, 2h)

### 1. Attention Is All You Need (Vaswani 2017)
- [arxiv](https://arxiv.org/abs/1706.03762) · [PDF](https://arxiv.org/pdf/1706.03762)
- **읽을 것**: Abstract / Figure 1 (전체 구조) / Figure 2 (attention heads) / Section 3.2 (Attention) / Table 1 (결과)
- **Claude 요약 프롬프트**: "Summarize the 3 key contributions of the Transformer paper and why each mattered. Bullet points only, 5 total."
- **본인 정리 3줄** → `notes/concepts.md`에 "Transformer 핵심" 섹션

### 2. Chinchilla (Hoffmann 2022)
- [arxiv](https://arxiv.org/abs/2203.15556)
- **읽을 것**: Abstract / Figure 1 (scaling law) / Table 3 (70B vs 280B 비교) / Section 4 결과
- **핵심**: "모델 파라미터 수 × 훈련 데이터 토큰 수의 최적 비율 = ~20토큰/파라미터"
- **왜 중요**: 이후 LLaMA/Qwen 등이 data-heavy로 방향 전환한 이유
- **본인 정리 3줄**

## 🔗 Further Reading (여력 있을 때)

- [Lost in the Middle (Liu 2023)](https://arxiv.org/abs/2307.03172) — 긴 컨텍스트 중간 무시
- [The Illustrated Word2vec](https://jalammar.github.io/illustrated-word2vec/) — embedding 감각 (Day 6 예습)
- [Sebastian Raschka — Understanding LLMs](https://magazine.sebastianraschka.com/p/understanding-large-language-models)
- [Karpathy — nanoGPT](https://github.com/karpathy/nanoGPT) — ~300줄 GPT 구현
