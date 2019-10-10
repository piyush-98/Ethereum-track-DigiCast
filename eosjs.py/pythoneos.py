# /home/jaspreet/.local/lib/python3.6/site-packages
# Reference:https://github.com/EvaCoop/eosjs_python

import requests
import json

#payload = "{\"block_num_or_id\":\"500000\"}"

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

signedin=False
signinacc = piyushtester # let piyushtester be liquid acc
signedinaccName = 'bobzeptagram'


def createacct(_name):
	key_pair = Eos.generate_key_pair()
	jaseos.newaccount({
		'creator': 'jasthetester',
		'name': _name,
		'owner_public_key': key_pair["public"],
		'active_public_key': key_pair["public"],
		'buyrambytes_bytes': 2000,
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
	global signedin,signedinaccName
	signedin=True
	signedinaccName=_name
	global signinacc 
	signinacc=signineos


def transferVID(_from,_to,_quantity,signer):
  signer.push_transaction('dnfttoken123','transfer',_from,'active',{
	"from":_from,
	"to":_to,
	"quantity":_quantity,
	"memo":""})




# for mailing
import json
import codecs
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import smtplib 

def check_sum(filename):
    import hashlib
    #filename =r'data.json'
    with open(filename,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()
        return readable_hash

def json_make(_from, mailid, _videoname, link, signer):
    data={}
    #data['data']=[]
    data['data']=({'accname':_from,'vidname':_videoname,'link':link})
    filename=r'data.json'
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
    # Python code to illustrate Sending mail from  
    # your Gmail account
    msg = MIMEMultipart()
    f = codecs.open(filename, "r", "utf-8")
    attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attachment)
    #p = MIMEBase('application', 'octet-stream') 
    s = smtplib.SMTP('smtp.gmail.com', 587)  
    s.starttls()
    s.login("arjunguptaa98@gmail.com", "piyush@1234") 
    #message = "Message_you_need_to_send"
    s.sendmail("arjunguptaa98@gmail.com", mailid, msg.as_string()) 

    # terminating the session 

    s.quit()
    hash = check_sum(filename)
    return hash


#from = eos acc name
# mailid = id of google signed in user
# videoname= small name
# link = youtube link
def createMTO(_from, mailid, _videoname, link, signer):

  hash = json_make(_from, mailid, _videoname, link, signer)
  signer.push_transaction('dnftversion1','create',_from,'active',{
	"issuer":_from,
	"category":"video",
	"token_name":_videoname,
	"burnable":1,
	"base_uri":link,
	"span":"10",
	"origin_hash":hash})

#dnftversion1

#1. Create new acct, save acct name, keys and popup

nk=createacct("alicetesting")	
print(nk)

#2. Sign in through acct name and 2nd key
signin("alicetesting","5JCUiyyjjaGxWoNNyAnPYA6FTmAqEjSs9Jw5dkXpPMkTpaZzhvA")

#get sign in details
# info = get_accPublickey(signedinaccName)
# print(info)

#View table
# result = get_table("zeptagram123","stat","ZPT")
# print(result)

# transferVID("dnfttoken123","piyushtester","2.0001 VID",dnfteos)

#3. give mailid, vidname, youtube link
createMTO(signedinaccName,"mailid","vidname","link",signinacc)