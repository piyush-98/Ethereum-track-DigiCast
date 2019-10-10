
#include <dnfts.hpp>

ACTION dnfts::setconfig(string version)
{

    require_auth(get_self());
    // add/update tokenconfigs singleton table
    s_tokenconfigs configs(get_self(), get_self().value);
    configs.set(tokenconfigs{"dnft"_n, version}, get_self());
}

ACTION dnfts::create(name issuer,
                     name category,
                     name token_name,
                     bool burnable,
                     string base_uri,
                     uint8_t span,
                     checksum256 origin_hash)
{

    require_auth(issuer);
    check(base_uri.size() <= 256, "base_uri has more than 256 bytes");

    // check if config table exists
    s_tokenconfigs config_table(get_self(), get_self().value);
    check(config_table.exists(), "Config table does not exist, setconfig first");

    // find the category and make new dnft_id
    categories_index category_table(get_self(), get_self().value);
    auto cat = category_table.find(category.value);

    // category hasn't been created for validation
    check(cat != category_table.end(), "Validator doesnot exist for the given category");
    
    auto num_validators = std::distance(category_table.cbegin(), category_table.cend());

    // atleast 2 validators are required for the category to validate
    check(num_validators >= 1, "Validators for the given category < 2");

    s_uids uid_table(get_self(), get_self().value);
    auto uid_singleton = uid_table.get_or_create(get_self(), uids{0, 0});
    auto dnft_id = uid_singleton.dnft_id;

    // check provided validator_id can authorise
    vector<uint64_t> v(cat->validator_ids);

    // generate random numbers between 0 to no. of validators who can validate
    validator_index validator_table(get_self(), get_self().value);
    auto size = v.size();
    auto random_num = ((tapos_block_num() % size) + transaction_size() + tapos_block_prefix() + expiration()) % (size - 1);

    // find random validator id
    uint64_t validator_id = 0;//v[random_num];

    // print(validator2_id);
    stats_index stats_table(get_self(), category.value);
    auto existing_token = stats_table.find(token_name.value);
    check(existing_token == stats_table.end(), "Token with category and token_name exists");
    // token type hasn't been created, create it
    stats_table.emplace(issuer, [&](auto &stats) {
        stats.dnft_id = dnft_id;
        stats.issuer = issuer;
        stats.token_name = token_name;
        stats.burnable = burnable;
        stats.span = span;
        stats.current_supply = PER;                 // 100%
        stats.issued_supply = asset(0, PER.symbol); //0%
        stats.origin_hash = origin_hash;
        stats.base_uri = base_uri;
        stats.validated = false;
        stats.validated_by[validator_id] = false;
    });
    uid_singleton.dnft_id++;
    uid_table.set(uid_singleton, get_self());
}

ACTION dnfts::addvalidator(name validator, string email, name category)
{

    // callable by _self only
    require_auth(get_self());
    // check email size
    check(email.size() <= 256, "email has more than 256 bytes");

    validator_index validator_table(get_self(), get_self().value);
    auto acct = validator_table.find(validator.value);

    categories_index category_table(get_self(), get_self().value);
    auto existing_category = category_table.find(category.value);

    // Validator account doesnot exists
    if (acct == validator_table.end())
    {
        s_uids uid_table(get_self(), get_self().value);
        auto uid_singleton = uid_table.get_or_create(get_self(), uids{0, 0});
        auto validator_id = uid_singleton.validator_id;

        // add in validator's table
        validator_table.emplace(get_self(), [&](auto &a) {
            a.validator_id = validator_id;
            a.validator = validator;
            a.email = email;
            a.active = true;
            a.categories.push_back(category);
        });

        uid_singleton.validator_id++;
        uid_table.set(uid_singleton, get_self());
    }
    // email ids and categories may be modified
    else
    {
        validator_table.modify(acct, same_payer, [&](auto &a) {
            a.email = email;
            a.categories.push_back(category);
            a.active = true;
        });
    }

    auto updated_acct = validator_table.find(validator.value);
    if (existing_category == category_table.end())
    {

        //Category doesnot exists, emplace the category
        category_table.emplace(_self, [&](auto &cat) {
            cat.category = category;
            cat.validator_ids.push_back(updated_acct->validator_id);
        });
    }
    else
    {
        // update in categories table
        category_table.modify(existing_category, same_payer, [&](auto &cat) {
            cat.validator_ids.push_back(updated_acct->validator_id);
        });
    }
}

ACTION dnfts::delvalidator(name validator)
{

    // callable by _self only
    require_auth(get_self());

    validator_index validator_table(get_self(), get_self().value);
    auto acct = validator_table.find(validator.value);

    // check if validator exists
    check(acct != validator_table.end(), "Validator account doesnot exists");
    uint64_t v_id = acct->validator_id;

    // delete from all categories
    categories_index category_table(get_self(), get_self().value);

    // temp variables to update vectors
    vector<name> v(acct->categories);
    vector<name>::iterator it;

    // iterate to all categories validator can validate
    for (it = v.begin(); it != v.end(); it++)
    {
        name c = *it;
        const auto &cat = category_table.get(c.value, "Category doesnt exist");
        vector<uint64_t> cids(cat.validator_ids);
        cids.erase(std::remove(cids.begin(), cids.end(), v_id), cids.end());
        // modify category table and remove the validator id
        category_table.modify(cat, same_payer, [&](auto &c) {
            c.validator_ids.assign(cids.begin(), cids.end());
        });
    }

    // modify validators table and remove all categories
    validator_table.modify(acct, same_payer, [&](auto &a) {
        a.active = false;
        a.categories.clear();
    });
}

ACTION dnfts::validate(name validator, name category, name token_name)
{

    require_auth(validator);

    validator_index validators_table(get_self(), get_self().value);
    categories_index categories_table(get_self(), get_self().value);

    // check if account can validate the category & category exists
    auto acct = validators_table.find(validator.value);
    check(acct != validators_table.end(), "The account is not allowed for validation");

    auto cat = categories_table.find(category.value);
    check(cat != categories_table.end(), "The category doesnot exist");

    // check if validator is not disallowed
    check(acct->active, "The account is disallowed for validation");

    // temp variables to store vectors and check conditions
    vector<uint64_t> v(cat->validator_ids);
    vector<name> acc(acct->categories);

    check(find(v.begin(), v.end(), acct->validator_id) != v.end(), "Validator is not authorised to validate the category ");
    check(find(acc.begin(), acc.end(), category) != acc.end(), "Validator is not authorised to validate the category ");

    stats_index stats_table(get_self(), category.value);
    const auto &dnft_stats = stats_table.get(token_name.value,
                                             "Token with category and token_name does not exist");

    // update stats table
    stats_table.modify(dnft_stats, same_payer, [&](auto &stats) {
        stats.validated_by[acct->validator_id] = true;
        stats.validated = true;
    });

    // // check if both validators have been validated
    // map<uint64_t, bool> m(dnft_stats.validated_by);
    // map<uint64_t, bool>::iterator it;
    // short validation_count = 0;
    // for (it = m.begin(); it != m.end(); it++)
    //     if (it->second == true)
    //         validation_count++;

    // // both validators have validated
    // if (validation_count == 2)
    //     stats_table.modify(dnft_stats, same_payer, [&](auto &stats) {
    //         stats.validated = true;
    //     });
}

ACTION dnfts::issue(name to,
                    name category,
                    name token_name,
                    asset quantity,
                    string memo)
{

    check(is_account(to), "to account does not exist");
    // check memo size
    check(memo.size() <= 256, "memo has more than 256 bytes");

    stats_index stats_table(get_self(), category.value);
    const auto &dnft_stats = stats_table.get(token_name.value,
                                             "Token with category and token_name does not exist");

    // ensure have issuer authorization and valid quantity
    require_auth(dnft_stats.issuer);

    // check if quantity is in PER
    checkasset(quantity);

    check(dnft_stats.validated == true, "The verification by validator is still pending");

    // check cannot issue more than available ownership
    check(quantity.amount <= (dnft_stats.current_supply.amount - dnft_stats.issued_supply.amount), "Cannot issue more than max supply");

    add_balance(to, dnft_stats.dnft_id, quantity);

    // increase current supply
    stats_table.modify(dnft_stats, same_payer, [&](auto &s) {
        s.issued_supply += quantity;
    });
}

ACTION dnfts::transfer(name from,
                       name to,
                       name category,
                       name token_name,
                       asset percent_share,
                       string memo)
{
    require_auth(from);
    // check memo size
    check(memo.size() <= 256, "memo has more than 256 bytes");
    // transfer NFT PERs from -> to
    transfer_shares(from, to, category, token_name, percent_share);
}

ACTION dnfts::burn(name owner,
                   name category,
                   name token_name,
                   asset quantity)
{

    // ensure have owners authorization and valid quantity
    require_auth(owner);

    // check conditions of PER
    checkasset(quantity);

    stats_index stats_table(get_self(), category.value);
    const auto &dnft_stats = stats_table.get(token_name.value,
                                             "Token with category and token_name does not exist");

    check(dnft_stats.burnable == true, "The token is not allowed to be burnable");

    sub_balance(owner, dnft_stats.dnft_id, quantity);

    // decrease current and issued PERs
    stats_table.modify(dnft_stats, same_payer, [&](auto &s) {
        s.current_supply.amount -= quantity.amount;
        s.issued_supply.amount -= quantity.amount;
    });
}

ACTION dnfts::listsale(name seller,
                       name category,
                       name token_name,
                       asset percent_share,
                       asset per_percent_amt,
                       time_point_sec expiration)
{

    require_auth(seller);

    // minimum amount should be sent
    check(per_percent_amt.amount > .02, "minimum price of at least 0.02 VID");

    // check conditions of PER
    checkasset(percent_share);

    list_index list_table(get_self(), get_self().value);

    stats_index stats_table(get_self(), category.value);
    const auto &dnft_stats = stats_table.get(token_name.value,
                                             "Token with category and token_name does not exist");

    account_index from_account(get_self(), seller.value);
    const auto &acct = from_account.get(dnft_stats.dnft_id, "This category token does not exist in account");

    // check account balance wrt listing
    check(acct.amount.amount >= percent_share.amount, "cannot list sale more than owner's actual percent share");

    // find configuration for ram_payer
    auto ram_payer = CONTRACT_PAYER ? get_self() : seller;

    if (CONTRACT_PAYER)
        check(expiration <= time_point_sec(current_time_point()) + MONTH_SEC, "The sale listing should expire within 30 days");

    // transfer listed shares to _self
    transfer_shares(seller, get_self(), category, token_name, percent_share);

    // add token to table of lists
    list_table.emplace(ram_payer, [&](auto &list) {
        list.sale_id = list_table.available_primary_key();
        list.token_name = token_name;
        list.seller = seller;
        list.percent_share = percent_share;
        list.category = category;
        list.per_percent_amt = per_percent_amt;
        list.expiration = expiration;
    });
}

ACTION dnfts::closesale(name seller,
                        uint64_t sale_id)
{

    list_index list_table(get_self(), get_self().value);
    const auto &list = list_table.get(sale_id, "cannot cancel sale that doesn't exist");

    // if sale listing has not expired, only seller can cancel
    if (time_point_sec(current_time_point()) < list.expiration)
    {
        require_auth(seller);
        check(list.seller == seller, "only the seller can cancel a sale in progress");
    }
    // transfer shares back to seller
    transfer_shares(get_self(), seller, list.category, list.token_name, list.percent_share);

    // remove sale listing from table
    list_table.erase(list);
}

ACTION dnfts::startbid(name seller,
                       name category,
                       name token_name,
                       asset percent_share,
                       asset base_price,
                       time_point_sec expiration)
{

    require_auth(seller);

    // check if base price is in VID
    check(base_price.symbol == symbol(symbol_code("VID"), 4), "only accept VID for biddings");

    bids_index bids_table(get_self(), get_self().value);
    list_index list_table(get_self(), get_self().value);

    // check conditions of PER
    checkasset(percent_share);

    stats_index stats_table(get_self(), category.value);
    const auto &dnft_stats = stats_table.get(token_name.value,
                                             "Token with category and token_name does not exist");

    account_index from_account(get_self(), seller.value);
    const auto &acct = from_account.get(dnft_stats.dnft_id, "This category token does not exist in account");

    // check owner balance
    check(acct.amount.amount >= percent_share.amount, "cannot list sale more than owner's actual percent share");

    // check ram payer
    auto ram_payer = CONTRACT_PAYER ? get_self() : seller;
    if (CONTRACT_PAYER)
        check(expiration <= time_point_sec(current_time_point()) + MONTH_SEC, "The bidding listing should expire within 30 days");

    // shares for bidding are transferred to _self
    transfer_shares(seller, get_self(), category, token_name, percent_share);

    // update bids table and start bid of NFT
    bids_table.emplace(ram_payer, [&](auto &b) {
        b.sale_id = list_table.available_primary_key();
        ;
        b.token_name = token_name;
        b.category = category;
        b.seller = seller;
        b.percent_share = percent_share;
        b.current_bid = base_price;
        b.current_bidder = name("");
        b.base_price = base_price;
        b.expiration = expiration;
    });
}

ACTION dnfts::closebid(name seller,
                       uint64_t sale_id)
{

    bids_index bids_table(get_self(), get_self().value);
    const auto &bid = bids_table.get(sale_id, "cannot cancel bidding that doesn't exist");

    // check if bidding has expired
    if (time_point_sec(current_time_point()) >= bid.expiration)
    {

        // successful bidding give % shares to highest bidder, callable by anyone
        if (bid.current_bidder != name(""))
        {
            transfer_shares(get_self(), bid.current_bidder, bid.category, bid.token_name, bid.percent_share);
            action(permission_level{get_self(), name("active")}, name("dnfttoken123"), name("transfer"),
                   make_tuple(get_self(), bid.seller, bid.current_bid, "successful bidding, transfer highest bid for sale_id" + to_string(sale_id)))
                .send();
        }

        else
            // no one took part in bidding so an unsucessful bidding
            // rollback bid shares to seller
            transfer_shares(get_self(), bid.seller, bid.category, bid.token_name, bid.percent_share);
    }

    //unsucessful bidding, callable by seller
    else
    {

        require_auth(seller);
        check(bid.seller == seller, "only the seller can cancel bidding in progress");

        // clear bid returning to seller
        transfer_shares(get_self(), seller, bid.category, bid.token_name, bid.percent_share);

        // also send back current bid back to investor
        if (bid.current_bidder != name(""))
        {
            action(permission_level{get_self(), name("active")}, name("dnfttoken123"), name("transfer"),
                   make_tuple(get_self(), bid.current_bidder, bid.current_bid, "rollback due to cancel of biddings" + to_string(sale_id)))
                .send();
        }
    }
    bids_table.erase(bid);
}

//memo : sale_id,to_account
ACTION dnfts::buyshare(name from,
                       name to,
                       asset quantity,
                       string memo)
{

    if (to != get_self())
        return;
    // check if quantity is in VID
    if (quantity.symbol != symbol(symbol_code("VID"), 4))
        return;
    if (memo.length() > 32)
        return;

    uint64_t sale_id;
    name to_account;
    tie(sale_id, to_account) = parsememo(memo);

    list_index list_table(get_self(), get_self().value);
    bids_index bids_table(get_self(), get_self().value);

    // check if sale_id is either of bidding or listing
    check(list_table.find(sale_id) != list_table.end() || bids_table.find(sale_id) != bids_table.end(), "Sale id doesnot exists");

    if (list_table.find(sale_id) != list_table.end())
    {

        const auto &list = list_table.get(sale_id, "token not listed for sale");

        //check expiration and memo format
        check(list.expiration > time_point_sec(current_time_point()), "sale has expired");
        check(list.seller == to_account, "saleID, to_account combination (memo) doesnot exist");

        asset sharepercent = div(quantity, list.per_percent_amt, PER.symbol);

        // check if VID sent can be used to buy <= listed PERs of NFT
        check(list.percent_share >= sharepercent, "The amount exceeded the price of the token share %");

        // VID are transferred to seller
        action(permission_level{get_self(), name("active")}, name("dnfttoken123"), name("transfer"),
               make_tuple(get_self(), list.seller, quantity, "sold token: " + to_string(sale_id)))
            .send();

        // remove sale from list_table if complete else modify
        if (list.percent_share == sharepercent)
            list_table.erase(list);
        else
            list_table.modify(list, same_payer, [&](auto &a) {
                a.percent_share -= sharepercent;
            });

        // transfer the bought shares to investor
        transfer_shares(get_self(), from, list.category, list.token_name, sharepercent);
    }
    else if (bids_table.find(sale_id) != bids_table.end())
    {

        const auto &bid = bids_table.get(sale_id, "token not listed for sale");

        //check expiration & memo format
        check(bid.expiration > time_point_sec(current_time_point()), "sale has expired");
        check(bid.seller == to_account, "saleID, to_account combination (memo) doesnot exist");

        // allow only price > current bidding price
        check(quantity > bid.current_bid, "Bidding price must be more than current bidding price");

        // rollback the previous bidder's bidding
        if (bid.current_bidder != name(""))
            action(permission_level{get_self(), name("active")}, name("dnfttoken123"), name("transfer"),
                   make_tuple(get_self(), bid.current_bidder, bid.current_bid, "Released back the lesser bidding_amount" + to_string(sale_id)))
                .send();

        // update new bidder and current bid
        bids_table.modify(bid, same_payer, [&](auto &a) {
            a.current_bidder = from;
            a.current_bid = quantity;
        });
    }
}

ACTION dnfts::close(name owner,
                    uint64_t dnft_id)
{

    // if contract is the RAM payer, anyone can erase 0 PER's accounts
    if (!CONTRACT_PAYER)
        require_auth(owner);

    account_index account(get_self(), owner.value);
    auto acct = account.find(dnft_id);
    owner_index d_category(get_self(), dnft_id);
    auto dnft = d_category.find(owner.value);

    // check if 0 PERS exists for dnft
    check(acct != account.end(), "Token for dnft_id doesnot exists");
    check(dnft != d_category.end(), "Owner account doesnot exists");
    check(acct->amount.amount == 0, "Account holds PERs of the token");

    // release the RAM
    account.erase(acct);
    d_category.erase(dnft);
}

// Private
void dnfts::checkasset(asset amount)
{
    // check conditions of PER
    auto sym = amount.symbol;
    check(amount.amount > 0, "amount must be positive");
    check(PER.symbol.code().raw() == sym.code().raw(), "Symbol used must be 'PER'");
    check(amount.is_valid(), "invalid amount");
    string string_precision = "precision of quantity must be " + to_string((PER.symbol).precision());
    check(amount.symbol == PER.symbol, string_precision.c_str());
}

//Private
void dnfts::transfer_shares(name from,
                            name to,
                            name category,
                            name token_name,
                            asset percent_share)
{
    // check if from and to are different accounts and to exists
    check(from != to, "cannot transfer to self");
    check(is_account(to), "to account does not exist");
    checkasset(percent_share);

    // get dnft_id of NFT
    stats_index stats_table(get_self(), category.value);
    const auto &dnft_stats = stats_table.get(token_name.value, " token stats not found");

    // update balances
    sub_balance(from, dnft_stats.dnft_id, percent_share);
    add_balance(to, dnft_stats.dnft_id, percent_share);
}

// Private
void dnfts::add_balance(name owner, uint64_t dnft_id, asset quantity)
{

    account_index to_account(get_self(), owner.value);
    owner_index d_category(get_self(), dnft_id);
    auto acct = to_account.find(dnft_id);
    auto dnft = d_category.find(owner.value);

    // check ram payer config
    auto ram_payer = CONTRACT_PAYER ? get_self() : owner;

    // update accounts table
    if (acct == to_account.end())
    {

        to_account.emplace(ram_payer, [&](auto &a) {
            a.dnft_id = dnft_id;
            a.amount = quantity;
        });
    }
    else
        to_account.modify(acct, same_payer, [&](auto &a) {
            a.amount += quantity;
        });

    // update category table
    if (dnft == d_category.end())
        d_category.emplace(ram_payer, [&](auto &a) {
            a.owner = owner;
        });
}

// Private
void dnfts::sub_balance(name owner, uint64_t dnft_id, asset quantity)
{

    account_index from_account(get_self(), owner.value);
    const auto &acct = from_account.get(dnft_id, "token does not exist in account");

    // check if balance in owner account > transferred balance
    check(acct.amount.amount >= quantity.amount, "quantity is more than account balance");

    // update the accounts table
    from_account.modify(acct, same_payer, [&](auto &a) {
        a.amount -= quantity;
    });
}

extern "C"
{
    void apply(uint64_t receiver, uint64_t code, uint64_t action)
    {
        auto self = receiver;

        if (code == self)
        {
            switch (action)
            {
                EOSIO_DISPATCH_HELPER(dnfts, (setconfig)(create)(issue)(burn)(addvalidator)(delvalidator)(validate)(startbid)(closebid)(listsale)(closesale)(transfer)(close))
            }
        }
        else
        {
            if (code == name("dnfttoken123").value && action == name("transfer").value)
            {
                execute_action(name(receiver), name(code), &dnfts::buyshare);
            }
        }
    }
}