import matplotlib.pyplot as plt
def val(n):
	s = set()
	for i in range(n):
		s.add((i*i)%n)
	return len(s)

x = list(range(1,10001))
y = [val(i) for i in x]
plt.plot(x,y,".")
plt.xlabel("Base")
plt.ylabel("Nombre de chiffres d'unités de carrés")
plt.title("Nombre de chiffres d'unités de carrés en fonction de la base")
plt.show()