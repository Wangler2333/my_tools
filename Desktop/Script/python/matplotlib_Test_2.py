#!/usr/bin/python

import matplotlib.pyplot as plt

y_values = []

x_values = list(range(1,1991))

#for x in x_values:
#    a = x**2
#    y_values.append(a)

y_values = [x**2 for x in x_values]

plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, edgecolors='none', s=5)

plt.title("Square Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)


plt.axis([0, 1100, 0, 1100000])
#plt.tick_params(axis='both', which = 'major', labelsize=14)

#plt.savefig('squares_plot.png',bbox_inches='tight')

plt.show()


