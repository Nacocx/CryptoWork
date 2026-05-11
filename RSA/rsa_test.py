import time
from rsa_block import *
from outputColor import *
from multiprocessing import Pool, TimeoutError as MpTimeoutError

# --------------------
# 暴力分解 n（模拟 CPA 攻击，小 n 可行）
# --------------------
def factor_n_brute_force(n):
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return i, n // i
    return None, None

# --------------------
# 带超时的暴力分解
# --------------------
def factor_n_with_timeout(n, timeout=10):
    with Pool(processes=1) as pool:
        result = pool.apply_async(factor_n_brute_force, (n,))
        try:
            return result.get(timeout=timeout)
        except MpTimeoutError:
            pool.terminate()
            return None, None

# --------------------
# 测试不同密钥长度的安全性
# --------------------
def test_rsa_security():
    message = "RSA Security Test Message!"
    key_sizes = [8, 16, 32, 64]  # bits
    print(f"{yellow}=== RSA 安全性实验 ==={reset}")
    
    for bits in key_sizes:
        print(f"\n{cyan}[密钥长度: {bits}-bit]{reset}")
        
        # 生成密钥
        start = time.time()
        pub, priv = generate_rsa_keys(bits)
        key_time = time.time() - start
        print(f"{green}密钥生成耗时: {key_time:.4f}s{reset}")
        n, e = pub

        # 加密
        start = time.time()
        cipher_blocks = encrypt_message(message, pub)
        enc_time = time.time() - start
        print(f"{magenta}加密耗时: {enc_time:.4f}s, 密文块数: {len(cipher_blocks)}{reset}")

        # 解密
        start = time.time()
        decrypted = decrypt_message(cipher_blocks, priv)
        dec_time = time.time() - start
        print(f"{green}解密耗时: {dec_time:.4f}s, 解密正确: {decrypted == message}{reset}")

        # 模拟选择明文攻击（小 n 可尝试）
        start = time.time()
        if bits <= 16:
            p, q = factor_n_brute_force(n)
            attack_time = time.time() - start
            if p:
                print(f"{red}[CPA攻击] 分解 n 成功: p={p}, q={q}, 耗时: {attack_time:.4f}s{reset}")
            else:
                print(f"{red}[CPA攻击] 分解 n 失败{reset}")
        else:
            # bits > 16 时尝试暴力，超时10s就认为不可行
            p, q = factor_n_with_timeout(n, timeout=10)
            attack_time = time.time() - start
            if p:
                print(f"{red}[CPA攻击] 分解 n 成功: p={p}, q={q}, 耗时: {attack_time:.4f}s{reset}")
            else:
                print(f"{red}[CPA攻击] 暴力分解超时或不可行（>10s）{reset}")

if __name__ == "__main__":
    test_rsa_security()