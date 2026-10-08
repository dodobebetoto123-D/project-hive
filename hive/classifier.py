"""인텐트 분류기: 파인튜닝된 Laya 모델로 작업 종류 + 복잡도를 분류한다."""

from laya import Agent

# 학습 때 쓴 것과 동일한 라벨 정의 (바꾸면 분류가 깨짐)
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


class IntentClassifier:
    """Laya 인텐트 분류기 래퍼."""

    def __init__(self, model_path="./hive_intent_laya"):
        # model_path: 파인튜닝된 체크포인트 폴더 경로 (CPU 추론)
        self._agent = Agent(model_path)

    def classify(self, prompt):
        """프롬프트를 분류해 작업 종류/복잡도/확신도를 dict로 반환."""
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
        res = self._agent.predict({"prompt": prompt}, questions)
        a = res["answers"]

        tt = a["task_type"]
        cx = a["complexity"]
        task_type = tt.get("choice", tt) if isinstance(tt, dict) else str(tt)
        complexity = cx.get("choice", cx) if isinstance(cx, dict) else str(cx)
        task_conf = float(tt.get("confidence", 0.0)) if isinstance(tt, dict) else 0.0
        cx_conf = float(cx.get("confidence", 0.0)) if isinstance(cx, dict) else 0.0

        return {
            "task_type": task_type,
            "task_conf": task_conf,
            "complexity": complexity,
            "cx_conf": cx_conf,
        }
