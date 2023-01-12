#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from Crypto.Cipher import AES, DES
import hashlib


def padding_pkcs5(BS, value):
	return str.encode(value + (BS - len(value) % BS) * chr(BS - len(value) % BS))


def padding_zero(value):
	while len(value) % 16 != 0:
		value += '\0'
	return str.encode(value)


def get_shalprng_key(key):
	signature = hashlib.sha1(key.encode("utf-8")).digest()
	signature = hashlib.sha1(signature).digest()
	return "".join(['%02x' % i for i in signature]).upper()[:32]


# aes加密，开放平台有用到
def aes_ecb_encrypt(key, value):
	BS = AES.block_size
	key = get_shalprng_key(key)
	cryptor = AES.new(bytes.fromhex(key), AES.MODE_ECB)
	padding_value = padding_pkcs5(BS, value)
	signtext = cryptor.encrypt(padding_value)
	return "".join(['%02x' % i for i in signtext]).upper()


# des加密，mes账户安全使用
def des_ecb_encrypt(value):
	key = "jinlaikelanxiaobotangjuandongbo"
	BS = DES.block_size
	cryptor = DES.new(key.encode("utf-8")[0:8], DES.MODE_ECB)
	padding_value = padding_pkcs5(BS, value)
	signtext = cryptor.encrypt(padding_value)
	return"".join(['%02x' % i for i in signtext])


if __name__ == '__main__':
	baseur1 = "http://10.10.201.221:8848"
	auth_url = baseur1 + "/open/api/auth"
	appid = "PuHuiKVIrPvhWbDYDnoUfgQJ"
	sercret = "742574a687124bf1b4d7728b4e37c58e"
	timestamp = "1585791530775"
	headers = {"appId": appid, "secretKey": sercret, "timestamp": timestamp, "sign": ""}
	signText = appid + timestamp + sercret + auth_url
	print("signText:" + signText)
	print("timestamp:" + timestamp)
	sign = aes_ecb_encrypt(sercret, signText)
	print("sign:" + sign)

