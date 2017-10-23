"""
quicksort.py

author: Colin Clement
date: 2017-10-23

This follows Skiena section 4.6 

Skiena has a nice C implementation which does almost all in-place 
operations. I think I'll not bother trying to emulate that because in
python it feels torturous
"""



if __name__=="__main__":
    li = [1942, 1783, 1776, 1804, 1865, 1945, 1963, 1918, 2001, 1941]

    #import random
    #import matplotlib.pyplot as plt
    #from datetime import datetime

    #sizes = [2**i for i in range(1, 18)]
    #mergetime = []
    #stdtime = []
    #for s in sizes:
    #    lst = [random.randint(0, 100000) for i in range(s)]

    #    st = datetime.now()
    #    lstsrt = mergesort(lst)
    #    mergetime += [(datetime.now() - st).total_seconds()]
    #        
    #    st = datetime.now()
    #    lstsrt = sorted(lst)
    #    stdtime += [(datetime.now() - st).total_seconds()]

    #plt.loglog(sizes, mergetime, label='mergetime')
    #plt.loglog(sizes, stdtime, label='stdsort')
    #plt.legend()
    #plt.show()



