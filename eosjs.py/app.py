from flask import Flask
app = Flask(__name__)

@app.route('/create_acc/<_name>')
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

@app.route('/videopage/<accname>')
def videopage(accname):
    result = get_table("dnftversion1","accounts",accName)
    return result

@app.route('/allsales/')
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
	global signedin,signedinaccName
	signedin=True
	signedinaccName=_name
	global signinacc
	signinacc=signineos

@app.route('/create_VTO/<_from>/<mailid>/<_videoname>/<link>/<pk>')
def createVTO(_from, mailid, _videoname, link, signer):

  hash = json_make(_from, mailid, _videoname, link, signer)
  signer.push_transaction('dnftversion1','create',_from,'active',{
	"issuer":_from,
	"category":"video",
	"token_name":_videoname,
	"burnable":1,
	"base_uri":link,
	"span":"10",
	"origin_hash":hash})

@app.route('/start_sale/<seller>/<_videoname>/<percent_shares>/<per_percent_amt><pk>')
def startsale(seller, _videoname, percent_shares, per_percent_amt, signer):

  signer.push_transaction('dnftversion1','listsale',seller,'active',{
	"seller":seller,
	"category":"video",
	"token_name":_videoname,
	"percent_share":percent_shares+ '.0000 PER',
	"per_percent_amt":per_percent_amt+'.0000 VID',
	"expiration":"2019-10-30T00:00:00"})



@app.route('/invest/<_from>/<quantity>/<sale_id>/<seller>/<pk>')
def invest(_from, quantity, sale_id, seller, signer):

  signer.push_transaction('dnfttoken123','transfer',_from,'active',{
	"from":_from,
	"to":"dnftversion1",
	"quantity":quantity+ '.0000 VID',
	"memo":sale_id+','+seller
	})

if __name__ == '__main__':
   app.run(debug = True)
