"""Hive MVP v0.1 CLI 진입점.

사용법:
    python -m hive "프롬프트"
"""

import sys

from .config import load_config
from .router import route

# 목적지별 표시 이름
DEST_LABEL = {"ollama": "Ollama (로컬)", "groq": "Groq (클라우드)"}


def print_usage():
    print('사용법: python -m hive "프롬프트"')


def main():
    # 1. 프롬프트 파싱 (인자 없으면 사용법 출력 후 종료)
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        print_usage()
        sys.exit(1)

    # 2. 설정 로드 (API 키 없으면 여기서 한국어 안내 후 종료)
    cfg = load_config()

    # 3. 인텐트 분류 → 작업 종류/복잡도/확신도 출력
    #    (laya는 무거우므로 실제 사용 시점에 늦게 임포트)
    print("분류 중...")
    try:
        from .classifier import IntentClassifier
    except ModuleNotFoundError:
        print(
            "오류: laya 패키지가 설치되지 않았습니다. "
            "`pip install laya` 실행 후 다시 시도하세요.",
            file=sys.stderr,
        )
        sys.exit(1)
    classifier = IntentClassifier(model_path=cfg["laya_model_path"])
    result = classifier.classify(prompt)
    print(f"작업 종류: {result['task_type']} (확신도 {result['task_conf']:.2f})")
    print(f"복잡도: {result['complexity']} (확신도 {result['cx_conf']:.2f})")

    # 4. 라우팅 → 목적지 출력
    dest = route(result["complexity"], result["cx_conf"])
    print(f"→ 라우팅: {DEST_LABEL[dest]}")
    print()

    # 5. 목적지 어댑터로 질문 → 답변 출력
    try:
        if dest == "ollama":
            from .adapters import ollama as ollama_adapter

            answer = ollama_adapter.ask(
                prompt, model=cfg["ollama_model"], system=cfg["system_prompt"]
            )
        else:
            try:
                from .adapters import groq as groq_adapter
            except ModuleNotFoundError:
                raise RuntimeError(
                    "openai 패키지가 설치되지 않았습니다. "
                    "`pip install openai` 실행 후 다시 시도하세요."
                )
            answer = groq_adapter.ask(
                prompt,
                models=cfg["groq_models"],
                api_key=cfg["groq_api_key"],
                system=cfg["system_prompt"],
            )
    except RuntimeError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)

    print(answer)


if __name__ == "__main__":
    main()
