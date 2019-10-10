
### Rationale
0. `setconfig`action is called by contract account specifying the version that helps external contracts parse actions and tables 
1. Contract account adds the validators account for categories like `videos`, `music` etc. `addvalidator` action is called.
2. Anyone can create the NFT under the category by calling `create` action. The creator needs to send mail to validator with original JSON file, listing their creation & the legal binding agreement (if needed for some high valued NFT in real world). The validator validates that in the platform if creation is not plagiarised. 
3. Random Validator selected validates the creation after taking fees offered. Validators validate using `validate` action.
4. After validated creation of NFT by both, NFT creator can issue ownership of NFTs to different accounts, say stakeholders if required. Issuing NFT can be done by calling action `issue`.
5. All current owners of NFT can list for sale of their ownership at fixed rate (using `listsale` action) or choose the bidding mechanism (using `startbid` action).
6. Investors can buy the ownership using eosio.token **```transfer```** action by sending EOS to the contract with the memo as:
**```sale_id,to```**
7. Sale listing or bidding may be closed by seller before expiration. Bidding is realised as unsuccessful if that happens. For the successful bidding, highest bidder receives the ownership shares. Actions for them are `closesale` and `closebid`.
8. For all the accounts with zero ownership may be deleted by anyone if the ram payer is configured as contract. Action `close` can be called to do so.
9. `burn` action needs to be called by creator in case of non-validation to release RAM or when anyone wants to burn their ownership shares.
10. In case any validator is found suspicious, `delvalidator` action is called by contract account. Validator account no longer can validate any further NFTs.


##### Note: To ensure the authenticity of NFT, mail mechanism is kept. Keeping blockchain fundamentals as permissionless, any EOS account can invest and do all operations normally.

---------------------------  

