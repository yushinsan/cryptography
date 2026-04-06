# Post-quantum symmetric cryptographic protocol
# XORIUM

import hashlib
import secrets

def BT(x):
    res = ''
    for i in x:
        s = hex(i)
        s = s[2:len(s)].upper()
        while len(s) < 2: s = '0' + s
        res = res + s
    return res
def TB(x):
    res = b''
    i = 0
    while i < len(x):
        s = int(x[i:i+2], 16).to_bytes()
        res = res + s
        i += 2
    return res
def HASH(x, t=True, b=False):
    if not b: x = x.encode()
    res = hashlib.sha256(x).digest()
    if t: res = BT(res)
    return res
def RAN(n, t=True):
    res = secrets.token_bytes(n)
    if t: res = BT(res)
    return res
def ENC(x, key, t=True, b=False):
    if not b: x = x.encode()
    sign = HASH(x, t=True, b=True)[0:12].encode()
    x = x + sign
    F = 12
    N = secrets.token_bytes(F)
    T = HASH('XRM' + BT(N) + key, t=False)
    res = bytearray(len(x))
    step, a, z = 32, 0, 0
    for i in range(0, len(x), step):
        h = HASH(BT(N) + key + str(z), t=False)
        a += 1
        z += T[a % len(T)]
        cur = x[i:i+step]
        for j in range(len(cur)): res[i + j] = cur[j] ^ h[j]
    res = N + res
    if t: res = BT(res)
    return res
def DEC(x, key, t=True, b=False):
    try:
        if t: x = TB(x)
        F = 12
        N = x[:F]
        T = HASH('XRM' + BT(N) + key, t=False)
        C = x[F:]
        res = bytearray(len(C))
        step, a, z = 32, 0, 0
        for i in range(0, len(C), step):
            h = HASH(BT(N) + key + str(z), t=False)
            a += 1
            z += T[a % len(T)]
            cur = C[i:i+step]
            for j in range(len(cur)): res[i + j] = cur[j] ^ h[j]
        res = bytes(res)
        c = res[len(res)-12:len(res)]
        res = res[0:len(res)-12]
        sign = HASH(res, t=True, b=True)[0:12].encode()
        if sign == c:
            if not b: res = res.decode()
            return res
        else: return False
    except: return False
