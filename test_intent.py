"""Hive Intent Classifier 로컬 테스트.

사용법:
  1. hive_intent_laya.zip 압축을 풀어서 이 파일과 같은 폴더에 두기
     (폴더명: hive_intent_laya)
  2. pip install laya
  3. python test_intent.py "이 보고서 3줄로 요약해줘"
"""
import sys
import json

from laya import Agent

TASK_TYPES = {
    "요약": "내용을 짧게 줄이기",
    "번역": "언어 간 변환",
    "질문답변": "사실, 정보, 방법을 묻기",
    "글쓰기": "이메일, 에세이, 창작 등 글 작성",
    "코드생성": "새 코드 작성",
    "코드분석": "코드 리뷰, 디버깅, 설명",
    "데이터분석": "표, 통계, 데이터 해석",
    "정보검색": "최신 정보나 검색이 필요한 질문",
    "계산": "수학, 수치 계산",
    "분류": "카테고리 나누기, 라벨링",
    "기타": "위에 속하지 않는 작업",
}

COMPLEXITY = {
    "low": "단순한 요청으로 짧은 답으로 해결됨",
    "medium": "문맥 이해나 중간 수준의 추론이 필요함",
    "high": "복잡한 추론, 전문 지식, 또는 긴 문서 처리가 필요함",
}

print("모델 로딩 중...")
agent = Agent("./hive_intent_laya")  # CPU. GPU 있으면 device="cuda" 추가
print("로드 완료.\n")


def classify(prompt):
    questions = {
        "task_type": {
            "type": "choice",
            "instructions": "이 요청은 어떤 작업 종류인가?",
            "criteria": TASK_TYPES,
        },
        "complexity": {
            "type": "choice",
            "instructions": "이 작업의 복잡도는 어느 정도인가?",
            "criteria": COMPLEXITY,
        },
    }
    res = agent.predict({"prompt": prompt}, questions)
    a = res["answers"]

    tt = a["task_type"]
    cx = a["complexity"]
    tt_choice = tt.get("choice", tt) if isinstance(tt, dict) else tt
    cx_choice = cx.get("choice", cx) if isinstance(cx, dict) else cx
    tt_conf = tt.get("confidence", "?") if isinstance(tt, dict) else "?"
    cx_conf = cx.get("confidence", "?") if isinstance(cx, dict) else "?"
    route = "로컬 (Ollama)" if cx_choice == "low" else "클라우드 (Gemini)"

    print(f"프롬프트: {prompt}")
    print(f"작업 종류: {tt_choice} (확신도 {tt_conf})")
    print(f"복잡도: {cx_choice} (확신도 {cx_conf})")
    print(f"→ 라우팅: {route}")
    print()
    print("전체 확률 분포:")
    print(json.dumps(a, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "이 보고서 3줄로 요약해줘"
    classify(prompt)
