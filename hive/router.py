"""라우터: 복잡도 + 확신도로 목적지를 결정한다."""


def route(complexity: str, cx_conf: float) -> str:
    """목적지를 반환. "ollama" 또는 "groq".

    - 확신도가 0.5 미만이면 판단이 애매하므로 안전한 쪽(Groq 클라우드)으로 보낸다.
    - low → Ollama (로컬, 무료), medium/high → Groq (클라우드, 무료 플랜).
    """
    if cx_conf < 0.5:
        return "groq"
    if complexity == "low":
        return "ollama"
    return "groq"
