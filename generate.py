# A script to generate properly formatted, random grade data.

import numpy as np
import random

anum = int(input("# of assignments: "))
snum = int(input("# of students: "))

f = open("output.csv", "w")
f.write("Name,ID,")

names = ["Benjamin Columbia", "Celestine Vancamp", "Shea Michaelson", "Gail Schutt", "Natasha Dambrosio", "Liana Mccaslin", "Chantelle Doshier", "Aretha Sharples", "Lavone Pundt", "Vernie Sutter", "Tawnya Fetter", "Loreen Houle", "Faith Martello", "Thaddeus Pasley", "Virginia Perugini", "Heidi Bice", "Tammie Araki"]

titles = ["Homework", "Test", "Lab", "IDK"]

for a in range(anum-1):
	f.write(random.choice(titles) + str(a) + ",")

f.write(random.choice(titles) + str(anum-1) + "\n")

for n in range(snum):
	f.write(str(random.choice(names)) + ",")
	f.write(str(n) + ",")
	rand = np.random.normal(80, 20, anum)
	for r in range(anum-1):
		f.write(str(int(rand[r])) + ",")
	f.write(str(int(rand[-1])) + "\n")

f.close()