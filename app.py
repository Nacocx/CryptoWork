from DES import DES

if __name__ == "__main__":
    # 密钥必须是正好 8 个字节
    key = b"Secret8!"
    
    # 待加密的消息（可以是任意长度）
    message = "这是一个不调用库的纯Python DES算法演示。"
    plaintext = message.encode('utf-8')
    
    print(f"原始文本: {message}")
    print(f"密钥: {key.decode('utf-8')}")
    
    # 初始化 DES 实例
    des = DES(key)
    
    # ---------------- 加密 ----------------
    ciphertext = des.encrypt(plaintext)
    print(f"\n[加密完成] 密文(Hex格式): {ciphertext.hex()}")
    
    # ---------------- 解密 ----------------
    decrypted_bytes = des.decrypt(ciphertext)
    decrypted_message = decrypted_bytes.decode('utf-8')
    print(f"[解密完成] 解密后文本: {decrypted_message}")