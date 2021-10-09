import random
# import base64

# choose prime p and q number
def choose_pq():
    result = ""

    while result != "prime":
        p = random.SystemRandom().getrandbits(32)
        result = miller_rabin_prime_test(p)

    result = ""
    while result != "prime":
        q = random.SystemRandom().getrandbits(32)
        result = miller_rabin_prime_test(q)

    return p, q


# primality test random number p and q with miller-rabin test
def miller_rabin_prime_test(number):
    if number % 2 == 0 or number % 5 == 0: return "not prime"
    number_t = number - 1
    r = 0
    while number_t % 2 == 0:
        number_t = number_t / 2
        r = r + 1

    u = int(number_t)
    number_t = number - 1
    for _ in range(3):
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


def generate():
    p, q = choose_pq()
    n = compute_n_public_key(p, q)
    phi = euler_phi_number(p, q)
    e = find_e_public_key(phi)
    d = find_inverse_d_private_key(e, phi)

    return n, e, d


if __name__ == "__main__":
    generate()



