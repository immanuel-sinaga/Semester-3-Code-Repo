def optimal_bst(keys, freq, n):
    dp = [[0 for _ in range(n)] for _ in range(n)] #Array 2D atau tabel sebesar n
    
    for i in range(n): #Inisialisasi untuk subarray ukuran 1 atau yang senilai seperti freq nya sendiri
        dp[i][i] = freq[i]
    
    for l in range(2, n+1): #Outer loop untuk jenis-jenis ukuran subarray seperti ukuran (2, 3, 4)
        for i in range(n - l + 1): #Inner loop untuk kombinasi subarray seperti (10,20)-(20,30)-(30,40)
            j = i + l - 1
            dp[i][j] = float('inf')
            
            freq_sum = sum(freq[i:j+1]) #Menghitung sum dari ukuran anggota-anggota subarray
            
            for r in range(i, j+1): #Mengetes berbagai kombinasi root dengan berbagai kombinasi subtree
                left_cost = dp[i][r-1] if r > i else 0
                right_cost = dp[r+1][j] if r < j else 0
                total_cost = left_cost + right_cost + freq_sum
                
                dp[i][j] = min(dp[i][j], total_cost) #Memilih kombinasi tree yang paling murah
    
    return dp[0][n-1] #Mengembalikan data paling kanan atas untuk biaya paling murah semua anggota keys

keys = [10, 20, 30, 40]
freq = [4, 2, 6, 3]
n = len(keys)

print(optimal_bst(keys, freq, n))