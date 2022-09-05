import numpy as np
import matplotlib.pyplot as plt
#sin & cos曲线
x = np.arange(0, 6, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)
plt.plot(x,y1,label="sin")
plt.plot(x,y2,label="cos",linestyle = "--")
plt.xlabel("x")
plt.ylabel("y")
plt.title('sin & cos')
plt.legend()   #打上标签
plt.show()
#gamma
x = np.arange(0, 1, 0.002)
y1 = pow(x,0.25)
y2 = pow(x,0.5)
y3 = pow(x,1)
y4 = pow(x,2)
y5 = pow(x,4)
plt.plot(x,y1,label="gamma=0.25")
plt.plot(x,y2,label="gamma=0.5")
plt.plot(x,y3,label="gamma=1")
plt.plot(x,y4,label="gamma=2")
plt.plot(x,y5,label="gamma=4")
plt.xlabel("x")
plt.ylabel("y")
plt.title('gamma')
plt.legend()   #打上标签
plt.show()