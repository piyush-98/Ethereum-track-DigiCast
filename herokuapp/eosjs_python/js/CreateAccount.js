// Eos = require('eosjs')

const httpEndpointAddress = process.argv[2];
const chain_id = process.argv[3];
const creator_account = process.argv[4];
const account_name = process.argv[5];
const privatekey = process.argv[6];
const owner_public_key = process.argv[7];
const active_public_key = process.argv[8];
const buyrambytes_bytes = process.argv[9];
const delegatebw_stake_net_quantity = process.argv[10];
const delegatebw_stake_cpu_quantity = process.argv[11];
const delegatebw_transfer = process.argv[12];


// const privatekey = process.argv[4];
//const wif = process.argv[4];

console.log("pk",privatekey);

console.log("ak",creator_account);
console.log("bk",account_name);
console.log("ck",owner_public_key);
console.log("dk",buyrambytes_bytes);
console.log("ek",delegatebw_stake_cpu_quantity);


const { Api, JsonRpc, RpcError } = require('eosjs');
const { JsSignatureProvider } = require('eosjs/dist/eosjs-jssig');      // development only
const fetch = require('node-fetch');                                    // node only; not needed in browsers
const { TextEncoder, TextDecoder } = require('util');                   // node only; native TextEncoder/Decoder
//const { TextEncoder, TextDecoder } = require('text-encoding');          // React Native, IE11, and Edge Browsers only



const signatureProvider = new JsSignatureProvider([privatekey]);//([defaultPrivateKey]);

const rpc = new JsonRpc('https://jungle2.cryptolions.io:443', { fetch });
const api = new Api({ rpc, signatureProvider, textDecoder: new TextDecoder(), textEncoder: new TextEncoder() });













function create_account( creator_account, account_name, owner_public_key, active_public_key, buyrambytes_bytes, delegatebw_stake_net_quantity, delegatebw_stake_cpu_quantity, delegatebw_transfer){
      

    (async () => {
        const result = await api.transact({
            
          actions: [{
            account: 'eosio',
            name: 'newaccount',
            authorization: [{
                actor: creator_account,
                permission: 'active'
            }],
            data: {
              creator: creator_account,
              name: account_name,
              owner: 
              {
                threshold: 1,
                keys: [
                  {
                    key: owner_public_key,
                    weight: 1,
                  },
                ],
                accounts: [],
                waits: [],
              },

              
              active: 
              {
                threshold: 1,
                keys: [
                  {
                    key: active_public_key,
                    weight: 1,
                  },
                ],
                accounts: [],
                waits: [],
              }
          },
          }
          ,{

            account: 'eosio',
            name: 'buyrambytes',
            authorization: [{
                actor: creator_account,
                permission: 'active'
            }],
            data: {
                payer: creator_account,
                receiver: account_name,
                bytes: 5000//parseInt(buyrambytes_bytes)
              },

          },{
            account: 'eosio',
            name: 'delegatebw',
            authorization: [{
                actor: creator_account,
                permission: 'active'
            }],
            data: {
                from: creator_account,
                receiver: account_name,
                stake_net_quantity: delegatebw_stake_net_quantity,
                stake_cpu_quantity: delegatebw_stake_cpu_quantity,
                transfer: false//parseInt(delegatebw_transfer)
            }  

          }
        ]
        }, {
          blocksBehind: 3,
          expireSeconds: 30,
        });
        console.dir(result);
      })().then(function (value){
                console.log((value));
                return value;
              }).catch(function (e) {
              console.error(e);
              process.exit(1);
              });      

}
    
//     eos = Eos({keyProvider: keyProviderValue, httpEndpoint: httpEndpointAddress, chainId: chain_id})
//       eos.transaction(tr => {
//           let data = {
//               creator: creator_account,
//               name: account_name,
//               owner: owner_public_key,
//               active: active_public_key
//           }
//           console.log(data);
//           tr.newaccount(data);
//           tr.buyrambytes({
//               payer: creator_account,
//               receiver: account_name,
//               bytes: parseInt(buyrambytes_bytes)
//           });
//           tr.delegatebw({
//               from: creator_account,
//               receiver: account_name,
//               stake_net_quantity: delegatebw_stake_net_quantity,
//               stake_cpu_quantity: delegatebw_stake_cpu_quantity,
//               transfer: parseInt(delegatebw_transfer)
//           });
//       }).then(function (value){
//         console.log(JSON.stringify(value));
//       }).catch(function (e) {
//       console.error(e);
//       process.exit(1);
//       })
// }


create_account( creator_account, account_name, owner_public_key, active_public_key, buyrambytes_bytes, delegatebw_stake_net_quantity, delegatebw_stake_cpu_quantity, delegatebw_transfer);
            