from enum import Enum
from database import conn, cursor
from questions import questions



class Answer(Enum):
    YES = 1
    PROBABLY = 2 # Maybe not
    UNKNOWN = 3
    MAYBE = 4 # Probably not
    NO = 5


def calculate(champions, attr, question, answer):
    cursor.execute(f"""SELECT weight FROM weights WHERE attr = "{attr}" """)
    weight = cursor.fetchone()[0]
    cursor.execute("SELECT champion, `yes`, `probably`, `unknown`, `maybe`, `no`, (`yes` + `probably` + `unknown` + `maybe` + `no`) as total FROM attributes WHERE attr = ?", [attr])
    rows = cursor.fetchall()
    for row in rows:
        champion, yes, prob, unknown, maybe, no, total = row
        if champion not in champions:
            champions[champion] = 50

        distribution = [0.5, 0.2, 0.05]

        # Something like z distribution but I failed probability :(
        
        minus_two = row[max(1, answer.value - 2)]* distribution[2]
        minus_one = row[max(1, answer.value - 1)]* distribution[1]
        middle = row[answer.value]               * distribution[0]
        plus_two = row[min(1, answer.value + 2)] * distribution[1]
        plus_one = row[min(1, answer.value + 1)] * distribution[2]
        score = sum([minus_one, minus_two, middle, plus_one, plus_two])/total * weight
        champions[champion] += score

def sort_results(champions):
    return sorted(champions.items(), key=lambda x: x[1])

def print_result(champions):
    champions_sorted = sort_results(champions)
    for champion, probability in champions_sorted:
        print(champion + ": " + str(probability))

def print_max(chapmions):
    current_max = None
    current_champion = None
    for champion, probability in champions.items():
        if current_max is None or probability > current_max:
            current_max = probability
            current_champion = champion
    print("You're probably thinking about " + current_champion)

def parse_answer(question):
    while True:
        user_input = input(question).lower()
        if user_input == "yes":
            return Answer.YES
        elif user_input == "no":
            return Answer.NO
        elif user_input == "maybe":
            return Answer.MAYBE
        elif "prob" in user_input:
            return Answer.PROBABLY
        elif "unk" in user_input or "idk" in user_input:
            return Answer.UNKNOWN
        else:
            print("Invalid answer")
        

if __name__ == "__main__":
    # conn = sqlite3.connect('data.db')
    champions = {}

    c = conn.cursor()
    answers = []
    for attribute, question in questions.items():
        answer = parse_answer(question)

        calculate(champions, attribute, question, answer)
        
    print_result(champions)
    print_max(champions)