#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An

# !/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
import random
import string


class RandomUtil:

	@staticmethod
	def random_phone():
		firsts = ['130', '131', '132', '133', '134', '135', '136', '137',
					'138', '139', '145', '147', '149', '150', '151', '152',
					'153', '155', '156', '157', '158', '159', '173', '176',
					'177', '178', '180', '181', '182', '183', '184', '185',
					'186', '187', '188', '189']
		k = 8
		phone = random.choice(firsts) + ''.join(random.sample('0123456789', k))
		return phone

	@staticmethod
	def random_string(length, punctuation=False, digits=True, startswith=''):
		"""
		随机字符串,传入长度,特殊字符默认没有,默认有数字
		:param length:长度
		:param punctuation:特殊符号,默认没有
		:param digits:数字,默认有
		:param startswith:自定义开头
		:return:一个随机字符串
		"""
		sample = string.ascii_letters
		if punctuation:
			sample += string.punctuation

		if digits:
			sample += string.digits

		return startswith + "".join([random.choice(sample) for _ in range(length - len(startswith))])

	@staticmethod
	def random_int(length, is_str=True, startswith=''):
		"""
		随机数字。传入数字的长度,例如两位数传2。已字符串形式return
		:param length: 数字的长度
		:param is_str: 默认是字符串,需要数字的将此设置为False
		:return:
		"""
		tmp = str(startswith) + ''.join(str(random.choice(range(1, 10))) for _ in range(length))
		if is_str:
			return tmp
		else:
			return int(tmp)

	@staticmethod
	def random_int_range(start, end, is_str=False, startswith=''):
		"""
		随机数字。传入数字的范围,范围包含end以数字类型return
		param start:
		:param end:
		:param is_str: 默认是数字,需要字符串的将此设置为True
		return:
		"""
		tmp = str(startswith) + ''.join(str(random.randint(start, end)))
		if is_str:
			return tmp
		else:
			return int(tmp)

	@staticmethod
	def random_chinese(length, startswith=''):
		"""
		随机汉字。传入汉字的长度
		param startswith:
		:param length:汉字的长度
		:return:字符串形式return
		"""
		chinese_list = ['用', '例', '描', '述', '完', '整', '比', '如', '步', '骤', '预', '期', '结', '果', '不', '缺', '失',
						'致', '界', '面', '描', '述', '无', '歧', '义', '比', '如', '预', '期', '跟', '以', '前', '一', '致',
						'与', '现', '一', '致', '有', '逻', '拆', '分', '粒', '度', '细', '辑', '一']
		str_ = ''
		for i in range(length):
			for j in chinese_list[random.randint(1, 48)]:
				# str +chr(random.randint (0x4E00,0X9FA5))
				str_ += ''.join(j)
		str_ = startswith + str_
		return str_

	@staticmethod
	def random_name():
		first_name = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '卫',
						'将', '沈', '韩', '杨', '朱', '秦', '何', '张', '孔', '曹']
		last_name = ['汗', '函', '类', '杰', '斌', '帅', '亮', '权', '飞', '备',
						'能', '才', '阿涵', '子媚', '呵', '克']
		name = ''.join((random.sample(first_name, k=1))) + ''.join(random.sample(last_name, k=1))
		return name[::1]

	@staticmethod
	def random_choice(list_):
		# first_name = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '卫',
		#               '将', '沈', '韩', '杨', '朱', '秦', '何', '张', '孔', '曹']
		# last_name = ['汗', '函', '类', '杰', '斌', '帅', '亮', '权', '飞', '备',
		#              '能', '才', '阿涵', '子媚', '呵', '克']
		# name = ''.join((random.sample(first_name, k=1))) + ''.join(random.sample(last_name, k=1))
		# return name[::1]
		return random.choice(list_)

	@staticmethod
	def random_strbypre(name):
		res_str = name.split(":")[0]
		num = int(name.split(":")[1])
		for i in range(num):
			res_str += "".join(random.choices(string.ascii_letters + string.digits))
		return res_str

	@staticmethod
	def random_allow(num):
		res_str = ""
		for i in range(num):
			res_str += "".join(random.choices(r"#&'()*+,-.:<=>?@[]()~"))
		return res_str

	@staticmethod
	def random_allow_material(num):
		res_str = ""
		for i in range(num):
			res_str += "".join(random.choices(r"&'()*+,-.:<=>?@[]_()~/"))
		return res_str

	@staticmethod
	def random_unallow(num):
		res_str = ""
		for i in range(num):
			res_str += "".join(random.choices(r"!/;"))
		return res_str

	@staticmethod
	def random_unallow_material(num):
		res_str = ""
		for i in range(num):
			res_str += "".join(random.choices(r"!%/;\^^"))
		return res_str

	@staticmethod
	def random_allow_pre(name):
		res_str = name.split(":")[0]
		num = int(name.split(":")[1])
		for i in range(num):
			res_str += "".join(random.choices(r"&'()++,-.:<=>?@[]_{)~"))
		return res_str

	@staticmethod
	def random_unallow_pre(name):
		res_str = name.split(":")[0]
		num = int(name.split(":")[1])
		for i in range(num):
			res_str += "".join(random.choices(r"!%/;\^"))
		return res_str

	@staticmethod
	def random_allow_material_pre(name):
		res_str = name.split(":")[0]
		num = int(name.split(":")[1])
		for i in range(num):
			res_str += "".join(random.choices(r"#&'()*+,-.:<=>?@[]{)~/"))
		return res_str

	@staticmethod
	def random_unallow_material_pre(name):
		res_str = name.split(":")[0]
		num = int(name.split(":")[1])
		for i in range(num):
			res_str += "".join(random.choices(r"!%/;\^"))
		return res_str


if __name__ == '__main__':
	r = RandomUtil
	a = r.random_string(8, startswith='UiTest-')
	b = r.random_phone()
	c = r.random_chinese(2)
	print(a, b, c)


