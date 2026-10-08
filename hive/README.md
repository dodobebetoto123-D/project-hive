# Hive MVP v0.1 — 라우터 CLI

프롬프트를 파인튜닝된 Laya 인텐트 분류기로 분류하고,
복잡도에 따라 Ollama(로컬) 또는 Groq 무료 플랜(클라우드)로 자동 라우팅합니다.

## 설치

```powershell
pip install laya openai
```

### Ollama (로컬용)

1. https://ollama.com 에서 Windows용 설치
2. 모델 다운로드:
```powershell
ollama pull qwen2.5:3b
```
3. `ollama serve`가 실행 중이어야 합니다 (보통 자동 실행).

### 파인튜닝 체크포인트

`hive_intent_laya` 폴더를 이 README와 같은 위치(`project-hive/`)에 두세요.
다른 경로라면 `LAYA_MODEL_PATH` 환경변수로 지정합니다.

## API 키 설정

https://console.groq.com/keys 에서 API 키를 발급받은 뒤 (무료, 카드 불필요, 키는 `gsk_`로 시작),
Windows PowerShell에서:

```powershell
$env:GROQ_API_KEY = "..."
```

Groq 무료 플랜으로 사용 가능합니다.

## 실행

`project-hive` 폴더에서:

```powershell
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

## 환경변수 (선택)

| 변수 | 기본값 | 설명 |
|---|---|---|
| `GROQ_API_KEY` | (필수) | Groq API 키 (console.groq.com/keys 발급, 무료) |
| `OLLAMA_MODEL` | `qwen2.5:3b` | Ollama 모델명 |
| `GROQ_MODELS` | `openai/gpt-oss-120b,qwen/qwen3.6-27b` | 폴백 체인: 쉼표로 구분된 모델 ID 목록. 앞에서부터 시도하고, 사용 불가(404/429/503)면 다음 모델로 넘어감 |
| `LAYA_MODEL_PATH` | `./hive_intent_laya` | 파인튜닝 체크포인트 경로 |
| `HIVE_SYSTEM_PROMPT` | (대화체 기본값) | 모델 답변 스타일 지정. 비우면 기본 대화체 프롬프트 사용 |

## 라우팅 규칙

- 복잡도 `low` + 확신도 0.5 이상 → Ollama (로컬, 무료)
- 그 외 (`medium`/`high`, 또는 확신도 0.5 미만) → Groq (클라우드, 무료 플랜)
