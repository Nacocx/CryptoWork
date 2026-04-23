from pymodbus.client.sync import ModbusTcpClient
from DES.DES import DES
import outputColor as oc

def str_to_registers(s: str):
    b = s.encode('utf-8')
    if len(b) % 2 != 0:
        b += b'\x00'
    regs = []
    for i in range(0, len(b), 2):
        regs.append((b[i] << 8) + b[i + 1])
    return regs


def registers_to_str(regs):
    b = bytearray()
    for r in regs:
        b.append((r >> 8) & 0xFF)
        b.append(r & 0xFF)
    return b.rstrip(b'\x00').decode('utf-8', errors='ignore')


client = ModbusTcpClient("127.0.0.1", port=5020)

if not client.connect():
    print(f"{oc.red}连接失败{oc.reset}")
    exit()

print(f"{oc.green}已连接到服务器{oc.reset}")

data = "helloworld"
key = b"Secret8!"
des = DES(key)

encrypted_hex = des.encrypt(data.encode()).hex()
print(f"{oc.green}原文: {data}{oc.reset}")
print(f"{oc.green}密文(hex): {encrypted_hex}{oc.reset}")

regs = str_to_registers(encrypted_hex)

res = client.write_registers(0, regs)

if res.isError():
    print(f"{oc.red}写入失败: {res}{oc.reset}")
    client.close()
    exit()

print(f"{oc.green}写入成功{oc.reset}")

result = client.read_holding_registers(0, len(regs))

if result.isError():
    print(f"{oc.red}读取失败: {result}{oc.reset}")
    client.close()
    exit()

received_hex = registers_to_str(result.registers)
print(f"{oc.green}读取(hex): {received_hex}{oc.reset}")

try:
    decrypted = des.decrypt(bytes.fromhex(received_hex))\
        .decode()\
        .rstrip('\x00')
    print(f"{oc.green}解密后: {decrypted}{oc.reset}")
except Exception as e:
    print(f"{oc.red}解密失败: {e}{oc.reset}")

client.close()
print(f"{oc.yellow}连接关闭{oc.reset}")