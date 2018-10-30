from PIL import Image
from math import pi, log, exp
import numpy as np
import sys
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print()
def process(filename, r):
    img = Image.open(filename)
    img.load()
    dx, dy = np.meshgrid(np.arange(-r, +r+1, 1.), np.arange(-r, +r+1, 1.0))
    sigma = 0.38*r
    gauss_dist = np.exp( -(dx*dx+dy*dy)/(2*sigma**2) ) / (2*pi*sigma**2)
    coeff = gauss_dist / np.sum(gauss_dist)
    w = 3000
    h = 3667
    A = np.array(img.getdata())
    A = A.reshape(w,h)
    B = np.zeros((w,h))
    full = w*h
    percent = 0
    for i in range(r,w-r-1):
        for j in range(r,h-r-1):
            for k in range(-r,r+1):
                for m in range(-r,r+1):
                    B[i,j] += coeff[k+r,m+r] * A[i+k,j+m]
            percent +=1
            printProgressBar(percent,full,prefix = 'Progress:', suffix = 'Complete',length = 50)
        

    newimg = Image.fromarray(B)
    newimg.show()
    newimg.save(filename+'.gaussblurred.png')



if __name__=='__main__':
    # Запускать с командной строки с аргументом <имя файла>, например: python gauss.py darwin.png
    if len(sys.argv) > 1:
        process(sys.argv[1], 3)
    else:
        print("Must give filename.\n")