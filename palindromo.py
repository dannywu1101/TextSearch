# /palindromo.py

def preprocess(s: str) -> str:
    if not s:
        return "^$"
    ret = "^"
    for char in s:
        ret += f"#{char}"
    ret += "#$"
    return ret

def longest_palindrome(s: str) -> str:
    if not s:
        return ""  # Return empty string if the input is empty

    # Clean the string by removing spaces
    clean_s = ''.join(s.split())

    # Preprocess the string (without spaces)
    T = preprocess(clean_s)
    n = len(T)
    P = [0] * n  # Array to store the length of the palindrome radius at each center
    C, R = 0, 0  # Current center and right edge of the palindrome

    # Iterate over each character in the preprocessed string
    for i in range(1, n - 1):
        i_mirror = 2 * C - i  # Mirror of the current position

        if R > i:
            P[i] = min(R - i, P[i_mirror])

        # Expand around the center
        while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
            P[i] += 1

        # Update the center and right edge if the palindrome expands beyond R
        if i + P[i] > R:
            C = i
            R = i + P[i]

    # Find the maximum length palindrome
    max_len = max(P)
    center_index = P.index(max_len)

    # Calculate the start position in the original clean string (without spaces)
    start = (center_index - max_len) // 2
    longest_pal_clean = clean_s[start:start + max_len]

    # Map the longest palindrome back to the original string (with spaces)
    index_in_original = 0
    longest_pal_original = ""
    for char in s:
        if char != " ":
            if index_in_original < len(longest_pal_clean) and char == longest_pal_clean[index_in_original]:
                longest_pal_original += char
                index_in_original += 1
            if index_in_original == len(longest_pal_clean):
                break

    return longest_pal_original
