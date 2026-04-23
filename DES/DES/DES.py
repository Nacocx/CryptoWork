# 导入矩阵和常量
try:
    from .DES_Matrixes import *
except ImportError:
    from DES_Matrixes import *
class DES:
    # ---------------- 核心常量与置换表 ----------------
    IP=IP
    FP=FP
    E=E
    P=P
    PC1=PC1
    PC2=PC2
    SHIFTS = SHIFTS
    S_BOX = S_BOX


    def __init__(self, key: bytes):
        if len(key) != 8:
            raise ValueError("DES 密钥必须刚好是 8 字节 (64 位)。")
        self.subkeys = self._generate_subkeys(self._bytes_to_bits(key))

    # ---------------- 辅助工具函数 ----------------

    def _bytes_to_bits(self, data: bytes) -> list:
        """将字节串转换为比特列表(0和1)"""
        bits = []
        for byte in data:
            bits.extend([int(x) for x in format(byte, '08b')])
        return bits

    def _bits_to_bytes(self, bits: list) -> bytes:
        """将比特列表转换回字节串"""
        byte_array = bytearray()
        for i in range(0, len(bits), 8):
            byte_val = int("".join(str(x) for x in bits[i:i+8]), 2)
            byte_array.append(byte_val)
        return bytes(byte_array)

    def _permute(self, block: list, table: list) -> list:
        """根据给定的表执行置换，由于表是从1开始的，索引需要减1"""
        return [block[i - 1] for i in table]

    def _xor(self, bits1: list, bits2: list) -> list:
        """两个比特列表执行异或操作"""
        return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

    def _pkcs7_pad(self, data: bytes) -> bytes:
        """PKCS#7 填充机制，使数据长度为8的整数倍"""
        padding_len = 8 - (len(data) % 8)
        return data + bytes([padding_len] * padding_len)

    def _pkcs7_unpad(self, data: bytes) -> bytes:
        """移除 PKCS#7 填充"""
        padding_len = data[-1]
        return data[:-padding_len]

    # ---------------- 核心算法步骤 ----------------

    def _generate_subkeys(self, key_bits: list) -> list:
        """生成 16 轮子密钥"""
        # 第一步：PC-1 置换 (64位 -> 56位)
        key_56 = self._permute(key_bits, self.PC1)
        left = key_56[:28]
        right = key_56[28:]
        
        subkeys = []
        for shift in self.SHIFTS:
            # 循环左移
            left = left[shift:] + left[:shift]
            right = right[shift:] + right[:shift]
            # 第二步：PC-2 置换 (56位 -> 48位)
            subkey = self._permute(left + right, self.PC2)
            subkeys.append(subkey)
            
        return subkeys

    def _feistel_function(self, right_half: list, subkey: list) -> list:
        """Feistel 网络轮函数 (F函数)"""
        # 1. 扩展置换 (32位 -> 48位)
        expanded = self._permute(right_half, self.E)
        
        # 2. 与子密钥异或
        xored = self._xor(expanded, subkey)
        
        # 3. S盒代换 (48位 -> 32位)
        substituted = []
        for i in range(8):
            chunk = xored[i * 6 : (i + 1) * 6]
            # 头尾两位决定行，中间四位决定列
            row = (chunk[0] << 1) + chunk[5]
            col = (chunk[1] << 3) + (chunk[2] << 2) + (chunk[3] << 1) + chunk[4]
            
            val = self.S_BOX[i][row][col]
            # 将输出的十进制转换为 4 位二进制列表
            substituted.extend([int(x) for x in format(val, '04b')])
            
        # 4. P盒置换
        return self._permute(substituted, self.P)

    def _process_block(self, block: list, subkeys: list) -> list:
        """处理 64 位数据块（加密或解密取决于子密钥的顺序）"""
        # 1. 初始置换 IP
        block = self._permute(block, self.IP)
        left = block[:32]
        right = block[32:]
        
        # 2. 16轮 Feistel 网络
        for subkey in subkeys:
            next_left = right
            f_result = self._feistel_function(right, subkey)
            right = self._xor(left, f_result)
            left = next_left
            
        # 3. 交换左右半部分，并做逆初始置换 (FP)
        combined = right + left
        return self._permute(combined, self.FP)

    # ---------------- 接口方法 ----------------

    def encrypt(self, data: bytes) -> bytes:
        """加密字节数据并返回密文"""
        padded_data = self._pkcs7_pad(data)
        bits = self._bytes_to_bits(padded_data)
        
        encrypted_bits = []
        for i in range(0, len(bits), 64):
            block = bits[i:i+64]
            encrypted_bits.extend(self._process_block(block, self.subkeys))
            
        return self._bits_to_bytes(encrypted_bits)

    def decrypt(self, data: bytes) -> bytes:
        """解密字节数据并移除填充"""
        bits = self._bytes_to_bits(data)
        # 解密时使用逆序的子密钥
        rev_subkeys = self.subkeys[::-1]
        
        decrypted_bits = []
        for i in range(0, len(bits), 64):
            block = bits[i:i+64]
            decrypted_bits.extend(self._process_block(block, rev_subkeys))
            
        unpadded_data = self._pkcs7_unpad(self._bits_to_bytes(decrypted_bits))
        return unpadded_data