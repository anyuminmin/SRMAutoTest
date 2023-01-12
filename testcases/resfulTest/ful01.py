#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:yumin An
from flask import make_response,jsonify,Flask
from flask_restful import Resource,Api,reqparse

app=Flask(__name__)
api=Api(app=app)

class LoginView(Resource):
	def get(self):
		return jsonify({'status':0,'msg':'ok','data':''})

	def post(self):
		parser=reqparse.RequestParser()
		parser.add_argument('username',type=str,required=True,help='您的用户名参数不能为空')
		parser.add_argument('password',type=str)
		parser.add_argument('yzCode',type=int,help='验证码必须是整数')
		return jsonify({'status':0,'msg':'ok','data':parser.parse_args()})

api.add_resource(LoginView,'/login',endpoint='login') #请求地址：http://127.0.0.1:5000/login
if __name__ == '__main__':
	app.run(debug=True)