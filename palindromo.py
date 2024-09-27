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
    T = preprocess(s)
    n = len(T)
    P = [0] * n
    C, R = 0, 0

    for i in range(1, n - 1):
        i_mirror = 2 * C - i
        if R > i:
            P[i] = min(R - i, P[i_mirror])

        while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
            P[i] += 1

        if i + P[i] > R:
            C = i
            R = i + P[i]

    max_len = max(P)
    center_index = P.index(max_len)
    start = (center_index - max_len) // 2
    return s[start:start + max_len]


