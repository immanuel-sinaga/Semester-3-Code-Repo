def main():
    N = int(input())
    kata_list = [""] * N

    for i in range(N):
        kata = input()
        kata_list[i] = replaceC(kata)

    for kata in kata_list:
        print(kata)

def replaceC(kata):
    hasilKata = ""
    i = 0
    
    while i < len(kata):
        if i < len(kata) - 1 and kata[i] == 'c' and kata[i + 1] == 'h':
            hasilKata = hasilKata + 'c'
            i = i + 2
        
        elif kata[i] == 'c':
            if i + 1 < len(kata):
                huruf_lnjt = kata[i + 1]
                if huruf_lnjt in 'eiy':
                    hasilKata = hasilKata + 's'
                else:
                    hasilKata = hasilKata + 'k'
            else:
                hasilKata = hasilKata + 'k'
            i = i + 1
        
        else:
            hasilKata = hasilKata + kata[i]
            i = i + 1

    return hasilKata

main()
