import random
import base64
from multiprocessing import Pool

# choose prime p and q number
def choose_pq(n):
    result = ""
    t = 0
    print("now compute p random prime number!")

    while result != "prime":
        p = random.SystemRandom().getrandbits(80)
        result = miller_rabin_prime_test(p)
    print("p is done!!!")
    print("now compute q random prime number!")
    result = ""
    while result != "prime":
        q = random.SystemRandom().getrandbits(80)
        result = miller_rabin_prime_test(q)
    print("compute is done!!!")
    return p, q


# primality test random number p and q with miller-rabin test
def miller_rabin_prime_test(number):
    if number % 2 == 0 or number % 5 == 0:
        return "not prime"
    number_t = number - 1
    r = 0
    while number_t % 2 == 0:
        number_t = number_t / 2
        r = r + 1

    u = int(number_t)
    number_t = number - 1
    for _ in range(24):
        a = random.randint(2, number_t)
        if pow(a, u, number) == 1:
            return "prime"
        for j in range(1, r):
            z = pow(a, u*pow(2, j), number)
            # z = (a**(u*(2**j))) % number
            if z == number_t or z == -1:
                return "prime"
    return "not prime"


# compute public key n with p qnd q prime number
def compute_n_public_key(p, q):
    n = p * q
    return n


# compute Euler's phi number with p qnd q prime number
def euler_phi_number(p, q):
    phi = (p-1) * (q-1)
    return phi


# find e public key with phi and euclid's gcd
def find_e_public_key(phi):
    result = -1
    while result != 1:
        e = random.randint(1, phi)
        result = euclid_gcd(phi, e)

    return e


# Euclid's algorithm - GCD
def euclid_gcd(number_one, number_two):
    a = number_one
    b = number_two

    while b != 0:
        r = b
        b = a % b
        a = r
    return a


# find inverse d private key with e and phi
# by sybrenstuvel/python-rsa
def find_inverse_d_private_key(e, phi):
    x = 0
    lx = 1
    ob = phi  # negative values from return results
    while phi != 0:
        q = e // phi
        (e, phi) = (phi, e % phi)
        (x, lx) = ((lx - (q * x)), x)
    if lx < 0:
        lx += ob

    return lx


# convert char to ascii
def convert_ascii(text):
    ascii_value = []
    for ch in text:
        ascii_value.append(ord(ch))

    return ascii_value

def convert_text(text_list):
    text = ''
    for ch in text_list:
        text += chr(ch)
    return text


# Encrypt Plaintext
def encrypt(plaintext, n, e):
     text_list = convert_ascii(plaintext)
     C_list = []
     C_str = ''
     for M in text_list:
        # C=M^e(mod n)
        C = pow(M, e, n)
        C_list.append(C)
        C_str += str(C)
     print(base64.b64encode(bytes(C_str, "ascii")))
     return C_list


# Decrypt Ciphertext
def decrypt(ciphertext, n, d):
    text_list = ciphertext
    M_list = []
    for C in text_list:
        # M=C^d(mod n)
        M = pow(C, d, n)
        M_list.append(M)
    plaintext = convert_text(M_list)
    print(plaintext)


if __name__ == "__main__":

    plaintext = '12345'
    # "Python is a popular open source programming language used for both standalone pro" # \
             #   "grams and scripting applications in a wide variety of domains. It is free, portable, powerful, " \
              #  "and is both relatively easy and remarkably fun to use. Programmers from every" \
             #   " corner of the software industry have found Python’s focus on developer productivity" \
             #   " and software quality to be a strategic advantage in projects both large and small."
    

    with Pool(5) as pr:
        p,q = pr.map(choose_pq, range(5))
        pr.terminate()
        pr.join()

    #p, q = choose_pq()
    n = compute_n_public_key(p, q)
    phi = euler_phi_number(p, q)
    e = find_e_public_key(phi)
    d = find_inverse_d_private_key(e, phi)

    print(n, e, d)

    C = encrypt(plaintext, n, e)
    print('')
    decrypt(C, n, d)




