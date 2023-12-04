# merge 2 subarrays from arr
def mergeSort(arr, charac):

    # Split the array into two halves
    mid = len(arr) // 2
    leftArr = arr[:mid]
    rightArr = arr[mid:]

    # Recursively sort both halves
    leftArr = mergeSort(leftArr, charac)
    rightArr = mergeSort(rightArr, charac)

    # Merge the sorted halves
    return merge(leftArr, rightArr, charac)

def merge(left, right, charac):
    result = []
    i = j = 0

    # Compare elements from the left and right halves and merge them
    while i < len(left) and j < len(right):
        if left[i][charac] < right[j][charac]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append the remaining elements from both halves
    result.extend(left[i:])
    result.extend(right[j:])

    return result