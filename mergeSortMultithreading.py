import threading

arr = []
THREAD_MAX = 5

# Function
# Taget:
#   merge two ordered partitions in an array.
#   l -> m and m + 1 -> r
# Input:
#   arr: array
#   l: index of left most element.
#   m: index of median element.
#   r: index of right most element.
# Output: void
def merge(l, m, r):

    global arr

    n1 = m - l + 1
    n2 = r - m
 
    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)
 
    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]
 
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
 
    # Merge the temp arrays back into arr[l..r]
    i = 0     # Initial index of first subarray
    j = 0     # Initial index of second subarray
    k = l     # Initial index of merged subarray

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
 
    # Copy the remaining elements of L[]
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
 
    # Copy the remaining elements of R[]
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
 
 
# Function
# Target:
#   Calculate middle point
#   Call recursive
# Input:
#   arr: array
#   l: index of left most element.
#   r: index of right most element.
# Output: void
def mergeSort(lock, l, r):
    
    global arr


    if l < r:
        
        # Calculate middle point
        # Same as (l+r)//2, but avoids overflow for large l and h
        m = l + (r - l)//2
 
        # Call recursive for first half
        mergeSort(lock, l, m)

        # Call recursive for second half
        mergeSort(lock, m+1, r)

        # Merge two halves
        lock.acquire()
        merge(l, m, r)
        lock.release()


# Function
# Target: To merge result of threads
# Input:
#   start: schedule array
#   end: schedule array
#   l: number of left most thread
#   r: number of right most thread
def mergeThread(start, end, l, r):

    global THREAD_MAX

    if l < r:
        
        m = (l + r) // 2

        mergeThread(start, end, l, m)

        mergeThread(start, end, m + 1, r)

        merge(start[l], end[m], end[r])






def main():

    lock = threading.Lock()

    global arr
        # Driver code to test above
    arr = [12, 11, 13, 5, 6, 7, 5, 8, 9, 10, 23, 27, 98, 65]
    n = len(arr)

    # i'th Thread order array from start[i] -> end[i]
    start = []
    end = []

    # For contain thread
    threadList = []

    remainder = n % THREAD_MAX
    work = n // THREAD_MAX

    # Initial value
    start.append(0)
    if remainder == 0:
        end.append(work - 1)
    else:
        end.append(work)

    # Calculate start and end of each thread
    # For example:
    #   15 number 4 thread -> 4, 4, 4, 3
    #   18 number 5 thread -> 4, 4, 4, 3, 3
    for i in range(THREAD_MAX - 1):
        start.append(end[i] + 1)
        if i < remainder - 1:
            end.append(end[i] + work + 1)
        else:
            end.append(end[i] + work)

    print("Given array is")
    for i in range(n):
        print("%d" % arr[i],end=" ")
    print("")

    for i in range(THREAD_MAX):
        print("{} {}".format(start[i], end[i]))

    for i in range(THREAD_MAX):
        name = "Thread {}".format(i)
        t = threading.Thread(target=mergeSort, args=(lock, start[i] , end[i]), name=name)
        threadList.append(t)

    for thread in threadList:
        thread.start()

    for thread in threadList:
        thread.join()

    mergeThread(start, end, 0, THREAD_MAX - 1)

    print("\n\nSorted array is")
    for i in range(n):
        print("%d" % arr[i],end=" ")
    
if __name__ == "__main__":
    main()
