#pragma once

#include <string>
#include <algorithm>
#include <cctype>
#include <locale>
#include <eosio/eosio.hpp>
#include <math.h>


using namespace std;
using namespace eosio;

namespace utility {

    // trim from left (in place)
    static inline void ltrim(string& s) {
        s.erase( s.begin(), find_if( s.begin(), s.end(), [](int ch) {
            return !isspace(ch);
        }));
    }

    // trim from right (in place)
    static inline void rtrim(string& s) {
        s.erase( find_if( s.rbegin(), s.rend(), [](int ch) {
            return !isspace(ch);
        }).base(), s.end());
    }

    // trim from both ends (in place)
    static inline string trim(string s) {
        ltrim(s);
        rtrim(s);
        return s;
    }

    tuple<uint64_t, name> parsememo(const string& memo) {
        auto dot_pos = memo.find(',');
        string errormsg = "malformed memo: must have sale_id,to_account";
        check ( dot_pos != string::npos, errormsg.c_str() );
        if ( dot_pos != string::npos ) {
            check( ( dot_pos != memo.size() - 1 ), errormsg.c_str() );
        }
        // will abort if stoull throws error since wasm no error checking
        uint64_t sale_id = stoull( trim( memo.substr( 0, dot_pos ) ) );
        name to_account = name( trim ( memo.substr( dot_pos + 1 ) ) );

        return make_tuple(sale_id, to_account);

    }

    // division of 2 assets
    asset div(const eosio::asset &a, const eosio::asset &b, const eosio::symbol &c) {
    double result = static_cast<double>(a.amount) /
                static_cast<double>(b.amount);
    result *= pow(10, b.symbol.precision());
    return asset(static_cast<uint64_t>(result), c);
}

    // multiplication of 2 assets
   asset mul(const eosio::asset &a, const eosio::asset &b, const eosio::symbol &c) {
    double result = static_cast<double>(a.amount) *
                static_cast<double>(b.amount);
    result /= pow(10, b.symbol.precision());
    return asset(static_cast<uint64_t>(result), c);
}

}
