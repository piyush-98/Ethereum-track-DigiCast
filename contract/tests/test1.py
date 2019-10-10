import sys
from eosfactory.eosf import *
verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_WORKSPACE = sys.path[0] + "/../"
TOKEN_CONTRACT_WORKSPACE = sys.path[0] + "/../../eosio.token/"


def test():
    SCENARIO('''
    Execute all actions.
    ''')
    reset()
    create_master_account("eosio")

    #######################################################################################################
    
    COMMENT('''
    Create test accounts:
    ''')

    # test accounts and accounts where the smart contracts will be hosted
    create_account("alice", eosio, account_name="alice")
    create_account("dnftsaccount", eosio, account_name="dnftsaccount")
    create_account("eosiotoken", eosio, account_name="eosio.token")
    create_account("bob", eosio, account_name="bob")
    create_account("jas", eosio, account_name="jas")
    create_account("quillhash", eosio, account_name="quillhash")
    create_account("quillhash1", eosio, account_name="quillhash1")
    create_account("quillhash2", eosio, account_name="quillhash2")


    ########################################################################################################
    
    COMMENT('''
    Build and deploy token contract:
    ''')

    # creating token contract
    token_contract = Contract(eosiotoken, TOKEN_CONTRACT_WORKSPACE)
    token_contract.build(force=True)
    token_contract.deploy()

    ########################################################################################################
    
    COMMENT('''
    Build and deploy dnftsaccount contract:
    ''')

    # creating dnftsaccount contract
    contract = Contract(dnftsaccount, CONTRACT_WORKSPACE)
    contract.build(force=True)
    contract.deploy()

    ########################################################################################################
    
    COMMENT('''
    Create EOS tokens 
    ''')

    token_contract.push_action(
        "create",
        {
            "issuer": eosio,
            "maximum_supply": "1000000000.0000 EOS"
        },
        [eosiotoken]
    )


    ########################################################################################################

    COMMENT('''
    Issue EOS tokens to alice 
    ''')

    token_contract.push_action(
        "issue",
        {
            "to": alice,
            "quantity": "1000.0000 EOS",
            "memo": "issued tokens to alice"
        },
        [eosio]
    )

    COMMENT('''
    Issue EOS tokens to bob 
    ''')

    token_contract.push_action(
        "issue",
        {
            "to": bob,
            "quantity": "50.0000 EOS",
            "memo": "issued tokens to bob"
        },
        [eosio]
    )

########################################################################################################

    COMMENT('''
    Config the dnftsaccount
    ''')

    contract.push_action(
        "setconfig",
        {
            "version": "0.1"
        },
        [dnftsaccount]
    )

#####################################################################

    COMMENT('''
    Add validator quillhash
    ''')

    contract.push_action(
        "addvalidator",
        {
            "validator": quillhash,
            "email": "hello@quillhash.com",
            "category": "video"
        },
        [dnftsaccount]
    )

#####################################################################   

    # contract.push_action(
    #     "addvalidator",
    #     {
    #         "validator": quillhash1,
    #         "email": "hello@quillhash1.com",
    #         "category": "video"
    #     },
    #     [dnftsaccount]
    # )

    contract.push_action(
        "addvalidator",
        {
            "validator": quillhash1,
            "email": "hello@quillhash1.com",
            "category": "ebook"
        },
        [dnftsaccount]
    )

##################################################################

    contract.push_action(
        "addvalidator",
        {
            "validator": quillhash2,
            "email": "hello@quillhash2.com",
            "category": "video"
        },
        [dnftsaccount]
    )


    dnftsaccount.table("validators","dnftsaccount")
    dnftsaccount.table("categories","dnftsaccount")


########################################################################################################

    COMMENT('''
    Create the videoa token by jas
    ''')

    contract.push_action(
        "create",
        {
            "issuer": jas,
            "category": "video",
            "token_name": "videoa",
            "burnable": True,
            "base_uri": "15881.Harry_Potter_and_the_Chamber_of_Secrets",
            "span":"20",
            "origin_hash":"ca6b03344d8210b6c9f374f33d4119332e6b947329b35936ad4e902ac4d7c9e8",
        },
        [jas]
    )

    # COMMENT('''
    # Create the outlander ebook
    # ''')

    # contract.push_action(
    #     "create",
    #     {
    #         "issuer": alice,
    #         "category": "ebook",
    #         "token_name": "outlander",
    #         "burnable": True,
    #         "base_uri": "10964.Outlander",
    #         "span":"60",
    #         "origin_hash":"ca6b04424d8210b6c9f374f33d4119332e6b947329b35936ad4e902ac4d7c9e8",
    #         "validator_id":"1"
    #     },
    #     [alice]
    # )


    ########################################################################################################
    
    # set eosio.code permission to the contract
    dnftsaccount.set_account_permission(
        Permission.ACTIVE,
        {
            "threshold": 1,
            "keys": [
                {
                    "key": dnftsaccount.active(),
                    "weight": 1
                }
            ],
            "accounts":
            [
                {
                    "permission":
                        {
                            "actor": dnftsaccount,
                            "permission": "eosio.code"
                        },
                    "weight": 1
                }
            ]
        },
        Permission.OWNER,
        (dnftsaccount, Permission.OWNER)
    )
################################################################
    dnftsaccount.table("dnftstats","video")

    COMMENT('''
    Validates videoa creation by jas
    ''')

    contract.push_action(
        "validate",
        {
            "validator": quillhash,
            "category": "video",
            "token_name":"videoa"
        },
        [quillhash]
    )
    dnftsaccount.table("dnftstats","video")

    # COMMENT('''
    # Validates videoa creation by jas
    # ''')

    # contract.push_action(
    #     "validate",
    #     {
    #         "validator": quillhash1,
    #         "category": "video",
    #         "token_name":"videoa"
    #     },
    #     [quillhash1]
    # )

#####################################################################   

    COMMENT('''
    Issue videoa to jas
    ''')
    # 10% share issued to some singer say
    contract.push_action(
        "issue",
        {
            "to": jas,
            "category": "video",
            "token_name": "videoa",
            "quantity": "40.0000 PER",
            "memo": "na"
        },
        [jas]
    )

    dnftsaccount.table("dnftstats", "video")
    dnftsaccount.table("accounts", "jas")


    # COMMENT('''
    # Issue outlander to bob
    # ''')
    # # 20% share issued to some video-maker say
    # contract.push_action(
    #     "issue",
    #     {
    #         "to": bob,
    #         "category": ebook,
    #         "token_name": harrypotter,
    #         "quantity": "25.0000 PER",
    #         "memo": "na"
    #     },
    #     [bob]
    # )

########################################################################################################

# sale by any video token owner

    COMMENT('''
    Sale by jas
    ''')
    contract.push_action(
        "listsale",
        {
            "seller": jas,
            "category":"video",
            "token_name":"videoa",
            "percent_share": "5.0000 PER",
            "per_percent_amt": "50.0000 EOS",
            "expiration": "2019-10-29T00:00:00"
        },
        [jas]
    )

########################################################################################################

    COMMENT('''
    Bid by jas
    ''')
    contract.push_action(
        "startbid",
        {
            "seller": jas,
            "category":"video",
            "token_name":"videoa",
            "percent_share": "15.0000 PER",
            "base_price": "50.0000 EOS",
            "expiration": "2019-10-29T00:00:00"
        },
        [jas]
    )
    dnftsaccount.table("bids", "dnftsaccount")
    dnftsaccount.table("accounts", "dnftsaccount")
    
    dnftsaccount.table("lists", "dnftsaccount")
    eosiotoken.table("accounts", "alice")

###########################################################################

    COMMENT('''
    Invest in the listing  
    ''')
    eosiotoken.push_action(
        "transfer",
        {
            "from": alice,
            "to": dnftsaccount,
            "quantity": "50.0000 EOS",
            "memo": "0,jas"
        },
        permission=(alice, Permission.ACTIVE)
    )
    dnftsaccount.table("lists", "dnftsaccount")

###########################################################################

    COMMENT('''
    Invest in the biddings 
    ''')
    eosiotoken.push_action(
        "transfer",
        {
            "from": alice,
            "to": dnftsaccount,
            "quantity": "50.1000 EOS",
            "memo": "1,jas"
        },
        permission=(alice, Permission.ACTIVE)
    )

    dnftsaccount.table("bids", "dnftsaccount")

###########################################################################
    
    dnftsaccount.table("accounts", "alice")

    COMMENT('''
    Sale by alice (the investor)
    ''')
    contract.push_action(
        "listsale",
        {
            "seller": alice,
            "category":"video",
            "token_name":"videoa",
            "percent_share": "1.0000 PER",
            "per_percent_amt": "800.0000 EOS",
            "expiration": "2019-08-20T00:00:00"
        },
        [alice]
    )

####################################################

    COMMENT('''
    Close the videoa tokens sale
    ''')

    contract.push_action(
        "closesale",
        {
            "seller": jas,
            "sale_id": 0
        },
        [jas]
    )

####################################################

    dnftsaccount.table("accounts", "dnftsaccount")

    eosiotoken.table("accounts", "dnftsaccount")

    COMMENT('''
    Close the videoa tokens bidding
    ''')

    contract.push_action(
        "closebid",
        {
            "seller": jas,
            "sale_id": 1
        },
        [jas]
    )
####################################################

    COMMENT('''
    Burn the videoa tokens
    ''')

    contract.push_action(
        "burn",
        {
            "owner": jas,
            "category": "video",
            "token_name":"videoa",
            "quantity":"0.0010 PER"
        },
        [jas]
    )
####################################################

    COMMENT('''
    Delete the validator 
    ''')
    contract.push_action(
        "delvalidator",
        {
            "validator": quillhash2,
        },
        [dnftsaccount]
    )

####################################################################
    COMMENT('''
    Tables dnft
    ''')

    dnftsaccount.table("owners","0")
    dnftsaccount.table("owners","1")

    dnftsaccount.table("lists", "dnftsaccount")

    dnftsaccount.table("accounts", "alice")
    dnftsaccount.table("accounts", "bob")

    eosiotoken.table("accounts", "alice")
    eosiotoken.table("accounts", "bob")
    eosiotoken.table("accounts", "eosio.token")

    eosiotoken.table("accounts", "dnftsaccount")
    eosiotoken.table("stat", "EOS")
    dnftsaccount.table("dnftstats","video")
    dnftsaccount.table("accounts", "dnftsaccount")

    stop()

if __name__ == "__main__":
    test()
