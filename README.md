# Project Hive — MVP v0.1

실시간 맥락 통합형 멀티모달 오케스트레이터의 첫 번째 마일스톤.
파인튜닝된 인텐트 분류기가 사용자 요청을 분석하고, 복잡도에 따라
로컬 LLM과 클라우드 LLM 사이를 자동으로 라우팅한다.

## 동작 방식

```
사용자 프롬프트
    ↓
[Laya 인텐트 분류기] — 작업 종류 11종 + 복잡도 3단계 분류 (파인튜닝됨)
    ↓
[라우터] — 복잡도 low → 로컬 / medium·high → 클라우드
    ↓                    ↓
Ollama (로컬, 무료)   Groq 무료 플랜 (클라우드)
```

## 실행

```bash
pip install laya openai
ollama pull qwen2.5:3b          # 로컬용 (https://ollama.com)

# Windows PowerShell
$env:GROQ_API_KEY="..."        # https://console.groq.com/keys (무료)

python -m hive "이 보고서 3줄로 요약해줘"
```

실행 예시:

```
분류 중...
작업 종류: 요약 (확신도 0.93)
복잡도: low (확신도 0.66)
→ 라우팅: Ollama (로컬)

(모델 답변...)
```

## 환경변수

| 변수 | 기본값 | 설명 |
|---|---|---|
| `GROQ_API_KEY` | (필수) | Groq API 키 |
| `GROQ_MODELS` | `openai/gpt-oss-120b,qwen/qwen3.6-27b` | 폴백 체인 (앞에서부터 시도) |
| `OLLAMA_MODEL` | `qwen2.5:3b` | Ollama 모델명 |
| `LAYA_MODEL_PATH` | `./hive_intent_laya` | 파인튜닝 체크포인트 경로 |
| `HIVE_SYSTEM_PROMPT` | (대화체 기본값) | 답변 스타일 지정 |

## 인텐트 분류기 학습

- 학습 데이터: `training/hive_typed_decisions.jsonl` (한국어 598 케이스, 11개 작업 종류 × 3단계 복잡도)
  → [Google Drive에서 다운로드](https://drive.google.com/file/d/1n6HOmBc-QASP6YgseINcxGSl-tlJE0FS/view?usp=drivesdk) (용량 문제로 레포에 직접 포함하지 않음)
- 학습 노트북: `training/hive_finetune_colab.ipynb` (Laya-multilingual 파인튜닝, Colab T4)
- 검증 정확도: 작업 종류 78.0% / 복잡도 74.6% (59 케이스)
- 체크포인트(`hive_intent_laya/`, 약 1.1GB)는 용량 문제로 레포에 포함하지 않음.
  위 노트북으로 직접 학습하거나, 별도로 공유된 체크포인트를 `LAYA_MODEL_PATH`에 배치.

## 구조

```
hive/
├── __main__.py        # CLI 진입점
├── classifier.py      # Laya 인텐트 분류기 래퍼
├── router.py          # 복잡도 기반 라우팅
├── config.py          # 환경변수 설정
└── adapters/
    ├── ollama.py      # Ollama 로컬 어댑터
    └── groq.py        # Groq 클라우드 어댑터 (폴백 체인)
test_intent.py         # 분류기 단독 테스트
training/              # 학습 데이터 + 노트북
```

## 다음 단계

- [ ] 멀티모달 입력 (이미지·음성)
- [ ] 대화 맥락 메모리
- [ ] 라우팅 로그 대시보드
- [ ] 분류기 정확도 개선 (데이터 증강)
