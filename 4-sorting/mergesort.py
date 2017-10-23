"""
mergesort.py

author: Colin Clement
date: 2017-10-23

This follows Skiena section 4.5, implementing the heap sort

"""


class MergeSort(object):
    def __init__(self, items):
        pass

    def sort(self, lst, low, high):
        if low < high:
            mid = (low+high)//2
            self.sort(lst, low, mid)
            self.sort(lst, mid+1, high)
            self.merge(lst, low, mid, high)

    def merge(lst, low, mid, high):
        buf1 = list(lst)
        buf1 = list(lst)

        i = low
        while not (buf1 or buf2):  # keep going if any are left
            if buf1[0] <= buf2[0]:
                lst[i+1] = buf1.pop(0)
            else:
                lst[i+1] = buf2.pop(0)
            i += 1
    

if __name__=="__main__":
    li = [1942, 1783, 1776, 1804, 1865, 1945, 1963, 1918, 2001, 1941]

    #import random
    #import matplotlib.pyplot as plt
    #from datetime import datetime

    #sizes = [2**i for i in range(1, 18)]
    #heaptime = []
    #fastheaptime = []
    #stdtime = []
    #for s in sizes:
    #    s = datetime.now()
    #    lstsrt = sorted(lst)
    #    stdtime += [(datetime.now() - s).total_seconds()]

    #plt.loglog(sizes, stdtime, label='stdsort')
    #plt.legend()
    #plt.show()



