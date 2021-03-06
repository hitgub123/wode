#coding=utf-8
#非常详细的教程，包含了各种mode：https://blog.csdn.net/u013578500/article/details/77905924


from Crypto.Cipher import AES
import base64
from Crypto import Random

# padding算法
BS = AES.block_size # aes数据分组长度为128 bit

def pad(s):
    add=(BS - len(s)%BS) * chr(0)
    if add==16:add=0
    return (s + add).encode()

class aesdemo:
    def __init__(self, key,mode):
        self.key = key
        self.mode = mode
        
    def encrypt(self, plaintext):
        # 生成随机初始向量IV
        iv = Random.new().read(AES.block_size)
        print('encrypt_iv=',iv)
        cryptor = AES.new(self.key, self.mode, iv)
        
        ciphertext = cryptor.encrypt(pad(plaintext))
        #print(cryptor.decrypt)会报错，提示decrypt() cannot be called after encrypt()
        #似乎创建的只能encrypt或者只能decrypt，交替使用会报错
        # 这里统一把加密后的字符串转化为16进制字符串
        return base64.b64encode(iv + ciphertext)

    def decrypt(self, ciphertext):
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[0:AES.block_size]
        print('decrypt_iv=',iv)
        ciphertext = ciphertext[AES.block_size:len(ciphertext)]
        cryptor = AES.new(self.key, self.mode, iv)
        plaintext = cryptor.decrypt(ciphertext)
        return plaintext.decode().rstrip('\0')          
        #上面这里必须加'\0'，不然不会删除，原因似乎是默认的strip只删除'\s\t\n'

# 测试模块
if __name__ == '__main__':
    # 密钥长度可以为128 / 192 / 256比特，这里采用128比特
    # 指定加密模式为CBC
    demo = aesdemo(b'keyven__keyven__', AES.MODE_CBC)
    e = demo.encrypt('huaQ!!!')
    d = demo.decrypt(e)
    print ("加密：", e)
    print ("解密：", d)

    
===========================================================================

#简化版（？）。key1,key2,m最大长度是16，超过的话要切割，不足则用pad填充

key1,key2,m='key1','key2','huaQ!!!'

def encrypt(key1,key2,m):
    cryptor = AES.new(pad(key1), AES.MODE_CBC, pad(key2))
    m1=cryptor.encrypt(pad(m))
    print(m1)
    return  m1
    

def decrypt(key1,key2,a):
    cryptor = AES.new(pad(key1), AES.MODE_CBC, pad(key2))
    m2=cryptor.decrypt(a).rstrip('\0')
    print(m2)
    return m2


===========================================================================
