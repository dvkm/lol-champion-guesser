from questions import questions
from database import conn, cursor

# https://docs.python.org/3/library/sqlite3.html

cursor.execute('''CREATE TABLE IF NOT EXISTS champions(
    id int primary key,
    name text,
    UNIQUE(name)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS weights(
    attr text,
    weight int,
    UNIQUE(attr)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `attributes` (
	`champion`	text,
	`attr`	text,
	`yes`	int DEFAULT 0,
	`probably`	int DEFAULT 0,
	`unknown`	int DEFAULT 0,
	`maybe`	int DEFAULT 0,
	`no`	int DEFAULT 0,
    UNIQUE(champion, attr)
);''')

champions = open("champions.txt", "r").read().splitlines()


for attr in questions.keys():
    weight = input("Please enter the weight for " + attr + ": ")
    cursor.execute('INSERT OR REPLACE INTO weights VALUES (?, ?)', [attr, weight])


for num, champion in enumerate(champions, 1):
    cursor.execute("INSERT OR IGNORE INTO champions VALUES (?, ?)", [num, champion])

cursor.execute("""INSERT OR IGNORE INTO attributes (champion, attr) SELECT name as champion, attr FROM champions CROSS JOIN weights""")

conn.commit()

conn.close()