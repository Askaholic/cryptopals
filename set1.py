import base64
import string
from binascii import hexlify, unhexlify

from transcode import ascii_freq, xor, xor_key


def chal1():
    string_input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    print(base64.b64encode(unhexlify(string_input)))


def chal2():
    result = xor(
        unhexlify('1c0111001f010100061a024b53535009181c'),
        unhexlify('686974207468652062756c6c277320657965')
    )
    print("{} - {}".format(result, hexlify(result)))


def chal3():
    string_input = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    binary_input = unhexlify(string_input)

    (top, top_score) = find_xor_candidates(binary_input)

    print("Best found: ")
    for (candidate, key) in top:
        print("{} - Key: {} Score: {}".format(candidate, key, top_score))


def find_xor_candidates(binary_input, top_score=0, top=None):
    if top is None:
        top = []
    for char in string.printable:
        xored_result = xor(binary_input, char.encode() * len(binary_input))
        score = ascii_freq(xored_result)

        if score > top_score:
            top_score = score
            top = [(xored_result, char)]
        elif top_score == score:
            top_score = score
            top.append((xored_result, char))
    return (top, top_score)


def chal4():
    top = []
    top_score = 0
    with open("4.txt", "r") as f:
        for line in f.readlines():
            (top, top_score) = find_xor_candidates(unhexlify(line.strip()), top_score, top)

    print("Best found: {}".format(top_score))
    for (candidate, key) in top:
        print("{} - Key: {}".format(candidate, key))


def chal5():
    string_input = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    print(hexlify(xor_key(string_input.encode(), b'ICE')))


if __name__ == '__main__':
    chal5()
