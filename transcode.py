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
