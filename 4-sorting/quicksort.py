"""
quicksort.py

author: Colin Clement
date: 2017-10-23

This follows Skiena section 4.6 

"""
    
import random

def swap(lst, i, j):
    tmp = lst[i]
    lst[i] = lst[j]
    lst[j] = tmp

def sort(lst, l, h):
    if l < h:  # end case evaluate false
        p = partition(lst, l, h)
        sort(lst, l, p-1)
        sort(lst, p+1, h)

def partition(lst, l, h):
    p = h-1  # pivoting around value of last element
    firsthigh = l  # first high point, will be reported partition
    for i in range(l, h):  # compare ever val to lst[p]
        if lst[i] < lst[p]:  # i moves to the right of elements it dominates
            swap(lst, i, firsthigh)
            firsthigh += 1  # how many elements are smaller than lst[p]
    swap(lst, p, firsthigh)
    return firsthigh

def quicksort(lst):
    sortlst = list(lst)
    random.shuffle(sortlst)  # makes unlucky starting points less likely
    sort(sortlst, 0, len(lst))
    return sortlst

if __name__=="__main__":
    li = [1942, 1783, 1776, 1804, 1865, 1945, 1963, 1918, 2001, 1941]

    import matplotlib.pyplot as plt
    from datetime import datetime

    sizes = [2**i for i in range(1, 18)]
    quicktime = []
    stdtime = []
    for s in sizes:
        lst = [random.randint(0, 100000) for i in range(s)]

        st = datetime.now()
        lstsrt = quicksort(lst)
        quicktime += [(datetime.now() - st).total_seconds()]
            
        st = datetime.now()
        lstsrt = sorted(lst)
        stdtime += [(datetime.now() - st).total_seconds()]

    plt.loglog(sizes, quicktime, label='quicktime')
    plt.loglog(sizes, stdtime, label='stdsort')
    plt.legend()
    plt.show()



