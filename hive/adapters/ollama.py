"""Ollama 로컬 어댑터 (표준 라이브러리 urllib만 사용)."""

import json
import urllib.error
import urllib.request

# Ollama 기본 API 주소
OLLAMA_URL = "http://localhost:11434/api/generate"


def ask(prompt: str, model: str, system: str = "") -> str:
    """Ollama에 프롬프트를 보내고 답변 텍스트를 반환한다."""
    payload = {"model": model, "prompt": prompt, "stream": False}
    if system:
        payload["system"] = system
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=body, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise RuntimeError(
            "Ollama에 연결할 수 없습니다. "
            "Ollama가 설치되어 있고 실행 중인지 확인하세요 "
            "(https://ollama.com 에서 설치 후 `ollama serve` 실행)."
        ) from e

    answer = data.get("response", "")
    if not answer:
        raise RuntimeError("Ollama가 빈 답변을 반환했습니다.")
    return answer
