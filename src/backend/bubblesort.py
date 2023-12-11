import radio

def bubble_sort(radio):
    for i in range(0, len(radio.queue) - 1):
        for j in range(0, len(radio.queue) - i - 1):
            if (radio.queue[j][radio.characteristic] > radio.queue[j + 1][radio.characteristic]):
                (radio.queue[j], radio.queue[j + 1]) = (radio.queue[j + 1], radio.queue[j])  

# testing
'''
data = [[1, 2, 3], [3, 4, 5], [6, 7, 8], [2, 3, 4], [-2, -1, 4], [5, 2, -1], [-7, 0, 3]]
print("Unsorted Array")
print(data)
 
size = len(data)
 
bubble_sort(data, 2)
 
print('Sorted Array in Ascending Order:')
print(data)
'''
