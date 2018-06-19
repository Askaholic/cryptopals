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


def blocks_of(s, size=16):
    for i in range(0, len(s), size):
        yield s[i: i + size]
