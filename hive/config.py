"""환경변수 설정 읽기."""

import os
import sys


def load_config():
    """환경변수에서 설정을 읽어 dict로 반환.

    GROQ_API_KEY가 없으면 한국어 안내를 출력하고 종료한다.
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        print(
            "GROQ_API_KEY 환경변수가 설정되지 않았습니다.\n"
            "console.groq.com/keys 에서 API 키를 발급받은 뒤 (무료, 카드 불필요),\n"
            "Windows PowerShell에서 아래 명령으로 설정하세요:\n"
            '  $env:GROQ_API_KEY = "..."',
            file=sys.stderr,
        )
        sys.exit(1)
    return {
        "groq_api_key": api_key,
        "ollama_model": os.environ.get("OLLAMA_MODEL", "qwen2.5:3b"),
        "groq_models": os.environ.get(
            "GROQ_MODELS",
            "openai/gpt-oss-120b,qwen/qwen3.6-27b",
        ),
        "laya_model_path": os.environ.get("LAYA_MODEL_PATH", "./hive_intent_laya"),
        "system_prompt": os.environ.get(
            "HIVE_SYSTEM_PROMPT",
            "너는 친근한 대화 상대야. 자연스러운 대화체로 답해. "
            "마크다운 헤더(##), 표, 과도한 글머리 기호는 쓰지 마. "
            "정말 필요할 때만 최소한으로 써. 길게 늘어놓지 말고 핵심만 간결하게.",
        ),
    }
