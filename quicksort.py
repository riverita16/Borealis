def partition(array, low, high, charac):
 
    pivot = array[low][charac]
 
    up = low
    down = high

    while (up < down):
    
        for i in range (up, high):
            if (array[up][charac] > pivot):
                break
            up = up + 1

        for i in range (high, low, -1):
            if (array[down][charac] < pivot):
                break
            down = down - 1

        if (up < down):
            (array[up], array[down]) = (array[down], array[up])
    
    (array[low], array[down]) = (array[down], array[low])
    return down;


 
def quickSort(array, low, high, charac):
    if low < high:
 
        pivot = partition(array, low, high, charac)
 
        # call quick sort on the left of pivot
        quickSort(array, low, pivot - 1, charac)
 
        # call quick sort on the right of pivot
        quickSort(array, pivot + 1, high, charac)
 
 
data = [[1, 2, 3], [3, 4, 5], [6, 7, 8], [2, 3, 4], [-2, -1, 4], [5, 2, -1], [-7, 0, 3]]
print("Unsorted Array")
print(data)
 
size = len(data)
 
quickSort(data, 0, size - 1, 1)
 
print('Sorted Array in Ascending Order:')
print(data)