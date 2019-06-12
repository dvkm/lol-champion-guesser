import sqlite3
import random

from question import Answer
from questions import questions
from database import conn, cursor


def parse_answer(question):
    while True:
        user_input = input(question + " ").lower()
        if user_input in ["yes", "1"]:
            return Answer.YES
        elif user_input in ["no", "5"]:
            return Answer.NO
        elif user_input in ["maybe", "4"]:
            return Answer.MAYBE
        elif "prob" in user_input or user_input in ["probably", "2", "prob"]:
            return Answer.PROBABLY
        elif "unk" in user_input or "idk" in user_input or user_input in ["?", "3"]:
            return Answer.UNKNOWN
        else:
            print("Invalid answer")

def answer_string(answer):
    answers = {
        Answer.YES: "yes",
        Answer.NO: "no",
        Answer.MAYBE: "maybe",
        Answer.PROBABLY: "probably",
        Answer.UNKNOWN: "unknown"
    }
    return answers[answer]

# https://docs.python.org/3/library/sqlite3.html

champions = open("champions.txt", "r").read().splitlines()

#moved to setup

conn.commit()

def get_next_training(cursor):
    cursor.execute("SELECT (`yes`+`probably`+`unknown`+`maybe`+`no`) as sum, champion, attr, (SELECT COUNT(*) FROM attributes WHERE (`yes`+`probably`+`unknown`+`maybe`+`no`) = (SELECT min((`yes`+`probably`+`unknown`+`maybe`+`no`)) FROM attributes)) as num FROM attributes WHERE sum = (SELECT min((`yes`+`probably`+`unknown`+`maybe`+`no`)) FROM attributes) ORDER BY random()")
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    row = rows[0]
    return [row[1], row[2], row[3]]
    pass

next_training = get_next_training(c)

while next_training:
    champion = next_training[0]
    attribute = next_training[1]
    left = next_training[2]
    question = questions[attribute]
    print(f"{left} questions left!")
    print(f"{champion}: ", end="")
    answer = parse_answer(question)
    c.execute('''INSERT OR IGNORE INTO attributes (champion, attr, yes, probably, `unknown`, maybe, `no`) VALUES (?, ?, 0, 0, 0, 0, 0);''', [champion, attribute])
    c.execute(f'''UPDATE attributes SET {answer_string(answer)} = {answer_string(answer)} + 1 WHERE champion = ? AND attr = ? ''', [champion, attribute])
    conn.commit()
    next_training = get_next_training(c)

# for champion in champions:
#     for question in questions:
#         print(f"Answering question for: {champion}")
#         answer = parse_answer(question["question"])
#         c.execute('''INSERT OR IGNORE INTO attributes (champion, attr, yes, probably, `unknown`, maybe, `no`) VALUES (?, ?, 0, 0, 0, 0, 0);''', [champion, question["value"]])
#         c.execute(f'''UPDATE attributes SET {answer_string(answer)} = {answer_string(answer)} + 1 WHERE champion = ? AND attr = ? ''', [champion, question["value"]])
#         conn.commit()

conn.commit()
conn.close()