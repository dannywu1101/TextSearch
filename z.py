# /z.py

def Z_algorithm(s: str) -> list:
    n = len(s)
    Z = [0] * n
    L, R, K = 0, 0, 0

    for i in range(1, n):
        if i > R:
            L, R = i, i
            while R < n and s[R] == s[R - L]:
                R += 1
            Z[i] = R - L
            R -= 1
        else:
            K = i - L
            if Z[K] < R - i + 1:
                Z[i] = Z[K]
            else:
                L = i
                while R < n and s[R] == s[R - L]:
                    R += 1
                Z[i] = R - L
                R -= 1
    return Z

def find_substring(text: str, pattern: str) -> int:
    concat = pattern + "$" + text
    Z = Z_algorithm(concat)
    pattern_len = len(pattern)

    for i in range(len(Z)):
        if Z[i] == pattern_len:
            return i - pattern_len - 1  # Adjust for the concatenation
    return -1

