#散点图
import matplotlib.pyplot as plt

x = range(0,21)
y = [y**2 for y in range(0,21)]

plt.scatter(x,y,s=150)
#title and tags
plt.title('Square Numbers',fontsize=24)
plt.xlabel('Value',fontsize=14)
plt.ylabel('Square pf Value',fontsize=14)

#刻度标记
plt.tick_params(axis='both',which='major',labelsize=14)

plt.show()