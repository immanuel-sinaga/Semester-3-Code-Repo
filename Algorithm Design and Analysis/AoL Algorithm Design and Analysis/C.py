def doubleChunksMaksimum(N, A):
    A = [0] + A
    maks = 0
    
    for i in range(1, N):
        currSum = A[i] + A[i + 1]
        possible_chunks = 0
        used = [False] * (N + 1)
        
        for j in range(1, N):
            if (not used[j] and 
                not used[j + 1] and 
                j + 1 <= N):
                if A[j] + A[j + 1] == currSum:
                    possible_chunks += 1
                    used[j] = True
                    used[j + 1] = True
        
        maks = max(maks, possible_chunks)
    
    return maks

N = int(input())
A = list(map(int, input().split()))

print(doubleChunksMaksimum(N, A))