class DES:
    # ---------------- 核心常量与置换表 ----------------

    # 初始置换表 (IP)
    IP = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    # 逆初始置换表 (FP / IP^-1)
    FP = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9,  49, 17, 57, 25
    ]

    # 扩展置换表 (E-Box)
    E = [
        32, 1,  2,  3,  4,  5,
        4,  5,  6,  7,  8,  9,
        8,  9,  10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    # P盒置换表 (P-Box)
    P = [
        16, 7,  20, 21, 29, 12, 28, 17,
        1,  15, 23, 26, 5,  18, 31, 10,
        2,  8,  24, 14, 32, 27, 3,  9,
        19, 13, 30, 6,  22, 11, 4,  25
    ]

    # 密钥置换表 1 (PC-1)
    PC1 = [
        57, 49, 41, 33, 25, 17, 9,
        1,  58, 50, 42, 34, 26, 18,
        10, 2,  59, 51, 43, 35, 27,
        19, 11, 3,  60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7,  62, 54, 46, 38, 30, 22,
        14, 6,  61, 53, 45, 37, 29,
        21, 13, 5,  28, 20, 12, 4
    ]

    # 密钥置换表 2 (PC-2)
    PC2 = [
        14, 17, 11, 24, 1,  5,
        3,  28, 15, 6,  21, 10,
        23, 19, 12, 4,  26, 8,
        16, 7,  27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]

    # 每轮密钥左移位数
    SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # S盒 (Substitution Boxes)
    S_BOX = [
        # S1
        [
            [14, 4,  13, 1,  2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0,  7],
            [0,  15, 7,  4,  14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3,  8],
            [4,  1,  14, 8,  13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5,  0],
            [15, 12, 8,  2,  4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6,  13]
        ],
        # S2
        [
            [15, 1,  8,  14, 6,  11, 3,  4,  9,  7,  2,  13, 12, 0,  5,  10],
            [3,  13, 4,  7,  15, 2,  8,  14, 12, 0,  1,  10, 6,  9,  11, 5],
            [0,  14, 7,  11, 10, 4,  13, 1,  5,  8,  12, 6,  9,  3,  2,  15],
            [13, 8,  10, 1,  3,  15, 4,  2,  11, 6,  7,  12, 0,  5,  14, 9]
        ],
        # S3
        [
            [10, 0,  9,  14, 6,  3,  15, 5,  1,  13, 12, 7,  11, 4,  2,  8],
            [13, 7,  0,  9,  3,  4,  6,  10, 2,  8,  5,  14, 12, 11, 15, 1],
            [13, 6,  4,  9,  8,  15, 3,  0,  11, 1,  2,  12, 5,  10, 14, 7],
            [1,  10, 13, 0,  6,  9,  8,  7,  4,  15, 14, 3,  11, 5,  2,  12]
        ],
        # S4
        [
            [7,  13, 14, 3,  0,  6,  9,  10, 1,  2,  8,  5,  11, 12, 4,  15],
            [13, 8,  11, 5,  6,  15, 0,  3,  4,  7,  2,  12, 1,  10, 14, 9],
            [10, 6,  9,  0,  12, 11, 7,  13, 15, 1,  3,  14, 5,  2,  8,  4],
            [3,  15, 0,  6,  10, 1,  13, 8,  9,  4,  5,  11, 12, 7,  2,  14]
        ],
        # S5
        [
            [2,  12, 4,  1,  7,  10, 11, 6,  8,  5,  3,  15, 13, 0,  14, 9],
            [14, 11, 2,  12, 4,  7,  13, 1,  5,  0,  15, 10, 3,  9,  8,  6],
            [4,  2,  1,  11, 10, 13, 7,  8,  15, 9,  12, 5,  6,  3,  0,  14],
            [11, 8,  12, 7,  1,  14, 2,  13, 6,  15, 0,  9,  10, 4,  5,  3]
        ],
        # S6
        [
            [12, 1,  10, 15, 9,  2,  6,  8,  0,  13, 3,  4,  14, 7,  5,  11],
            [10, 15, 4,  2,  7,  12, 9,  5,  6,  1,  13, 14, 0,  11, 3,  8],
            [9,  14, 15, 5,  2,  8,  12, 3,  7,  0,  4,  10, 1,  13, 11, 6],
            [4,  3,  2,  12, 9,  5,  15, 10, 11, 14, 1,  7,  6,  0,  8,  13]
        ],
        # S7
        [
            [4,  11, 2,  14, 15, 0,  8,  13, 3,  12, 9,  7,  5,  10, 6,  1],
            [13, 0,  11, 7,  4,  9,  1,  10, 14, 3,  5,  12, 2,  15, 8,  6],
            [1,  4,  11, 13, 12, 3,  7,  14, 10, 15, 6,  8,  0,  5,  9,  2],
            [6,  11, 13, 8,  1,  4,  10, 7,  9,  5,  0,  15, 14, 2,  3,  12]
        ],
        # S8
        [
            [13, 2,  8,  4,  6,  15, 11, 1,  10, 9,  3,  14, 5,  0,  12, 7],
            [1,  15, 13, 8,  10, 3,  7,  4,  12, 5,  6,  11, 0,  14, 9,  2],
            [7,  11, 4,  1,  9,  12, 14, 2,  0,  6,  10, 13, 15, 3,  5,  8],
            [2,  1,  14, 7,  4,  10, 8,  13, 15, 12, 9,  0,  3,  5,  6,  11]
        ]
    ]

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