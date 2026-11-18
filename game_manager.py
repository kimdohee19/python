import os
from quiz import Quiz
from quiz_data import default_quizzes


class QuizGame:

    def __init__(self):
        self.quizzes = default_quizzes
        self.best_score = 0
        self.state_file = "state.json"

    def run_menu(self):
        try:
            while True:
                print("\n" + "=" * 40)
                print("     😊 개발 & 프로그래밍 퀴즈 😊")
                print("=" * 40)
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록")
                print("4. 점수 확인")
                print("5. 종료")
                print("=" * 40)

                choice = input("선택: ").strip()

                if not choice:
                    print(
                        "\n⚠️  빈 입력입니다. 1-5 사이의 숫자를 입력하세요.\n"
                    )
                    continue

                try:
                    menu_num = int(choice)
                except ValueError:
                    print("\n⚠️  숫자 변환 실패! 숫자로 입력해주세요.\n")
                    continue

                if menu_num == 1:
                    self.play_quiz()
                elif menu_num == 2:
                    print("\n[알림] 퀴즈 추가 기능은 추후 구현됩니다.\n")
                elif menu_num == 3:
                    print("\n[알림] 퀴즈 목록 기능은 추후 구현됩니다.\n")
                elif menu_num == 4:
                    print("\n[알림] 점수 확인 기능은 추후 구현됩니다.\n")
                elif menu_num == 5:
                    print(
                        "\n프로그램을 종료합니다. 문제를 풀어주셔서 감사합니다.\n"
                    )
                    break
                else:
                    print(
                        "\n⚠️  허용 범위 밖의 숫자입니다. 1-5 사이의 숫자를 입력하세요.\n"
                    )
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️  강제 종료 신호가 감지되었습니다. 안전하게 종료합니다.\n")

    def play_quiz(self):
        if not self.quizzes:
            print(
                "\n⚠️  등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.\n"
            )
            return

        score = 0
        total_quizzes = len(self.quizzes)

        print(f"\n🚀 총 {total_quizzes}개의 퀴즈를 시작합니다!")

        for i, q in enumerate(self.quizzes, start=1):
            while True:
                print("\n" + "-" * 40)
                print(f"[문제 {i} / {total_quizzes}] {q.question}")
                print("-" * 40)

                for idx, choice in enumerate(q.choices, start=1):
                    print(f"{idx}. {choice}")

                # 괄호 (1-4)를 제거한 깔끔한 입력창
                user_input = input("\n정답 번호 입력: ").strip()

                if not user_input:
                    print("\n⚠️  빈 입력입니다. 숫자를 입력해주세요.")
                    continue

                try:
                    ans_num = int(user_input)
                except ValueError:
                    print(
                        "\n⚠️  숫자 변환 실패! 1~4 사이의 숫자를 입력해주세요."
                    )
                    continue

                if ans_num < 1 or ans_num > 4:
                    print(
                        "\n⚠️  허용 범위 밖의 숫자입니다. 1~4 사이의 숫자를 입력해주세요."
                    )
                    continue

                if q.check_answer(ans_num):
                    print("\n🟢 정답입니다! 👏👏")
                    score += 1
                else:
                    print(f"\n❌ 오답입니다! 정답은 {q.answer}번입니다.")

                break

        print("\n" + "=" * 40)
        print(f"🔥 퀴즈 종료! 총 {total_quizzes}문제 중 {score}문제를 맞혔습니다!")
        print("=" * 40)

        if score > self.best_score:
            self.best_score = score
            print(f"🏅 새로운 최고 점수 경신: {self.best_score}점! (축하합니다!)")
        else:
            print(f"📌 이번 점수: {score}점 (최고 점수: {self.best_score}점)")