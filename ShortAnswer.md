# HW3 Short Answers

## 1.5

1. Why does using GCM prevent mauling and padding oracle attacks?

GCM hashes the plain text so it can prevent mauling attacks. On the other hand, in padding oracle attacks, attackers need to use the previous block and attempt to find the good result by trial-and-error. But GCM's hash result for each block depends on the value of IV and a counter instead of the previous cypher block. Therefore GCM can also prevent padding oracle attacks.

2. For each attack above, explain whether enabling HTTPS for the entire payment site (as opposed to just the login page) prevents the attack if no other counter-measure is applied

HTTPS encrypts data sending via the website, so it could prevent mauling attacks where attackers need to know the paintext cookies. It could also prevent from padding oracle attacks since padding oracle attacks rely on information leakage. HTTPS encrypts the returned messages as well, so it is not possible for the attackers to know if the attack is successful.
