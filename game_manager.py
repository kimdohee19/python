import os
from quiz import Quiz
from quiz_data import default_quizzes


class QuizGame:

    def __init__(self):
        os.system("")
        self.quizzes = [
            Quiz(q.question, list(q.choices), q.answer) for q in default_quizzes
        ]
        self.best_score = 0

    def play_quiz(self):
        print("\n[알림] 퀴즈 풀기 기능은 추후 구현됩니다.\n")

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

                choice = input("선택: ").strip()

                if not choice:
                    print("\n⚠️  빈 입력입니다. 1-5 사이의 숫자를 입력하세요.\n")
                    continue

                try:
                    menu_num = int(choice)
                except ValueError:
                    print("\n⚠️  숫자 변환 실패! 1-5 사이의 숫자를 입력하세요.\n")
                    continue

                if menu_num < 1 or menu_num > 5:
                    print(
                        "\n⚠️  허용 범위 밖의 숫자입니다. 1-5 사이의 숫자를 입력하세요.\n"
                    )
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
                    print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다.\n")
                    break
        except (KeyboardInterrupt, EOFError):
            print(
                "\n\n⚠️  입력 중단 신호가 감지되었습니다. 안전하게 종료합니다.\n"
            )


if __name__ == "__main__":
    game = QuizGame()
    game.run_menu()