# merge 2 subarrays from arr
def mergeSort(arr):
    if len(arr) <= 1:
        return arr

    # Split the array into two halves
    mid = len(arr) // 2
    leftArr = arr[:mid]
    rightArr = arr[mid:]

    # Recursively sort both halves
    leftArr = mergeSort(leftArr)
    rightArr = mergeSort(rightArr)

    # Merge the sorted halves
    return merge(leftArr, rightArr)

def merge(left, right):
    result = []
    i = j = 0

    # Compare elements from the left and right halves and merge them
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append the remaining elements from both halves
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# makes an array containing the deviation from list of songs and the user's original request
def sort(ogVal, valArr, numVals):
    
    arr = [0.0] * numVals
    
    for i in range(numVals):
        arr[i] = abs(ogVal - valArr[i])

    return mergeSort(arr)