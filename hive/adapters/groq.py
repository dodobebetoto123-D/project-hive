"""Groq 어댑터 (클라우드, 무료 플랜). OpenAI 호환 API.

키 발급: https://console.groq.com/keys (무료, 카드 불필요, 키는 gsk_로 시작)
"""

from openai import OpenAI

# 폴백 대상 에러 코드 (모델 교체 시에도 재시도)
_FALLBACK_CODES = ("404", "429", "503")


def ask(prompt: str, models: str, api_key: str, system: str = "") -> str:
    """Groq 무료 플랜 모델에 프롬프트를 보내고 답변 텍스트를 반환한다.

    models: 쉼표로 구분된 모델 ID 체인 (예: "openai/gpt-oss-120b,qwen/qwen3.6-27b").
            앞에서부터 시도하고, 404/429/503이면 다음 모델로 넘어간다.
    system: 시스템 프롬프트 (대화 스타일 지정).
    """
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY 환경변수가 없습니다. "
            "console.groq.com/keys 에서 API 키를 발급받은 뒤 (무료, 카드 불필요),\n"
            "Windows PowerShell에서 아래 명령으로 설정하세요:\n"
            '  $env:GROQ_API_KEY = "..."'
        )
    model_list = [m.strip() for m in (models or "").split(",") if m.strip()]
    if not model_list:
        raise RuntimeError("GROQ_MODELS 환경변수에 모델 ID가 하나도 없습니다.")

    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
    last_error = None
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    for m in model_list:
        try:
            resp = client.chat.completions.create(
                model=m,
                messages=messages,
            )
            answer = (resp.choices[0].message.content or "").strip()
            if not answer:
                print(f"'{m}' 모델이 빈 답변을 반환했습니다. 다음 모델로 전환...")
                continue
            return answer
        except Exception as e:
            err = str(e)
            if any(code in err for code in _FALLBACK_CODES):
                print(f"'{m}' 모델 사용 불가 ({err[:80]}...). 다음 모델로 전환...")
                last_error = e
                continue
            raise RuntimeError(f"Groq API 호출에 실패했습니다: {e}")
    raise RuntimeError(f"모든 Groq 모델이 실패했습니다: {last_error}")
