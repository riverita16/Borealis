def bubbleSort(array, charac):
    for i in range(0, len(array) - 1):
        for j in range(0, len(array) - i - 1):
            if (array[j][charac] > array[j + 1][charac]):
                (array[j], array[j + 1]) = (array[j + 1], array[j])  

# testing
data = [[1, 2, 3], [3, 4, 5], [6, 7, 8], [2, 3, 4], [-2, -1, 4], [5, 2, -1], [-7, 0, 3]]
print("Unsorted Array")
print(data)
 
size = len(data)
 
bubbleSort(data, 2)
 
print('Sorted Array in Ascending Order:')
print(data)
