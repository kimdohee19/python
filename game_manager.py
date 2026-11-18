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

                if choice == "1":
                    print("\n[알림] 퀴즈 풀기 기능은 추후 구현됩니다.\n")
                elif choice == "2":
                    print("\n[알림] 퀴즈 추가 기능은 추후 구현됩니다.\n")
                elif choice == "3":
                    print("\n[알림] 퀴즈 목록 기능은 추후 구현됩니다.\n")
                elif choice == "4":
                    print("\n[알림] 점수 확인 기능은 추후 구현됩니다.\n")
                elif choice == "5":
                    print(
                        "\n프로그램을 종료합니다. 문제를 풀어주셔서 감사합니다.\n"
                    )
                    break
                else:
                    print(
                        "\n⚠️  잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.\n"
                    )
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️  강제 종료 신호가 감지되었습니다. 안전하게 종료합니다.\n")