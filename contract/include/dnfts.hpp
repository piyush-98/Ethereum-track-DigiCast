/**
 *  dNFTs (Distributed Non Fungible Tokens)
 *  (C) 2019 by Quillhash [ http://quillhash.com ]
 *
 *  A simple standard for digital assets that requires shared ownership on NFTs for EOSIO blockchains
 *
 *    GitHub:         https://github.com/Quillhash/dnfts 
 *    Presentation:   https://medium.com/quillhash/partial-ownership-on-eos-773aea600e3
 *
*/

#pragma once

#include <eosio/asset.hpp>
#include <eosio/symbol.hpp>
#include <eosio/eosio.hpp>
#include <eosio/time.hpp>
#include <eosio/transaction.hpp>
#include <eosio/system.hpp>
#include <eosio/singleton.hpp>
#include "utility.hpp"

using namespace std;
using namespace eosio;
using namespace utility;

CONTRACT dnfts: public contract {
	
    public:
        using contract::contract;

        /*
        defines the 100% total current supply of any NFT
        * PER acts as a stable token to denote percentage of ownership.
        * Token_name : PER
        * Precision: 4
        */ 
        const asset PER = asset( 1000000, symbol("PER", 4 )); 

        // defines the 30 days in seconds
        const int MONTH_SEC = 3600*24*30;

        /*
        Defines the ram_payer for all the actions (except create) in contract
        true-> contract account pays for all RAM actions
        */ 
        const bool CONTRACT_PAYER = true;

        dnfts(name receiver, name code, datastream<const char*> ds)
            : contract(receiver, code, ds) {}

        /* 
        Update version of this contract deployment for external marketplaces, wallets etc
        */
        ACTION setconfig(string version);


        /*
        * Adds the validator to the contract for each category 
        * Callable by contract account (_self).
        *
        * validator - account name to be allowed to validate 
        * mail - real life mail id of the validator
        * category - category allowed to validate 
        */
        ACTION addvalidator(name validator,
                            string email,
                            name category);


        /*
        * New registration of NFT. The information and consent of creating NFT is provided
        * to display info about the NFT, and get it validated by validators
        * Atleast 2 vallidators must exist for the category created.
        *
        * issuer - account name for issuer
        * category - category_name for hierarchy, eg. video, music, ebook, article, photography etc.
        * token_name - unique token_name for each digital asset (NFT)
        * burnable - specify if NFT ownership can be burnt or not
        * base_uri - URI for the digital asset NFT
        * span - Time duration for which the ownership remains existent to the investors
        * origin_hash - checksum256 hash of the JSON file that needs to be mailed to the validators
        * validator_id - validator_id for the validator selected manually. 
        */
        ACTION create(name issuer,
                        name category,
                        name token_name,
                        bool burnable,
                        string base_uri,
                        uint8_t span,
                        checksum256 origin_hash);


        /*
        * validate the creation of NFT if either chosen by token creator 
        * or randomly chosen by the contract
        * 
        * validator - account name of the validator verifying the NFT and its owner through mail in real-world
        * category - category of token being validated
        * token_name - token_name being validated
        */
        ACTION validate(name validator, 
                        name category, 
                        name token_name);

        /*
        * Issue NFTs ownership to the required authorities if required. May issue 100% to creator itself 
        * Callable by creator of the NFT after being validated.
        *
        * to - account name to whom token is being issued
        * category - category_name for hierarchy, eg. video, music, ebook, article, photography etc.
        * token_name - unique token_name for each digital asset (NFT)
        * quantity - to be specified with symbol "PER" within range 0 < quantity <= 100 PER; denotes percentage through stable token PER
        * memo - memo for NFT ownership being issued to issuer
        */
        ACTION issue(name to,
                        name category,
                        name token_name,
                        asset quantity,
                        string memo);

        /*
        * allows the burn of ownership shares by owner if allowed during the creation.
        * 
        * owner - account name of the owner who has token shares
        * category - category_name of token being burnt
        * token_name - unique token_name for each digital asset (NFT)
        * quantity - to be specified with symbol "PER" within range of owner's holding
        * if all PERs are burnt, the NFT is removed from the blockchain
        */
        ACTION burn(name owner,
                    name category,
                    name token_name,
                    asset quantity);


        /*
        * Transfer NFTs ownership from one account to another 
        * Callable by any current owner of the NFT.
        *
        * from - account name of the owner sending the shares of any NFT.
        * to - account name to which transfer is being made.
        * category - category_name for hierarchy, eg. video, music, ebook, article, photography etc.
        * token_name - unique token_name for each digital asset (NFT)
        * percent_share - to be specified with symbol "PER" within range of owner's holding
        * memo - memo for NFT ownership being transferred.
        */
        ACTION transfer(name from,
                        name to,
                        name category,
                        name token_name,
                        asset percent_share,
                        string memo);


        /*
        * List the sale of NFTs ownership 
        * Callable by any current owner of the NFT.
        *
        * seller - account name of the owner selling the shares of any NFT.
        * category - category_name for token 
        * token_name - unique token_name for each digital asset (NFT)
        * percent_share - to be specified with symbol "PER" within range of owner's holding that needs to be sold
        * per_percent_amt - Each percent of share price in EOS. This is decided by seller according to the market.
        * expiration - Provided in format YYYY-MM-DD or <YYYY-MM-DD>T<HH:MM:SS>
        * After expiration time, sale listing is removed. 
        * For contract as RAM_PAYER, maximum allowed expiration is within 1 month.
        * 
        * listsale allows seller to distribute listed ownership to multiple investors. It remains alive for 1 week
        * It is to quickly distribute the ownership to multiple investors. 
        */
        ACTION listsale(name seller,
                        name category,
                        name token_name,
                        asset percent_share,
                        asset per_percent_amt,
                        time_point_sec expiration);


        /*
        * Start the bidding of NFTs ownership 
        * Callable by any current owner of the NFT.
        *
        * seller - account name of the owner bidding the shares of any NFT.
        * category - category_name for token 
        * token_name - unique token_name for each digital asset (NFT)
        * percent_share - to be specified with symbol "PER" within range of owner's holding that shall be bid upon.
        * base_price - Base price of the shares in EOS. Bidders bid upon the base price and raise their bid.                                 
        * expiration - Provided in format YYYY-MM-DD or <YYYY-MM-DD>T<HH:MM:SS>
        * After expiration time, bid listing is removed considering it successfull. 
        * For contract as RAM_PAYER, maximum allowed expiration is within 1 month.
        * 
        * listsale allows seller to distribute listed ownership to multiple investors. It remains alive for 1 week
        * It is to quickly distribute the ownership to multiple investors. 
        */
        ACTION startbid(name seller,
                        name category,
                        name token_name,
                        asset percent_share,
                        asset base_price,
                        time_point_sec expiration);


        /*
        * Whenever "eosio.token" contract sends EOS for buying from the sellings listed. 
        * Callable by anyone transferring the EOS.
        *
        * from - account name to whom token is being issued
        * to - account name of contract being deployed to
        * quantity - quantity of EOS being transferred to the contract
        * memo - memo needs to be comma seperated saleid (of the listings) and seller "<sale_id>,<seller>"
        * 
        * saleid represents each unique sale created by any owner of NFT, it can be found in lists and bids table
        */
        ACTION buyshare(name from,
                        name to, 
                        asset quantity,
                        string memo);


        /*
        * closes the listing of sale either by seller before expiration time
        * or by anyone to release the tables after expiration. The unsold token shares are rolled back to seller.
        * 
        * seller - account name of the seller who is selling token shares
        * saleid - represents each unique sale created by any owner of NFT, it can be found in lists table
        */
        ACTION closesale(name seller,
                            uint64_t sale_id);



        /*
        * closes the bidding of sale either by seller before expiration time (unsucessfull)
        * or by anyone to release the tables after expiration and shall be called successfull.
        * When successfull, highest bidder receives the ownership shares listed.
        * 
        * seller - account name of the seller who is selling token shares
        * saleid - represents each unique sale created by any owner of NFT, it can be found in bids table
        */
        ACTION closebid(name seller,
                        uint64_t sale_id);


        /*
        * Removes the table row that can hold particular NFT token. The RAM is released back to RAM payer.
        * Callable by anyone if PERs in the account for the NFT are 0 PER.
        * 
        * owner - account name of the owner who has 0 PERs of particular token.
        * dnft_id - represents each unique NFT created by any owner, it can be found in dnft_stats table.
        */
        ACTION close(name owner,
                        uint64_t dnft_id);


        /*
        * Unauthorise the validator if acts suspiciosly,
        * banned from validating all the categories  
        *  
        * validator - account name being deleted for validation
        */
        ACTION delvalidator(name validator);


        /*
        * Helps external contracts parse actions and tables 
        *
        * Marketplaces, exchanges and other reliant contracts will be able to view this info using the following code.
        *   Configs configs("dnft"_n, "dnft"_n.value);
        *	configs.get("dnft"_n);
        */
        TABLE tokenconfigs {
            name standard;
            string version;
        };
        typedef singleton<"tokenconfigs"_n, tokenconfigs> s_tokenconfigs;


        /*
        * Table stores all categories that exist in the contract. 
        * Scope: _self
        */
        TABLE categories {
            name category;
            vector<uint64_t> validator_ids;
            uint64_t primary_key() const { return category.value; }
        };
        using categories_index = multi_index< "categories"_n, categories>;


        /*
        * Table stores the unique available dnft ids that identify each NFT token.
        * validator_ids are also updated here.
        *  
        */
        TABLE uids{
            uint64_t dnft_id;
            uint64_t validator_id;
        };
        EOSLIB_SERIALIZE( uids, (dnft_id)(validator_id))
        typedef singleton<"uids"_n, uids> s_uids;


        /*
        * Table stores all sale listings of NFT created by sellers. 
        * Scope: _self
        * Secondary index used to find seller's listings
        */
        TABLE lists {
            uint64_t sale_id;
            name token_name;
            name category;
            name seller;
            asset per_percent_amt;
            asset percent_share;
            time_point_sec expiration;
            uint64_t primary_key() const { return sale_id; }
            uint64_t get_seller() const { return seller.value; }
        };
        using list_index = multi_index< "lists"_n, lists,
            indexed_by< "byseller"_n, const_mem_fun< lists, uint64_t, &lists::get_seller> > >;


        /*
        * Table stores all biddings sale of NFT created by sellers. 
        * Scope: _self
        * Secondary index used to find seller's biddings
        */
        TABLE bids {
            uint64_t sale_id;
            name token_name;
            name category;
            name seller;
            asset percent_share;
            asset base_price;
            asset current_bid;
            name current_bidder;
            time_point_sec expiration;
            uint64_t primary_key() const { return sale_id; }
            uint64_t get_seller() const { return seller.value; }
        };
        using bids_index = multi_index< "bids"_n, bids,
                indexed_by< "byseller"_n, const_mem_fun< bids, uint64_t, &bids::get_seller> > >;


        /*
        * Table stores all the stats of any NFT existent on blockchain. 
        * Scope: category of the token (eg. video, music etc.)
        * Secondary index used to seperate validated NFTs.
        */            
        TABLE dnftstats {
            bool    burnable;
            name    issuer;
            name    token_name;
            uint64_t dnft_id;
            asset current_supply;
            asset issued_supply;
            string base_uri;
            checksum256 origin_hash;
            uint8_t span;
            bool validated;
            map<uint64_t, bool> validated_by;
            uint64_t primary_key() const { return token_name.value; }
            uint64_t is_verified() const { return validated; }
        };
        using stats_index = multi_index< "dnftstats"_n, dnftstats,
                indexed_by< "validated"_n, const_mem_fun< dnftstats, uint64_t, &dnftstats::is_verified> > >;


        /*
        * Table stores all the validators who verify the creation of NFT and their existence. 
        * Scope: _self
        */    
        TABLE validators {
            uint64_t validator_id;
            name validator;
            string email;
            vector<name> categories;
            bool active;
            uint64_t primary_key() const { return validator.value; }
        };
        using validator_index = multi_index< "validators"_n, validators>;


        /*
        * Table holds the owners list for every NFT. 
        * Scope: dnft_id of the NFT. 
        */    
        TABLE owners {
            name owner;
            uint64_t primary_key() const { return owner.value; }
        };
        using owner_index = multi_index< "owners"_n, owners>;


        /*
        * Table stores all the dnft ids and their ownership shares that owner account holds. 
        * Scope: owner account name. 
        */    
        TABLE accounts {
            uint64_t dnft_id;
            asset amount;
            uint64_t primary_key() const { return dnft_id; }
        };
        using account_index = multi_index< "accounts"_n, accounts >;

    //Private functions  
    private:

        // transfer any percent_share from 1 account to another
        void transfer_shares(name from,
                            name to,
                            name category,
                            name token_name,
                            asset percent_share);

        // check the stable token "PER" specifications
        void checkasset( asset amount );

        // adds PER balance to owner account 
        void add_balance(name owner, uint64_t dnft_id, asset quantity);

        // subtracts PER balance to owner account 
        void sub_balance(name owner, uint64_t dnft_id, asset quantity);

};
