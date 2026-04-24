# Day 13 — Local LLM + RunPod

커리큘럼: `curriculum/week2-day13-local-llm-runpod.md`

## 체크리스트 — Local (Ollama)
- [ ] `ollama pull qwen2.5:7b` (또는 llama3.1:8b)
- [ ] OpenAI SDK로 Ollama 호출 (base_url=http://localhost:11434/v1)
- [ ] Day 6 RAG를 Ollama로 generation 교체 → 비용 0 RAG
- [ ] GPT-4o-mini vs qwen2.5:7b 동일 쿼리 비교

## 체크리스트 — RunPod
- [ ] RunPod 계정 + 카드 등록 (또는 크레딧)
- [ ] Serverless endpoint에 worker-vllm template 배포
- [ ] Qwen/Llama 모델 선택, GPU 타입 결정
- [ ] API key 받아 OpenAI SDK로 호출
- [ ] `benchmark.py` — tokens/sec, cold start 측정
- [ ] `deploy_notes.md` — 배포 과정 기록 (막혔던 지점 포함)

## 체크리스트 — 비교
- [ ] OpenAI vs Ollama vs RunPod 비용/속도/품질 표
- [ ] "언제 self-host인가" 기준을 `notes/concepts.md`에 작성

## Stretch
- llama.cpp (GGUF) 서빙
- TGI 비교
