# coding: utf-8
from weibo import APIClient

#! /usr/bin/python
import time
PAGE_SIZE = 200

def print_users_list(ul):
        """
        打印用户列表的详细信息
        """
	index = 0
	for user in ul:
		uid = user["id"]
		ugen = user["gender"]
		uname = user["screen_name"]
		udesc = user["description"]
		print "%-6d%-12d%-3s%s%s" % (index, uid, ugen, uname.ljust(20), udesc.ljust(40))
		index += 1

def get_friends(client, uid=None, maxlen=0):
        """
        读取uid用户的关注用户列表，默认uid=None，此时uid赋值为client.uid，而client.uid表示的是当前授权用户的uid.
        """
	if not uid:
		uid = client.uid
	return get_users(client, False, uid, maxlen)

def get_followers(client, uid=None, maxlen=0):
        """
        读取uid用户的粉丝列表，默认uid=None，此时uid赋值为client.uid，而client.uid表示的是当前授权用户的uid.
        """
	if not uid:
		uid = client.uid
	return get_users(client, True, uid, maxlen)

def get_users(client, followersorfriends, uid, maxlen):
        """
        调用API读取uid用户的关注用户列表或者粉丝列表，followersorfriends为True读取粉丝列表，为False读取关注好友列表，
        参数maxlen设置要获取的好友列表的最大长度，为0表示没有设置最大长度，此时会尝试读取整个好友列表，但是API对于读取的
        好友列表的长度会有限制，测试等级最大只能获取一个用户的5000条好友信息。
        """
	fl = []
	next_cursor = 0
	while True:
		if followersorfriends:
			raw_fl = client.friendships.followers.get(uid=uid, cursor=next_cursor, count=PAGE_SIZE)
		else:
			raw_fl = client.friendships.friends.get(uid=uid, cursor=next_cursor, count=PAGE_SIZE)
		fl.extend(raw_fl["users"])
		next_cursor = raw_fl["next_cursor"]
		if not next_cursor:
			break
		if maxlen and len(fl) >= maxlen:
			break
		time.sleep(1)
	return fl

if __name__ == '__main__':
	APP_KEY = '219***1020'            # app key
	APP_SECRET = '60b318************21010f777a77328'      # app secret
	CALLBACK_URL = 'http://cshuo.sinaapp.com/'  # callback url

	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	url = client.get_authorize_url()
	print "auth_url : " + url

	code = raw_input("input the retured code : ")
	r = client.request_access_token(code)
	access_token = r.access_token # 新浪返回的token，类似abc123xyz456
	expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
	# TODO: 在此可保存access token
	client.set_access_token(access_token, expires_in)

	fl = get_followers(client,uid=2411802345, maxlen=100)
	print_users_list(fl)
