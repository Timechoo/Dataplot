import matplotlib.pyplot as plt # plt is a module

input_values = list(range(1,101))
squares = [x**2 for x in range(1,101)]

plt.plot(input_values,squares,linewidth=5)
plt.title('Square Numbers',fontsize=24)
plt.xlabel('Value',fontsize=14)
plt.ylabel('square of value',fontsize=14)
plt.tick_params(axis='both',labelsize=14)

plt.show()