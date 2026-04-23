from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from DES.DES import DES
import outputColor as oc

def registers_to_str(regs):
    b = bytearray()
    for r in regs:
        b.append((r >> 8) & 0xFF)
        b.append(r & 0xFF)
    return b.rstrip(b'\x00').decode('utf-8', errors='ignore')


class HookDataBlock(ModbusSequentialDataBlock):
    def __init__(self, address, values, key: bytes):
        super().__init__(address, values)
        self.des = DES(key)

    def setValues(self, address, values):
        print(f"{oc.yellow}[HOOK] address={address}, values={values}{oc.reset}")

        try:
            encrypted_hex = registers_to_str(values)

            if encrypted_hex:
                encrypted_bytes = bytes.fromhex(encrypted_hex)
                plaintext = self.des.decrypt(encrypted_bytes)\
                    .decode("utf-8", errors="ignore")\
                    .rstrip('\x00')

                print(f"{oc.green}[+] 密文: {encrypted_hex}{oc.reset}")
                print(f"{oc.green}[+] 明文: {plaintext}{oc.reset}")

        except Exception as e:
            print(f"{oc.red}[!] 解密失败: {e}{oc.reset}")

        return super().setValues(address, values)


store = ModbusSlaveContext(
    hr=HookDataBlock(0, [0]*200, key=b"Secret8!")
)

context = ModbusServerContext(slaves=store, single=True)

print(f"{oc.yellow}Server running on port 5020...{oc.reset}")
StartTcpServer(context, address=("0.0.0.0", 5020))