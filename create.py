import json
import sqlite3
from sqlite3 import Error
import unicodedata

"""
rows = cursor.fetchall()

for row in rows:
	print(row)
"""

def replace():
	list_words = getListWords()
	i = 0
	nbFile = 0
	lenW = len(list_words)
	while (i != lenW):
		with open("index{}.json".format(str(nbFile)), "a+") as f:
			f.write("{} ".format(list_words[i]))
		if (i % 10000 == 0):
			nbFile += 1
		i += 1



def create_connection(db_file):
	""" create a database connection to a SQLite database """
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
		cursor = conn.cursor()
		cursor.execute('''CREATE TABLE IF NOT EXISTS Words
			  (word TEXT, length INT)''')
		conn.commit()
	except Error as e:
		print(e)
	finally:
		if conn:
			conn.close()


def getListWords():
	res = []
	"""
	for i in range(35):
		with open("./index/index{}.json".format(str(i)), "r") as f:
			res.append(f.readlines())
	"""
	
	return res

def insert(word, cursor):
	command = "INSERT INTO Words(word, length) VALUES('{}', {})".format(word, str(len(word)))
	cursor.execute(command)

	#print(word)
	pass

def get_list_mots(description, cursor):
	command = "SELECT word from Words WHERE length = {} AND word LIKE '{}'".format(str(len(description)), description)
	rows = cursor.execute(command).fetchall()
	return rows

def build_database():
	create_connection("list_word.db")
	conn = sqlite3.connect("list_word.db")
	cursor = conn.cursor()
	res = []
	list_words = getListWords()
	for l in list_words:
		for word in l:
			print(word[0:-1])
			insert(word, cursor)
	conn.commit()
	conn.close()
	with open("test.txt", "a+") as f:
		for w in res:
			f.write(w)

def exclude_letters(base, list_lettres):
	res = []
	for mot in base:
		found = True
		for lettre in list_lettres:
			if (lettre in mot[0]):
				found = False
		if (found):
			res.append(mot)
	print("Il nous reste {} après l'exclusion résultats".format(str(len(res))))
	return res

def include_letters(base, lettre):
	res = []
	list_lettres = lettre.split(' ')
	pos = list_lettres[1]
	lettre = list_lettres[0]
	for mot in base:
		if (lettre in mot[0]):
			res.append(mot)
	print("Il nous reste {} après l'inclusion résultats".format(str(len(res))))
	return res

def ask_question(cursor):
	print("> Décrivez votre mot sous la forme A____E:")
	mots = input()
	mots = mots.lower()
	lists_mots = get_list_mots(mots, cursor)
	continuer = True
	print("> Quelles sont les lettres que vous connaissez l'existence mais pas la position?")
	while continuer:
		print("> Indiquer les sous la forme : LETTRE POSITION (position testée). DITE 'STOP' pour sortir")
		list_lettres_inclusion = input()
		if (list_lettres_inclusion == "STOP"):
			continuer = False
		else:
			lists_mots = include_letters(lists_mots, list_lettres_inclusion)
	print("> Quelles sont les lettres à exclure?")
	list_lettres_exclusion = input()
	if (len(list_lettres_exclusion) != 0):
		lists_mots = exclude_letters(lists_mots, list_lettres_exclusion)
		print("Il y a {} résultats correspondant:".format(str(len(lists_mots))))
	for word in lists_mots:
		print(word[0])
	print(">Avez vous trouvé? (y/n)")
	reponse = input()
	if (reponse == "n"):
		ask_question(cursor)
	#print(lists_mots)

def ask_questions():
	conn = sqlite3.connect("list_word.db")
	cursor = conn.cursor()
	ask_question(cursor)
	conn.close()

def launch_sql():
	conn = sqlite3.connect("list_word.db")
	cursor = conn.cursor()
	question = input()
	command = "SELECT word from Words WHERE  word LIKE '{}'".format(question)
	rows = cursor.execute(command).fetchall()
	for row in rows:
		print(row[0])
	conn.close()


if __name__ == "__main__":
	replace()
	#build_database()
	#ask_questions()
	#launch_sql()
	#print(getListWords())