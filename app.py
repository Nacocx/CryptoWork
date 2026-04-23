from DES import DES
import sys
import outputColor as oc

test_keys=[b"Secret8!", b"AnotherK", b"12345678", b"ABCDEFGH"]

test_messages=[
    "Hello, World! This is a test message for DES encryption.",
    "DES算法虽然过时，但它是对称加密历史上的重要里程碑。",
    "Python实现的DES算法可以帮助我们理解加密的基本原理。"
]

def test_des(test_keys=test_keys, test_messages=test_messages):
    for key in test_keys:
        des = DES(key)
        print(f"\n{oc.magenta}测试密钥: {key.decode('utf-8')}{oc.reset}")
        
        for message in test_messages:
            plaintext = message.encode('utf-8')
            print(f"\n{oc.yellow}原始文本: {message}{oc.reset}")
            
            # 加密
            ciphertext = des.encrypt(plaintext)
            print(f"{oc.cyan}密文(Hex格式): {ciphertext.hex()}{oc.reset}")
            
            # 解密
            decrypted_bytes = des.decrypt(ciphertext)
            decrypted_message = decrypted_bytes.decode('utf-8')
            print(f"{oc.green}解密后文本: {decrypted_message}{oc.reset}")
            
            assert message == decrypted_message, f"{oc.red}解密后的文本与原始文本不匹配！{oc.reset}"

            print("----" * 10)
if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_des(test_keys=[sys.argv[1].encode('utf-8')], test_messages=sys.argv[2:])   
    else:
        test_des()
    