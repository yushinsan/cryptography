# XORIUM
## Post-quantum cryptograhy

Let me demonstrate a useful cryptographic algorithm called Xorium, which belongs to the category of symmetric post-quantum protocols.

In the theory of information security, there is a concept of One-Time Pads, the essence of which is that when we perform an XOR logical operation between a completely random sequence of data and predictable data, the entropy of the result tends to infinity.
This is due to the XOR operator, since in the expression [A XOR B = C], when we see C, we do not know what A and B are equal to, with A = absolute random and B = the original text.

The Xorium algorithm aims to be a compact version of One-Time Pads.
The main parts of the algorithm are the ENC (Encode) and DEC (Decode) functions, as well as additional functions for converting text to bytes and pseudo-randomization.

We will only consider the ENC function, since DEC is its reversible counterpart.
Create a Nonce based on a cryptographically secure pseudo-random module [secrets]\
<code>
F = 12  
N = secrets.token_bytes(F)
</code>
This ensures that the same message will always be encrypted differently with the same key.
Then, throughout the entire message, we perform an XOR operation with the Nonce, key, and counter for each 32-byte block of the original data:\
<code> 
h = HASH(BT(N) + key + str(z), t=False)  
z += 1  
cur = x[i:i+32]  
for j in range(len(cur)): res[i + j] = cur[j] ^ h[j]  
</code>
It is impossible to recover the original data that was xor-ed with a SHA-256 hash array that has been proven to have extremely high entropy.
To further confuse the attacker, we will turn the linear change in the counter into a nonlinear one:\
<code>
- for ENC and DEC, we will calculate the vector that the counter will move along  
T = HASH('XRM' + BT(N) + key, t=False)  
- in each iteration, we change the counter to an element from the calculated gamma; since the counter only increases, its values will never overlap
a += 1  
z += T[a % len(T)]  
</code>
With every 32 bytes, we encounter a new hash, and the counter ensures that each block of data is independent of each other and their encryption is subject to an avalanche effect.
To ensure that the encrypted message cannot be tampered with or corrupted, we will add a signature (without a key, to enhance quantum resistance):\
<code>
sign = HASH(x, t=True, b=True)[0:12].encode()  
x = x + sign  
</code>
There are more SHA-256 brute force variations than there are atoms in the universe, and it is believed that the result of a hash function cannot be analytically reversed into its original data.
I believe that my algorithm has no logical vulnerabilities, and since it relies on SHA-256, its resistance reaches the post-quantum level, therefore
# In the entire space and time of existence, there is no entity that can without a key decrypt a message encrypted by this algorithm at any time or place, even if it is not an organic entity.
