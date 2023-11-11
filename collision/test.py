import matplotlib.pyplot as plt

figure, axes = plt.subplots()
plek = 490

axes.set_aspect(1)
plt.plot((300, 700, 200, 300), (500, 400, 200, 500), color="black")
plt.plot(300, plek, 'r.')

plt.xlim([0, 1000])
plt.ylim([0, 1000])
plt.show()
