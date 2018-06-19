import string


def xor(s1, s2):
    assert len(s1) == len(s2)
    result = b''
    for c1, c2 in zip(s1, s2):
        result += bytes([c1 ^ c2])
    return result


def xor_key(s1, key):
    l = len(key)
    s2 = key * (len(s1) // l + 1)
    return xor(s1, s2[:len(s1)])


def ascii_freq(string_input):
    score = 0
    for char in string_input:
        if chr(char) in string.printable:
            score += 1
    return score


def ascii_freq_hist(string_input):
    hist = [0] * 127
    for char in string_input:
        if chr(char) in string.printable:
            hist[char] += 1
    return hist


def ascii_freq_hist_likelyhood_score(hist):
    score = 0
    weights = {
        "lowercase": 4,
        "uppercase": 3,
        "numbers": 2,
        "other": 1
    }
    for i, num in enumerate(hist):
        char = chr(i)
        curr_score = 0
        if char in string.ascii_lowercase:
            curr_score = weights['lowercase']
        elif char in string.ascii_uppercase or char == " ":
            curr_score = weights['uppercase']
        elif char in string.digits or char == "_":
            curr_score = weights['numbers']
        elif char in string.printable:
            curr_score = weights['other']

        score += curr_score * num
    return score


def hamming_dist(s1, s2):
    assert len(s1) == len(s2)

    dist = 0
    for c1, c2 in zip(s1, s2):
        bits1 = bin(c1)[2:]
        bits2 = bin(c2)[2:]

        bits1 = "0" * (8 - len(bits1)) + bits1
        bits2 = "0" * (8 - len(bits2)) + bits2

        for b1, b2 in zip(bits1, bits2):
            if b1 != b2:
                dist += 1

    return dist


def print_hist(hist, divisor=1):
    for i, num in enumerate(hist):
        if num > 0:
            print(chr(i), ":", "*" * (num // divisor))


def blocks_of(s, size=16):
    for i in range(0, len(s), size):
        yield s[i: i + size]
