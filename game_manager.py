import json
import os
from quiz import Quiz
from quiz_data import default_quizzes


class QuizGame:

    def __init__(self, state_file="state.json"):
        os.system("")
        self.state_file = state_file
        self.quizzes, self.best_score, self.has_played = self.load_state()

    def _build_default_quizzes(self):
        return [
            Quiz(q.question, list(q.choices), q.answer) for q in default_quizzes
        ]

    def _parse_quizzes(self, raw_quizzes):
        if not isinstance(raw_quizzes, list) or not raw_quizzes:
            return None

        parsed = []
        for item in raw_quizzes:
            if not isinstance(item, dict):
                return None
            question = item.get("question")
            choices = item.get("choices")
            answer = item.get("answer")

            if (
                not isinstance(question, str)
                or not question.strip()
                or not isinstance(choices, list)
                or len(choices) != 4
                or not all(isinstance(c, str) and c.strip() for c in choices)
                or not isinstance(answer, int)
                or isinstance(answer, bool)
                or not (1 <= answer <= 4)
            ):
                return None

            parsed.append(Quiz(question.strip(), [c.strip() for c in choices], answer))

        return parsed

    def load_state(self):
        default_list = self._build_default_quizzes()
        if not os.path.exists(self.state_file):
            return default_list, 0, False

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                print(
                    "\n⚠️  state.json 형식이 올바르지 않아 기본 퀴즈 데이터로 초기화합니다.\n"
                )
                return default_list, 0, False

            quizzes = self._parse_quizzes(data.get("quizzes"))
            if quizzes is None:
                print(
                    "\n⚠️  state.json의 퀴즈 데이터가 손상되어 기본 퀴즈 데이터로 복구합니다.\n"
                )
                quizzes = default_list

            raw_best = data.get("best_score", 0)
            if (
                isinstance(raw_best, int)
                and not isinstance(raw_best, bool)
                and raw_best >= 0
            ):
                best_score = raw_best
            else:
                print(
                    "\n⚠️  state.json의 최고 점수 데이터가 손상되어 0점으로 복구합니다.\n"
                )
                best_score = 0

            raw_played = data.get("has_played", False)
            has_played = bool(raw_played) or best_score > 0
            print(
                f"\n📥 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best_score}점)\n"
            )
            return quizzes, best_score, has_played

        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            print(
                "\n⚠️  state.json 파일을 읽는 중 오류가 발생해 기본 데이터로 복구합니다.\n"
            )
            return default_list, 0, False

    def save_state(self):
        payload = {
            "quizzes": [
                {"question": q.question, "choices": q.choices, "answer": q.answer}
                for q in self.quizzes
            ],
            "best_score": self.best_score,
            "has_played": self.has_played,
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except OSError:
            print("\n⚠️  state.json 저장 중 파일 입출력 오류가 발생했습니다.\n")

    def _read_non_empty_text(self, prompt, empty_message):
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print(empty_message)

    def _read_int_in_range(
        self,
        prompt,
        min_val,
        max_val,
        empty_message,
        nan_message,
        range_message,
    ):
        while True:
            raw = input(prompt).strip()
            if not raw:
                print(empty_message)
                continue
            try:
                num = int(raw)
            except ValueError:
                print(nan_message)
                continue
            if num < min_val or num > max_val:
                print(range_message)
                continue
            return num

    def play_quiz(self):
        if not self.quizzes:
            print("\n⚠️  등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.\n")
            return

        score = 0
        total_quizzes = len(self.quizzes)
        print(f"\n🚀 총 {total_quizzes}개의 퀴즈를 시작합니다!")

        for i, q in enumerate(self.quizzes, start=1):
            print("\n" + "-" * 40)
            print(f"[문제 {i} / {total_quizzes}] {q.question}")
            print("-" * 40)

            for idx, choice in enumerate(q.choices, start=1):
                print(f"{idx}. {choice}")

            ans_num = self._read_int_in_range(
                prompt="\n정답 번호 입력: ",
                min_val=1,
                max_val=4,
                empty_message="\n⚠️  빈 입력입니다. 숫자를 입력해주세요.",
                nan_message="\n⚠️  숫자 변환 실패! 1~4 사이의 숫자를 입력해주세요.",
                range_message="\n⚠️  허용 범위 밖의 숫자입니다. 1~4 사이의 숫자를 입력해주세요.",
            )

            if q.check_answer(ans_num):
                print("\n🟢 정답입니다! 👏👏")
                score += 1
            else:
                print(f"\n❌ 오답입니다! 정답은 {q.answer}번입니다.")

        self.has_played = True
        print("\n" + "=" * 40)
        print(f"🔥 퀴즈 종료! 총 {total_quizzes}문제 중 {score}문제를 맞혔습니다!")
        print("=" * 40)

        if score > self.best_score:
            self.best_score = score
            print(f"🏅 새로운 최고 점수 경신: {self.best_score}점! (축하합니다!)")
        else:
            print(f"📌 이번 점수: {score}점 (최고 점수: {self.best_score}점)")

        self.save_state()

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = self._read_non_empty_text(
            prompt="문제를 입력하세요: ",
            empty_message="\n⚠️  빈 입력입니다. 문제를 입력해주세요.\n",
        )

        choices = []
        for i in range(1, 5):
            choice = self._read_non_empty_text(
                prompt=f"선택지 {i}: ",
                empty_message=f"\n⚠️  빈 입력입니다. 선택지 {i} 내용을 입력해주세요.\n",
            )
            choices.append(choice)

        ans_num = self._read_int_in_range(
            prompt="정답 번호 (1-4): ",
            min_val=1,
            max_val=4,
            empty_message="\n⚠️  빈 입력입니다. 1-4 사이의 숫자를 입력하세요.\n",
            nan_message="\n⚠️  숫자 변환 실패! 1-4 사이의 숫자를 입력하세요.\n",
            range_message="\n⚠️  허용 범위 밖의 숫자입니다. 1-4 사이의 숫자를 입력하세요.\n",
        )

        self.quizzes.append(Quiz(question, choices, ans_num))
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!\n")

    def list_quizzes(self):
        if not self.quizzes:
            print("\n⚠️  등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.\n")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for idx, q in enumerate(self.quizzes, start=1):
            print(f"[{idx}] {q.question}")
        print("-" * 40 + "\n")

    def show_best_score(self):
        if not self.has_played and self.best_score == 0:
            print("\n⚠️  아직 퀴즈를 풀지 않았습니다. 1번 메뉴에서 퀴즈를 풀어보세요!\n")
            return

        print("\n" + "=" * 40)
        print(f"🏆 현재 최고 점수: {self.best_score}점")
        print("=" * 40 + "\n")

    def run_menu(self):
        try:
            while True:
                print("\n" + "=" * 40)
                print(" 😊 개발 & 프로그래밍 퀴즈 😊 ")
                print("=" * 40)
                print(" 1. 퀴즈 풀기")
                print(" 2. 퀴즈 추가")
                print(" 3. 퀴즈 목록")
                print(" 4. 점수 확인")
                print(" 5. 종료")
                print("=" * 40)

                menu_num = self._read_int_in_range(
                    prompt="선택: ",
                    min_val=1,
                    max_val=5,
                    empty_message="\n⚠️  빈 입력입니다. 1-5 사이의 숫자를 입력하세요.\n",
                    nan_message="\n⚠️  숫자 변환 실패! 1-5 사이의 숫자를 입력하세요.\n",
                    range_message="\n⚠️  허용 범위 밖의 숫자입니다. 1-5 사이의 숫자를 입력하세요.\n",
                )

                if menu_num == 1:
                    self.play_quiz()
                elif menu_num == 2:
                    self.add_quiz()
                elif menu_num == 3:
                    self.list_quizzes()
                elif menu_num == 4:
                    self.show_best_score()
                elif menu_num == 5:
                    self.save_state()
                    print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다.\n")
                    break
        except (KeyboardInterrupt, EOFError):
            self.save_state()
            print(
                "\n\n⚠️  입력 중단 신호가 감지되었습니다. 안전하게 종료합니다.\n"
            )


if __name__ == "__main__":
    game = QuizGame()
    game.run_menu()