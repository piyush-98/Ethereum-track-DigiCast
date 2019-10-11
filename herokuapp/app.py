from flask import Flask
app = Flask(__name__)

# /home/jaspreet/.local/lib/python3.6/site-packages
# Reference:https://github.com/EvaCoop/eosjs_python

import requests
import json

# payload = "{\"block_num_or_id\":\"500000\"}"

headers = {
    'accept': "application/json",
    'content-type': "application/json"
    }

def get_table(contractName,tableName,scope):
	url = "https://jungle2.cryptolions.io:443/v1/chain/get_table_rows"
	payload = "{\"code\":\""+contractName+"\",\"table\":\""+tableName+"\",\"scope\":\""+scope+"\",\"index_position\":\"primary\",\"json\":\"true\"}"
	response = requests.request("POST", url, data=payload, headers=headers)
	return response.text	

def get_accPublickey(_accname):
	url = "http://jungle.eoscafeblock.com:8888/v1/chain/get_account"
	payload = "{\"account_name\":\""+_accname+"\"}"
	response = requests.request("POST", url, data=payload, headers=headers)
	pub = json.loads(response.text)
	return pub['permissions'][1]['required_auth']['keys'][0]['key']

from eosjs_python import Eos

jaseos = Eos({
	'http_address': 'https://jungle2.cryptolions.io:443',
	'key_provider': '5JPwrk36HBiHq1YY1Vhpp9JQifQ6biki3mVejV9HFWSkAKdgK8U',
    'chain_id': '1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f'
})   


piyushtester = Eos({
	'http_address': 'https://jungle2.cryptolions.io:443',
	'key_provider': '5HqWmHV449uUePaDm9QWXxsftkHkrzpiHxYsvNjkSddbe64jfKz',
    'chain_id': '1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f'
})   


dnfteos = Eos({
	'http_address': 'https://jungle2.cryptolions.io:443',
	'key_provider': '5JmZQh9AHvjR8HLVCcqBgCa8p44JNEYzUzyTLJD2FwZi3nbWaBS',
    'chain_id': '1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f'
})   

vidvalidatoreos = Eos({
	'http_address': 'https://jungle2.cryptolions.io:443',
	'key_provider': '5Hrt8MPM2SWVPUXDskw3v2pS2x6QThL5ipiLdXEmYEMvTqCnNrG',
    'chain_id': '1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f'
})   



# signedin=False
# signinacc = piyushtester # let piyushtester be liquid acc
# signedinaccName = 'bobzeptagram'


def createacct(_name):
	key_pair = Eos.generate_key_pair()
	piyushtester.newaccount({
		'creator': 'piyushtester',
		'name': _name,
		'owner_public_key': key_pair["public"],
		'active_public_key': key_pair["public"],
		'buyrambytes_bytes': 4000,
		'delegatebw_stake_net_quantity': '1.0000 EOS',
		'delegatebw_stake_cpu_quantity': '1.0000 EOS',
		'delegatebw_transfer': 0
	})
	return key_pair

def signin(_name,_pk):
	signineos = Eos({
		'http_address': 'https://jungle2.cryptolions.io:443',
		'key_provider': _pk,
		'chain_id': '1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f'
	})
	# global signedin,signedinaccName
	# signedin=True
	# signedinaccName=_name
	# global signinacc 
	# signinacc=signineos


def transferVID(_from,_to,_quantity,signer):
  signer.push_transaction('dnfttoken123','transfer',_from,'active',{
	"from":_from,
	"to":_to,
	"quantity":_quantity,
	"memo":""})




# for mailing
# import codecs
# from email.mime.multipart import MIMEMultipart 
# from email.mime.text import MIMEText 
# from email.mime.base import MIMEBase 
# from email import encoders
# import smtplib 

# def check_sum(filename):
#     import hashlib
#     #filename =r'data.json'
#     with open(filename,"rb") as f:
#         bytes = f.read() # read entire file as bytes
#         readable_hash = hashlib.sha256(bytes).hexdigest()
#         return readable_hash

# def json_make(_from, mailid, _videoname, link, signer):
#     data={}
#     #data['data']=[]
#     data['data']=({'accname':_from,'vidname':_videoname,'link':link})
#     filename=r'data.json'
#     with open(filename, 'w') as outfile:
#         json.dump(data, outfile)
    # Python code to illustrate Sending mail from  
    # your Gmail account
    # msg = MIMEMultipart()
    # f = codecs.open(filename, "r", "utf-8")
    # attachment = MIMEText(f.read())
    # attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    # msg.attach(attachment)
    # #p = MIMEBase('application', 'octet-stream') 
    # s = smtplib.SMTP('smtp.gmail.com', 587)  
    # s.starttls()
    # s.login("arjunguptaa98@gmail.com", "piyush@1234") 
    # #message = "Message_you_need_to_send"
    # s.sendmail("arjunguptaa98@gmail.com", mailid, msg.as_string()) 

    # # terminating the session 

    # s.quit()
    # hash = check_sum(filename)
    # print(hash)
    # return hash

def validate(_token_name, signer):
  signer.push_transaction('dnftversion1','validate',"vidvalidator",'active',{
	"validator":"vidvalidator",
	"category":"video",
	"token_name":_token_name})

def issue(authority, to, _token_name, quantity,signer):
  signer.push_transaction('dnftversion1','issue',authority,'active',{
	"to":to,
	"category":"video",
	"token_name":_token_name,
	"quantity":quantity+".0000 PER",
	"memo":"issuing"})



# # #from = eos acc name
# # # mailid = id of google signed in user
# # # videoname= small name
# # # link = youtube link
# # def createVTO(_from, mailid, _videoname, link, signer):

# #   hash = json_make(_from, mailid, _videoname, link, signer)
# #   signer.push_transaction('dnftversion1','create',_from,'active',{
# # 	"issuer":_from,
# # 	"category":"video",
# # 	"token_name":_videoname,
# # 	"burnable":True,
# # 	"base_uri":link,
# # 	"span":"10",
# # 	"origin_hash":hash
# # 	})
# #   # validate directly for now 
# #   validate(_videoname,vidvalidatoreos)
# #   # issue directly 100 PERs to creator
# #   issue(_from, _from, _videoname, "100",signinacc)



# # def startsale(seller, _videoname, percent_shares, per_percent_amt, signer):

# #   signer.push_transaction('dnftversion1','listsale',seller,'active',{
# # 	"seller":seller,
# # 	"category":"video",
# # 	"token_name":_videoname,
# # 	"percent_share":percent_shares+ '.0000 PER',
# # 	"per_percent_amt":per_percent_amt+'.0000 VID',
# # 	"expiration":"2019-10-30T00:00:00"})


# # def invest(_from, quantity, sale_id, seller, signer):

# #   signer.push_transaction('dnfttoken123','transfer',_from,'active',{
# # 	"from":_from,
# # 	"to":"dnftversion1",
# # 	"quantity":quantity+ '.0000 VID',
# # 	"memo":sale_id+','+seller
# # 	})



# #dnftversion1

# #1. Create new acct, save acct name, keys and popup

# # nk=createacct("alicetestinl")	
# # print(nk)

# # #2. Sign in through acct name and 2nd key
# # signin("alicetestinp","5Hyva2T2Rm9wQ9TdGgMDeBt757VW8T4gcwzb25QwFVZRyTSn7rj")

# # # #get sign in details
# # info = get_accPublickey(signedinaccName)
# # print(info)


# # #give 100 VID = 100 Rs. signup bonus
# # transferVID("dnfttoken123",signedinaccName,"100.0000 VID",dnfteos)

# # #3. craete VTO, give mailid, vidname, youtube link
# # createVTO(signedinaccName,"jsk1961998@gmail.com","bvpjs","youtube.com/bvpjs",signinacc)

# # # # My Video page
# print("MY VIDEO PAGE",end='\n')
# result = get_table("dnftversion1","accounts",signedinaccName)
# print(result)

# # # #4. start sale give vidname, percent share and per percent amt
# # startsale(signedinaccName,"bvpjs","51","1",signinacc)

# # # #Hot offerings page
# # print("HOT OFFERINGS PAGE",end='\n')
# # result = get_table("dnftversion1","lists","dnftversion1")
# # print(result)

# # transferVID("dnfttoken123","piyushtester","100.0000 VID",dnfteos)

# # # #5, any other user from other pc should be able to invest
# # # # take investment amt 10 VID
# # invest('piyushtester',"10", "3", "alicetestinp",piyushtester)

# # # # My Video page
# # print("MY VIDEO PAGE",end='\n')
# # result = get_table("dnftversion1","accounts","piyushtester")
# # print(result)






@app.route('/create_acc/<_name>')
def createacct(_name):
	key_pair = Eos.generate_key_pair()
	piyushtester.newaccount({
		'creator': 'piyushtester',
		'name': _name,
		'owner_public_key': key_pair["public"],
		'active_public_key': key_pair["public"],
		'buyrambytes_bytes': 4000,
		'delegatebw_stake_net_quantity': '1.0000 EOS',
		'delegatebw_stake_cpu_quantity': '1.0000 EOS',
		'delegatebw_transfer': 0
	})
	return key_pair

@app.route('/videopage/<accname>')
def videopage(accname):
    result = get_table("dnftversion1","accounts",accname)
    result=json.loads(result)
    return str(result['rows'][0]["amount"])[:2]

@app.route('/videoname/<accname>')
def videopage1(accname):
  result = (get_table("dnftversion1","accounts",accname))
  result=json.loads(result)
  return str(result['rows'][0]["dnft_id"])

@app.route('/allsales')
def allsales():
    result = get_table("dnftversion1","lists","dnftversion1")
    return result



@app.route('/signin/<_name>/<pk>')
def signin(_name,_pk):
	signineos = Eos({
		'http_address': 'https://jungle2.cryptolions.io:443',
		'key_provider': _pk,
		'chain_id': '1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f'
	})
	# global signedin,signedinaccName
	# signedin=True
	# signedinaccName=_name
	# global signinacc
	# signinacc=signineos

@app.route('/create_VTO/<_from>/<mailid>/<_videoname>/<link>/<pk>')
def createVTO(_from, mailid, _videoname, link, pk):

  signer = Eos({
		'http_address': 'https://jungle2.cryptolions.io:443',
		'key_provider': pk,
		'chain_id': '1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f'
	})
#   hash = json_make(_from, mailid, _videoname, link, signer)
  signer.push_transaction('dnftversion1','create',_from,'active',{
		"issuer":_from,
		"category":"video",
		"token_name":_videoname,
		"burnable":True,
		"base_uri":link,
		"span":"10",
		"origin_hash":'883fd863b6583fe91620653f2dfcad192d69340f6024c958e7d63a4f414d5cdb'
		})
	# validate directly for now 
  validate(_videoname,vidvalidatoreos)
	# issue directly 100 PERs to creator
  issue(_from, _from, _videoname, "100", signer)
  return "good job buddy"

@app.route('/start_sale/<seller>/<_videoname>/<percent_shares>/<per_percent_amt>/<pk>')
def startsale(seller, _videoname, percent_shares, per_percent_amt, pk):

  signer = Eos({
		'http_address': 'https://jungle2.cryptolions.io:443',
		'key_provider': pk,
		'chain_id': '1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f'
	})

  signer.push_transaction('dnftversion1','listsale',seller,'active',{
	"seller":seller,
	"category":"video",
	"token_name":_videoname,
	"percent_share":percent_shares+ '.0000 PER',
	"per_percent_amt":per_percent_amt+'.0000 VID',
	"expiration":"2019-10-30T00:00:00"})
  return "done this also"



@app.route('/invest/<_from>/<quantity>/<sale_id>/<seller>/<pk>')
def invest(_from, quantity, sale_id, seller, pk):

  signer = Eos({
		'http_address': 'https://jungle2.cryptolions.io:443',
		'key_provider': pk,
		'chain_id': '1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f'
	})

  signer.push_transaction('dnfttoken123','transfer',_from,'active',{
	"from":_from,
	"to":"dnftversion1",
	"quantity":quantity+ '.0000 VID',
	"memo":sale_id+','+seller
	})
  return 'aray wah'

if __name__ == '__main__':
   app.run(debug = True)

