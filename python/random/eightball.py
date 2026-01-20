import random

def Eight_ball():
    fortunes = [
        "Yes, definitely.",
        "Ask again later.",
        "Don't count on it.",
        "It is certain.",
        "My sources say no.",
        "Outlook not so good.",
        "Yes, in due time.",
        "You may rely on it.",
        "Very doubtful.",
        "As I see it, yes."
    ]
    return random.choice(fortunes)

def whatQuestion():
    global question
    question = input("What is your question? \n")
    if question.lower() == "exit":
        print("Goodbye!")
        return False
    else:
        print("Thinking...")
        print(Eight_ball())
        return True

whatQuestion()