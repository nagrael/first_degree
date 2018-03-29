import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


img = mpimg.imread('LENNA.jpg')
U, sigma, V = np.linalg.svd(img)
A = []
print(sigma)
for i in range(5, 2000, 10):
    reconstimg = np.matrix(U[:, :i]) * np.diag(sigma[:i]) * np.matrix(V[:i, :])
    diff = img - reconstimg
    A.append(np.linalg.norm(diff))
    #plt.imshow(diff, cmap='gray')
    #plt.savefig("Diff_"+str(i)+".jpg")
    #plt.imshow(reconstimg, cmap='gray')
    #plt.savefig("Image_" + str(i)+".jpg")

plt.plot(A)
plt.show()