# /lcs.py

def find_lcs(text1, text2):
    n1 = len(text1)
    n2 = len(text2)

    # Create a matrix of size (n1+1) x (n2+1) initialized to 0
    M = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    
    # Variables to keep track of the longest common substring
    max_length = 0
    substrings_max = []

    # Loop through both texts
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            if text1[i - 1] == text2[j - 1]:
                M[i][j] = M[i - 1][j - 1] + 1

                # If we find a longer common substring
                if M[i][j] > max_length:
                    max_length = M[i][j]
                    substrings_max = [text1[i - max_length:i]]
                elif M[i][j] == max_length:
                    # If the length matches the current max, append the substring
                    substrings_max.append(text1[i - max_length:i])
            else:
                M[i][j] = 0

    return substrings_max

