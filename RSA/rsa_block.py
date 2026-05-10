import random
from math import gcd
from outputColor import *

# --------------------
# Miller-Rabin 素数测试（快速生成大素数）
# --------------------
def is_prime_mr(n, k=5):
    if n < 2:
        return False
    if n in (2,3):
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n-1
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randrange(2, n-1)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def generate_large_prime(bits=32):
    while True:
        p = random.getrandbits(bits) | 1  # 确保奇数
        if is_prime_mr(p):
            return p

# --------------------
# 扩展欧几里得求逆元
# --------------------
def modinv(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x % m

# --------------------
# RSA 密钥生成
# --------------------
def generate_rsa_keys(bits=32):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    while p == q:
        q = generate_large_prime(bits)
    n = p * q
    phi = (p-1)*(q-1)
    
    e = 3
    while gcd(e, phi) != 1:
        e += 2
    d = modinv(e, phi)
    return (n, e), (n, d)

# --------------------
# RSA 基本加解密（单整数）
# --------------------
def encrypt_int(m, pubkey):
    n, e = pubkey
    return pow(m, e, n)

def decrypt_int(c, privkey):
    n, d = privkey
    return pow(c, d, n)

# --------------------
# 自动分块加密/解密
# --------------------
def encrypt_message(message, pubkey):
    n, e = pubkey
    message_bytes = message.encode()
    block_size = (n.bit_length() - 1) // 8
    cipher_blocks = []
    for i in range(0, len(message_bytes), block_size):
        block = message_bytes[i:i+block_size]
        m_int = int.from_bytes(block, 'big')
        c_int = encrypt_int(m_int, pubkey)
        cipher_blocks.append(c_int)
    return cipher_blocks

def decrypt_message(cipher_blocks, privkey):
    plain_bytes = b''
    for c_int in cipher_blocks:
        m_int = decrypt_int(c_int, privkey)
        block_bytes = m_int.to_bytes((m_int.bit_length() + 7)//8, 'big')
        plain_bytes += block_bytes
    return plain_bytes.decode()

# --------------------
# 测试
# --------------------
if __name__ == "__main__":
    pub, priv = generate_rsa_keys(bits=64)  # 用 64-bit 素数，Miller-Rabin 快速生成
    print(f"{green}公钥: {pub}{reset}")
    print(f"{green}私钥: {priv}{reset}")

    message = "Hello, this is a long message for RSA encryption!"
    print(f"{cyan}原文: {message}{reset}")

    cipher_blocks = encrypt_message(message, pub)
    print(f"{magenta}加密块: {cipher_blocks}{reset}")

    decrypted = decrypt_message(cipher_blocks, priv)
    print(f"{green}解密: {decrypted}{reset}")