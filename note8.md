**密码安全性**

保证数据库中的密码安全，关键不在于保存密码本身，而要存储密码的散列值。

密码的验证 使用同样的加密算法可复现结果。

生成密码散列值：

generate_passwoed_hash(password,method=pbkdf2:sha1, salt_length=8 )

验证密码：

check_password_hash(hash, password)