#!/usr/bin/env python
#-*-coding:utf-8-*-

import requests,re,sys,csv

city = {}	#Template: city['浙江省'] = {'杭州':'url1','宁波':'url2'}
province = [] 
home_url = 'http://www.jihaoba.com'
phone_numbers = []
filtered_phone_numbers = []

def welcome():
	print('''##########################################################################################
#      __  __               ______                                      _                #
#    |  \/  |             |  ____|                                    | |                #
#    | \  / |_ __  _ __   | |__   _ __  _   _ _ __ ___   ___ _ __ __ _| |_ ___  _ __     #
#    | |\/| | '_ \| '_ \  |  __| | '_ \| | | | '_ ` _ \ / _ | '__/ _` | __/ _ \| '__|    #
#    | |  | | |_) | | | | | |____| | | | |_| | | | | | |  __| | | (_| | || (_) | |       #
#    |_|  |_| .__/|_| |_| |______|_| |_|\__,_|_| |_| |_|\___|_|  \__,_|\__\___/|_|       #
#           | |                                                                          #
#           |_|                                                                          #
#                                                                                        #
#     Welcome to Mobile Phone Number Enumerator! ..................                      #
#     作者: Dubh3                                                                        #
#     Email: dubh3@qq.com                                                                #
#     说明: 使用本脚本可以枚举生成指定地区指定号段的所有手机号码                         #
#     注意：禁止使用本脚本用于非法用途，造成的一切后果与本人无关                         #
#                                                                                        #''')

# 初始化，从云端获取所有省市及其对应号段访问的URL
def init():
	print('#  正在同步各地区数据...')
	global city
	global province
	url = home_url + '/tools/haoduan/'
	response = requests.get(url)
	province = re.findall(r'<div class="hd_mar">.+?<p><span>(.+?)：</span></p>',response.text,re.S)[3:]
	tmp = re.findall(r'<div class="hd_number1">(.+?)<div class="clear">',response.text,re.S)
	i = 0
	for str in tmp:
		city_tmp = {}
		city_url = re.findall(r'<a href="(.+?)" target="_blank">',str)
		if city_url[0] == '/haoduan/beijing/':
			city_name = re.findall(r'target="_blank">(.+?)</a>',str)
		else:
			city_name = re.findall(r'<font color=".+?>(.+?)</font>',str)
		for j in range(0,len(city_name)):
			city_tmp[city_name[j]] = city_url[j]
		city[province[i]] = city_tmp
		i += 1
	print('#  同步完成!')

# 获取指定或全部号段的所有手机号码
def getNumberSection(name,url,hd,all):
	code = re.findall(r'/haoduan/(.+?)/',url)[0]
	url = home_url + url
	response = requests.get(url)
	hd_tmp = re.findall(r'<div class="hd_number">(.+?)<div class="clear">',response.text,re.S)[:4]
	hds = []
	for str in hd_tmp:
		tmp = re.findall(r' <a href=".+?">'+name+r'(.+?)</a>',str)
		for i in tmp:
			hds.append(i)
	hd_exist_flag = False

	if all:
		print('#  开始获取 '+name+' 地区所有号码...')
		for i in hds:
			url = 'http://www.jihaoba.com/haoduan/'+i+'/'+code+'.htm'
			response = requests.get(url)
			complete_hds = re.findall(r'title="'+name+r'\d+?号段">(.+?)</a></li>',response.text)
			for j in  complete_hds:
				url = 'http://www.jihaoba.com/haoduan/'+code+'/'+j+'.htm'
				response = requests.get(url)
				numbers_tmp = re.findall(r'<textarea name="textarea" cols="91" rows="10">(.+?)</textarea>',response.text,re.S)[0]
				numbers_tmp = re.findall(r'(\d+?)\s+?',numbers_tmp)
				for i in numbers_tmp:
					phone_numbers.append(i)
		print('#  所有号码获取成功！')
	else:
		for i in hds:
			if i == hd[:3]:
				hd_exist_flag = True
				break
		if hd_exist_flag:
			print('#  开始获取 '+name+' 地区号段为 '+hd+' 的所有号码...')
			url = 'http://www.jihaoba.com/haoduan/'+hd[:4]+'/'+code+'.htm'
			response = requests.get(url)
			hds = re.findall(r'title="'+name+r'\d+?号段">(.+?)</a></li>',response.text)
			if len(hd) > 3:
				for i in hds:
					if hd == i[:len(hd)]:
						url = 'http://www.jihaoba.com/haoduan/'+code+'/'+i+'.htm'
						response = requests.get(url)
						numbers_tmp = re.findall(r'<textarea name="textarea" cols="91" rows="10">(.+?)</textarea>',response.text,re.S)[0]
						numbers_tmp = re.findall(r'(\d+?)\s+?',numbers_tmp)
						for i in numbers_tmp:
							phone_numbers.append(i)
				print('#  所有指定号段号码获取成功!')
			else:
				for i in hds:
					url = 'http://www.jihaoba.com/haoduan/'+code+'/'+i+'.htm'
					response = requests.get(url)
					numbers_tmp = re.findall(r'<textarea name="textarea" cols="91" rows="10">(.+?)</textarea>',response.text,re.S)[0]
					numbers_tmp = re.findall(r'(\d+?)\s+?',numbers_tmp)
					for i in numbers_tmp:
						phone_numbers.append(i)
				print('#  所有指定号段号码获取成功!')
		else:
			print('#  该号码段不存在！')
			exit(1)


def main():
	global phone_numbers
	global filtered_phone_numbers
	welcome()
	print('******************************************************************************************')
	init()
	exit_flag = False
	location = None
	location_url = None
	while 1:
		location = input('#  号码归属地：')
		if location == "":
			print('#  输入不能为空,请重新输入!')
			continue
		for key in city:
			if exit_flag:
				break
			for key2 in city[key]:
				if exit_flag:
					break
				if key2 == location:
					location_url = city[key][key2]
					exit_flag = True
					break
		if exit_flag:
			break
		else:
			print('#  归属地不存在,请重新输入!')

	while 1:
		hd_prefix = input('#  号段前缀(3-7位)(不填则默认获取所有号段号码)：')
		if hd_prefix == '':
			break
		if len(hd_prefix) < 3 or len(hd_prefix) > 7:
			print('#  号段前缀需大于3位小于7位，请重新输入！')
		else:
			break

	while 1:
		hd_suffix = input('#  号段后缀(1-4位)(不填则默认获取所有号段号码)：')
		if hd_suffix == '':
			break
		if len(hd_suffix) > 4:
			print('#  号段后缀需小于4位，请重新输入！')
		else:
			break

	if len(hd_prefix) >= 3:
		getNumberSection(location,location_url,hd_prefix,False)
	else:
		getNumberSection(location,location_url,None,True)


	if len(hd_suffix) > 0:
		print('#  正在筛选号码后缀为 '+hd_suffix+' 的所有号码...')
		
		for k in phone_numbers:
			if hd_suffix == k[:-(len(hd_suffix)+1):-1][::-1]:
				filtered_phone_numbers.append(k)
		'''
		for i in range(len(phone_numbers)):
			nb = phone_numbers[i]
			if hd_suffix == nb[:-(len(hd_suffix)+1):-1][::-1]:
				filtered_phone_numbers.append(nb)
		print('#  筛选完成!')
		'''
	else:
		filtered_phone_numbers = phone_numbers

	print('#  正在生成csv文件...')
	with open('phones.csv','w',newline='') as myFile:
	    myWriter=csv.writer(myFile)
	    myWriter.writerow(['姓名','电话'])
	    count = 1
	    for i in filtered_phone_numbers:
	    	myWriter.writerow([count,i])
	    	count += 1

	print('#  文件生成成功!')
	print('#  共 '+str(len(filtered_phone_numbers))+' 个号码.')

if __name__ == '__main__':
	main()