def bubbleSort(mylist):
    # outer loop
    for i in range(len(mylist)-1, 0, -1):
        # inner loop
        for j in range(i):
            if mylist[j] > mylist[j+1]:
                # swap the value
                temp = mylist[j]
                mylist[j] = mylist[j+1]
                mylist[j+1] = temp
    return mylist

firstlist = [5, 8, 3, 1]
print(bubbleSort(firstlist))
