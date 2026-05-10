实现了简单的`RSA`加密算法，并且编写`rsa_test`脚本进行验证

`RSA`步骤

1. 获得大素数p q
2. 计算模数n和欧拉函数ϕ(n)
   1. ϕ(n)=ϕ(p * q) = ϕ(p) * ϕ(q)
   2. p q 是素数 => ϕ(n)=(p−1)(q−1)
3. 选择公钥指数e，要满足 1 < e < ϕ(n)，并且gcd(e,ϕ(n))=1，常用65537
4. 计算私钥指数d，要满足 d⋅e≡1(modϕ(n))，使用扩展欧几里得算法
5. 加密解密
   1. 加密 $c = m^e \mod n$
   2. 解密 $m = c^d \mod n$
6. 加密解密原理：
   
我们要证明：

$
(m^e)^d \equiv m \pmod n
$

也就是

$
m^{ed} \mod n
$

由于 $(d \cdot e \equiv 1 \mod \phi(n))$，可以写作：

$
ed = k \cdot \phi(n) + 1 \quad \text{(k 为某个整数)}
$


$
m^{ed} = m^{k \phi(n) + 1} = m^{k \phi(n)} \cdot m
$

由欧拉定理：

> 如果 $ \gcd(m, n) = 1 $，则
> $
> m^{\phi(n)} \equiv 1 \pmod n
> $

所以：

$
m^{k \phi(n)} \equiv 1^k \equiv 1 \pmod n
$


$
m^{ed} \equiv 1 \cdot m \equiv m \pmod n
$
