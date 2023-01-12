#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import time
import datetime


# 秒级时间戳转化为格式化时间
def getFormatTime(timestamp):
	if len(str(timestamp).split(".")[0]) > 10:
		print("请输入秒级时间戳，10位长度")
		return None
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


# 时间格式转化为时间戳
def getTimeStampByYYYYMMDD (strtime):
	return time.mktime(time.strptime(strtime, "%Y-%m-%d %H:%M:%S"))


def getFormatTimeYMD():
	return time.strftime('%Y-%m-%d', time.localtime())


def getFormatTimeYMDDays (days):
	return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%Y-%m-%d')


def getFormatTimeYMDHMSDays (days):
	return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%Y-%m-%d')


def getFormatTimeYYMMDD():
	return time.strftime('%Y-%m-%d', time.localtime())


def getFormatTimeYYMMDDSS():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def getTimestampMs():
	return str(round(time.time() * 1000))


def getTimesTZ():
	return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


if __name__ == '__main__':
	ymd = getFormatTimeYMD()
	yymmdd = getFormatTimeYYMMDD()
	yymmddss = getFormatTimeYYMMDDSS()
	t = getTimestampMs()
	print(ymd)
	print(yymmdd)
	print(yymmddss)
	print(t)
	print(time.localtime(time.time()))
	print(getTimesTZ())

