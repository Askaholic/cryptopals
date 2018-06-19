import base64
import string
from binascii import hexlify, unhexlify

from lib import (
    ascii_freq,
    ascii_freq_hist,
    ascii_freq_hist_likelyhood_score,
    blocks_of,
    hamming_dist,
    print_hist,
    xor,
    xor_key
)


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
        score = ascii_freq_hist_likelyhood_score(ascii_freq_hist(xored_result))
        # score = ascii_freq(xored_result)

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


def chal6():
    cipher = b""
    with open("6.txt", 'r') as f:
        cipher = base64.b64decode(f.read().replace('\n', ''))

    dists = get_average_hamming_distances(cipher)
    dists.sort(key=lambda x: x[1])

    # print(dists)

    for i in range(4):
        key_len = dists[i][0]
        print("Length: ", key_len)
        final_keys = find_keys_from_keysize(cipher, key_len)

        print(final_keys)
        for key in final_keys:
            print(xor_key(cipher, key))


def get_average_hamming_distances(cipher, num_samples=4):
    dists = []
    for ksize in range(2, 40):
        total_dist = 0
        for i in range(num_samples):
            t1 = cipher[i * ksize:i * ksize + ksize]
            t2 = cipher[i * ksize + ksize:i * ksize + ksize * 2]
            total_dist += hamming_dist(t1, t2)
        dists.append((ksize, total_dist / (num_samples * ksize)))
    return dists


def find_keys_from_keysize(cipher, key_len):
    transposed = transpose_blocks(cipher, key_len)

    final_keys = [b'']
    for data in transposed:
        (top, top_score) = find_xor_candidates(data)

        if len(top) > 1:

            old_final_keys = list(final_keys)
            new_final_keys = []
            for (_, key) in top:
                new_keys = list(old_final_keys)
                for i, k in enumerate(new_keys):
                    new_keys[i] = k + key.encode()
                new_final_keys += new_keys
            final_keys = new_final_keys
        else:
            for i, k in enumerate(final_keys):
                final_keys[i] = k + top[0][1].encode()

    return final_keys


def transpose_blocks(cipher, block_size):
    transposed = [b""] * block_size

    for block in blocks_of(cipher, size=block_size):
        for i, byte in enumerate(block):
            transposed[i] += bytes([byte])
    return transposed


if __name__ == '__main__':
    chal6()

    # strings = [
    #     b"ASJDKLAJSKDJHALSKJDHLASKJD",
    #     xor_key(b"The lazy brown fox jumps over the quick hedgehog", b"?")
    # ]
    # for s in strings:
    #     print("String: ", s)
    #     hist = ascii_freq_hist(s)
    #     print_hist(hist)
    #     print("Score: ", ascii_freq_hist_likelyhood_score(hist))
    #
    # print(find_xor_candidates(strings[1]))
