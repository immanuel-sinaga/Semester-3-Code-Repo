def sorting(inputArray):
    n = len(inputArray)

    for i in range(n):
        indexMinimal = i
        
        for j in range(i + 1, n):
            if inputArray[j] < inputArray[indexMinimal]:
                indexMinimal = j

        temp = inputArray[i]
        inputArray[i] = inputArray[indexMinimal]
        inputArray[indexMinimal] = temp


def main():
    teamJumlah = int(input())

    ratingSkil = list(map(int, input().split()))
    
    sorting(ratingSkil)
    
    maxDariTeamTerlemah = ratingSkil[teamJumlah]

    print(maxDariTeamTerlemah)

main()