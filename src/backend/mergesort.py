def mergeSort(arr, charac):
    if len(arr) > 1:
        mid = len(arr) // 2
        leftArr = arr[:mid]
        rightArr = arr[mid:]

        # Recursively sort the two halves
        mergeSort(leftArr, charac)
        mergeSort(rightArr, charac)
        
        merge(arr, leftArr, rightArr, charac)

def merge(arr, left, right, charac):
    # Merge the sorted halves
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i][charac] < right[j][charac]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        # Check if any elements are left
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
