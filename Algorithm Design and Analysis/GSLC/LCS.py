def longestCommonSubsequence(text1, text2):

    dp = [[0] * (len(text2) + 1) for _ in range(len(text1) + 1)] #Buat array 2D atau tabel untuk menyimpan data hasil
    
    for i in range(1, len(text1) + 1): #Outer loop untuk text 1
        for j in range(1, len(text2) + 1): #Inner loop untuk text 2
            if text1[i - 1] == text2[j - 1]: #Mengecek per char
                dp[i][j] = dp[i - 1][j - 1] + 1 #Jika sama ambil nilai dari 1 baris dan 1 colom sebelumnya, tambahin satu dan masukan ke alamat sekarang
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) #Jika beda maka akan di ambil nilai terbesar 
                                                            #antara 1 colom sebelumnya atau 1 baris sebelumnya 
                                                            #lalu dimasukan ke alamat sekarang (Bottom Up)

    return dp[len(text1)][len(text2)] #Me-return nilai palinng bawah kanan (total) di tabel/array 2D

text1 = "cat"
text2 = "crabt"

# c, a, dan t = 3

print(longestCommonSubsequence(text1, text2))