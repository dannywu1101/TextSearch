# /lcs.py

def find_lcs(text1, text2):
    # Clean the texts by removing spaces
    clean_text1 = ''.join(text1.split())
    clean_text2 = ''.join(text2.split())
    
    n1 = len(clean_text1)
    n2 = len(clean_text2)

    # Create a matrix of size (n1+1) x (n2+1) initialized to 0
    M = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    
    # Variables to keep track of the longest common substring
    max_length = 0
    substrings_max = set()

    # Loop through both cleaned texts
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            if clean_text1[i - 1] == clean_text2[j - 1]:
                M[i][j] = M[i - 1][j - 1] + 1

                # If we find a longer common substring, reset the set and update max_length
                if M[i][j] > max_length:
                    max_length = M[i][j]
                    substrings_max = {clean_text1[i - max_length:i]}
                elif M[i][j] == max_length:
                    # If the length matches the current max, add the substring
                    substrings_max.add(clean_text1[i - max_length:i])
            else:
                M[i][j] = 0

    # Map the longest substrings back to the original texts (with spaces)
    def map_to_original(clean_substrings, original_text):
        mapped_substrings = set()
        for clean_substring in clean_substrings:
            index_in_clean = 0
            mapped_substring = ""
            for char in original_text:
                if char != " ":
                    if index_in_clean < len(clean_substring) and char == clean_substring[index_in_clean]:
                        mapped_substring += char
                        index_in_clean += 1
                    if index_in_clean == len(clean_substring):
                        break
            mapped_substrings.add(mapped_substring)
        return mapped_substrings

    # Map LCS results back to both original texts
    substrings_in_text1 = map_to_original(substrings_max, text1)
    substrings_in_text2 = map_to_original(substrings_max, text2)

    return list(substrings_in_text1 & substrings_in_text2)  # Return common substrings
