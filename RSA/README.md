# 简单 RSA 加密算法实现与验证

实现了一个简单的 `RSA` 加密算法，并编写 `rsa_test` 脚本进行验证。

## RSA 步骤

1. **获得大素数** `p` 和 `q`
2. **计算模数** `n` 和欧拉函数 `ϕ(n)`

   * $$
     \phi(n) = \phi(p \cdot q) = \phi(p) \cdot \phi(q)
     $$
   * 由于 `p` 和 `q` 是素数：
     $$
     \phi(n) = (p-1)(q-1)
     $$
3. **选择公钥指数** `e`

   * 要满足 
     $$
     1 < e < \phi(n) \quad \text{且} \quad \gcd(e, \phi(n)) = 1
     $$
   * 常用值：`65537`
1. **计算私钥指数** `d`

   * 要满足：
     $$
     d \cdot e \equiv 1 \mod \phi(n)
     $$
   * 使用 **扩展欧几里得算法** 求解
2. **加密与解密**

   * 加密：
     $$
     c = m^e \mod n
     $$
   * 解密：
     $$
     m = c^d \mod n
     $$
3. **加密解密原理**

   我们要证明：
   $$
   (m^e)^d \equiv m \mod n
   $$
   即
   $$
   m^{ed} \mod n
   $$

   由于
   $$
   d \cdot e \equiv 1 \mod \phi(n)
   $$
   可以写作：
   $$
   ed = k \cdot \phi(n) + 1 \quad \text{(k 为某个整数)}
   $$

   因此：
   $$
   m^{ed} = m^{k \phi(n) + 1} = m^{k \phi(n)} \cdot m
   $$

   根据 **欧拉定理**：

   > 如果 $ \gcd(m, n) = 1 $，则
   > $$
   > m^{\phi(n)} \equiv 1 \mod n
   > $$

   所以：
   $$
   m^{k \phi(n)} \equiv 1^k \equiv 1 \mod n
   $$

   最终：
   $$
   m^{ed} \equiv 1 \cdot m \equiv m \mod n
   $$