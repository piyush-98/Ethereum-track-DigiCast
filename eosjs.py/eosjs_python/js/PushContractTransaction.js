//Eos = require('eosjs') // Eos = require('./src')

// import { Api, JsonRpc, RpcError } from 'eosjs';
// import { JsSignatureProvider } from 'eosjs/dist/eosjs-jssig';           // development only

const privatekey = process.argv[4];
//const wif = process.argv[4];

// console.log("pk",privatekey);

const contract_account = process.argv[5];
const contract_function = process.argv[6];
const authorization_actor = process.argv[7];
const authorization_permission = process.argv[8];
const data_values = JSON.parse(process.argv[9]);
// console.log("ak",contract_account);
// console.log("bk",contract_function);
// console.log("ck",authorization_actor);
// console.log("dk",authorization_permission);
// console.log("ek",data_values);


const { Api, JsonRpc, RpcError } = require('eosjs');
const { JsSignatureProvider } = require('eosjs/dist/eosjs-jssig');      // development only
const fetch = require('node-fetch');                                    // node only; not needed in browsers
const { TextEncoder, TextDecoder } = require('util');                   // node only; native TextEncoder/Decoder
//const { TextEncoder, TextDecoder } = require('text-encoding');          // React Native, IE11, and Edge Browsers only



const defaultPrivateKey = "5KE2yA2iuQWrzzpSFt3VPCwdYZPrqse9k1z97Bpb5gz9gw1bMxD"; // useraaaaaaaa
const signatureProvider = new JsSignatureProvider([privatekey]);//([defaultPrivateKey]);

const rpc = new JsonRpc('https://jungle2.cryptolions.io:443', { fetch });
const api = new Api({ rpc, signatureProvider, textDecoder: new TextDecoder(), textEncoder: new TextEncoder() });

// eos = Eos({
//   keyProvider: wif,
//   httpEndpoint: httpEndpointAddress,
//   chainId: chain_id
// })


// eos.transaction({
//   actions: [
//     {
//       account: contract_account,
//       name: contract_function,
//       authorization: [{
//         actor: authorization_actor,
//         permission: authorization_permission
//       }],
//       data: data_values
//     }
//   ]
// }).then(function (value){
//         console.log(JSON.stringify(value));
//         return value;
//       }).catch(function (e) {
//       console.error(e);
//       process.exit(1);
//       })



      (async () => {
        const result = await api.transact({
          actions: [{
            account: contract_account,
            name: contract_function,
            authorization: [{
                actor: authorization_actor,
                permission: authorization_permission
            }],
            data: data_values,
          }]
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
              })
        ;      


      // (async () => {
      //   const result = await api.transact({
      //     actions: [{
      //       account: 'zeptagram123',
      //       name: 'transfer',
      //       authorization: [{
      //         actor: 'alicezepta12',
      //         permission: 'active',
      //       }],
      //       data: {
      //         from: 'alicezepta12',
      //         to: 'bobzeptagram',
      //         quantity: '1.0001 ZPT',
      //         memo: '',
      //       },
      //     }]
      //   }, {
      //     blocksBehind: 3,
      //     expireSeconds: 30,
      //   });
      //   console.dir(result);
      // })();