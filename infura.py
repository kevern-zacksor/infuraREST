"""
@Description : Client side python api implementation for infura server. The class defines infura  
               typed objects allowing access to Ethereums network via infura. Infura types will 
               require public and private keys during instantiation. Currently no exceptions 
               class exists, this will change shortly.
@Author      : k.z
"""
import requests 
import time
import json

_PROTOCOL     = "https"
_ENDPOINT     = "infura.io"
_VERSION      = "v3"
_GET_METHOD   = []
_PUBLIC_SET   = ["eth_blockNumber","eth_getBlockByNumber","eth_getBlockByHash","eth_getTransactionByHash","eth_getTransactionReceipt"]
_PRIVATE_SET  = ["eth_accounts"]
_POST_METHOD  = [
    "eth_getTransactionByHash","eth_getTransactionByBlockNumberAndIndex","eth_getTransactionByBlockHashAndIndex","eth_getStorageAt",
    "eth_getLogs","eth_getBlockTransactionCountByNumber","eth_getBlockTransactionCountByHash","eth_getBlockByHash",
    "eth_getBalance","eth_gasPrice","eth_estimateGas","eth_call","eth_blockNumber","eth_getBlockByHash","eth_getBlockByNumber",
    "eth_getTransactionByHash","eth_getTransactionReceipt","eth_accounts", "eth_getTransactionCount","eth_getUncleCountByBlockHash",
    "eth_getUncleCountByBlockNumber","eth_getUncleByBlockHashAndIndex","eth_getUncleByBlockNumberAndIndex","eth_hashrate","eth_mining",
    "eth_protocolVersion","eth_syncing","net_listening","net_peerCount","net_version","web3_clientVersion","eth_getWork"
    ]


class INFURA(object):
    def __init__( self, _project_id, _project_scrt, _network='mainnet' ):        
        self._PROJECT_ID   = _project_id
        self._PROJECT_SCRT = _project_scrt
        self._URL  = "{}://{}.{}/{}/{}".format(_PROTOCOL,_network,_ENDPOINT,_VERSION,self._PROJECT_ID)
    
    #@Description: Forward facing caller. This function sanitizes outgoing and
    #              handles errors in returns (tbd).  
    #@Parameters :
    # _method      [ str ] The name of the JSON RPC method. 
    # _params      [ dict] The methods parameter counterparties. 
    #@Return     :
    # _request     Requests object. 
    def api_call( self, _method, _params=[] ):
        _headers = {}
        _headers['Content-Type'] = "application/json"        
        _data = {"id":1,"method":_method,"params":_params} 

        # Catch/handle here. soon to be moved and expection class to be added 
        try: 
            if _method in _POST_METHOD:
                _type = "POST" 
                _rtn  = requests.post(self._URL,headers=_headers,data=json.dumps(_data))
            elif _method in _GET_METHOD:
                _type = "GET"
                _rtn  = requests.get(self._URL,headers=_headers,data=json.dumps(_data))                
            else:
                print(" Method [ {} ] cannot be found. Returning None ".format(_method))
                return None            
        except Exception as e:
            print("API Exception : {} ".format( str()) )
            return {} 
            
        return _rtn.json()

    #@Description: Return the base url 
    #@Parameters : None 
    #@Return     :
    # _URL         [ str] The urlas a string.   
    def get_url( self ):
        return self._URL

    #@Description: Returns a list of addresses owned by client.
    #@Method     : eth_accounts
    #@Parameters : None 
    #@Return     :  
    # jsonrpc      [ str ] Version of RPC. 
    # id     	   [ int ] ...
    # result       [ hex ] Hex code of an integer rep. current block.
    # Addresses    [ list] Hex codes as strings representing the addresses
    #                      owned by the client. 
    def get_accounts( self ):
        return self.api_call("eth_accounts",[])["result"] 

    #@Description: Returns the current "latest" block number. 
    #@Method     : eth_blockNumber   
    #@Parameters : None 
    #@Return     :  
    # jsonrpc      [ str ] Version of RPC. 
    # id	   [ int ] ...
    # result       [ hex ] hex code of an integer rep. current block.
    def get_block_number( self ):
        _rtn = self.api_call("eth_blockNumber",[])
        return int(_rtn["result"],16)    

    #@Description: Returns information about a block by hash.
    #@Method     : eth_getBlockByHash
    #@Parameters : 
    # _blk_hash    [ str ] str representing the hash (32 bytes) of a block
    # _tx_flag     [ bool] true returns full tx object, false on tx hashes. 
    #@Return     :  
    # block      [ dict] block object, or null when no block was found
    #  number      [ int ] the block number. Null when the returned block is the pending block.
    #  hash        [ str ] 32 Bytes,hash of the block. Null if returned block is the pending block.
    #  parentHash  [ str ] 32 Bytes,hash of the parent block.
    #  nonce       [ str ] 8 Bytes,hash of the generated proof-of-work. Null if returned block is the pending block.
    #  sha3Uncles  [     ] 32 Bytes,SHA3 of the uncles data in the block.
    #  logsBloom   [     ] 256 Bytes, the bloom filter for the logs of the block. Null when block is the pending block.
    #  txRoot      [     ] 32 Bytes, the root of the transaction trie of the block.
    #  stateRoot   [     ] 32 Bytes,the root of the final state trie of the block.
    #  receiptsRoot[     ] 32 Bytes,the root of the receipts trie of the block.
    #  miner       [     ] 20 Bytes, the address of the beneficiary to whom the mining rewards were given.
    #  difficulty  [ int ] the difficulty for this block.
    #  totalDiff   [ int ] the total difficulty of the chain until this block.
    #  extraData   [     ] the "extra data" field of this block.
    #  size        [ int ] integer the size of this block in bytes.
    #  gasLimit    [ int ] the maximum gas allowed in this block.
    #  gasUsed     [ int ] the total used gas by all transactions in this block.
    #  timestamp   [ ts  ] the unix timestamp for when the block was collated.
    #  uncles      [ list] array of uncle hashes.
    #  txs         [ list] array of transaction objects, or 32 Bytes transaction hashes depending
    #                      on the last given parameter.
    def get_block_by_hash( self, _blk_hash,_tx_flag=True ):
        return self.api_call("eth_getBlockByHash",[str(_blk_hash),_tx_flag])
    
    #@Description: Returns information about a block by hash.
    #@Method     : eth_getBlockByNumber
    #@Parameters : None 
    # _blk_num     [ str ] str representing the hash (32 bytes) of a block
    # _tx_flag     [ bool] true returns full tx object, false on tx hashes. 
    #@Return     :  
    # block        [ dict ] A block object, see get block by hash
    def get_block_by_number( self, _blk_num, _tx_flag=True ):
        return self.api_call("eth_getBlockByNumber",[hex(_blk_num),_tx_flag])

    #@Description: Returns information about a transaction for a given hash.
    #@Method     : 
    #@Parameters :
    #   _tx_hash   [ str ]  32 bytes hash of a transaction
    #@Return     :
    # tx         [ dict  ] tx object, or null when no tx was found
    #   hash       [ str ] 32 Bytes hash of the transaction.
    #   nonce      [ str ] the number of txs made by the sender prior to this one.
    #   blockHash  [ str ] 32 Bytes hash of the block where this tx was in. null when pending.
    #   blockNumber[ str ] block number where this tx was in. null when its pending.
    #   txIndex    [ int ] tx index position in the block. null when its pending.
    #   from       [ str ] 20 Bytes address of the sender.
    #   to         [ str ] 20 Bytes address of the receiver. null when contract creation tx.
    #   value      [float] value tx in Wei.
    #   gasPrice   [float] gas price provided by the sender in Wei.
    #   gas        [float] gas provided by the sender.
    #   input      [ str ] the data send along with the transaction.
    def get_transaction_by_hash( self, _tx_hash ):
        return self.api_call("eth_getTransactionByHash",[str(_tx_hash)])
 
    #@Description: Returns the receipt of a transaction by transaction hash. The
    #              receipt is not available for pending transactions.
    #@Method     :
    #@Parameters :
    #   _tx_hash   [ str ] represents the hash (32 bytes) of a transaction.
    #@Return     :
    # tx_receipt [ dict  ] A transaction receipt object, or null when no receipt was found.
    #  txHash      [ str ] 32 Bytes,  hash of the transaction.
    #  txIndex     [ int ] the transactions index position in the block.
    #  blockHash   [ str ] 32 Bytes hash of the block where this tx was in. null when pending.
    #  blockNumber [ str ] block number where this tx was in. null when its pending.
    #  from        [ str ] 20 Bytes address of the sender.
    #  to          [ str ] 20 Bytes address of the receiver. null when contract creation tx.
    #  cumlteGasUsd[     ] total amount of gas used when this transaction was executed in the block.
    #  gasUsed     [     ] the amount of gas used by this specific transaction alone.
    #  contractAddr[     ] 20 Bytes, contract address created, if tx was contract creation, null otherwise.
    #  logs        [ list] array of the log objects, which this tx generated
    #  logsBloom   [     ] 256 Bytes, bloom filterr for light clients to quickly rerieve logs. 
    def get_transaction_receipt( self, _tx_hash ):
        return self.api_call("eth_getTransactionReceipt",[str(_tx_hash)])

    #@Description: Executes a new message call immediately without creating a
    #              transaction on the block chain.
    #@Method     : eth_call
    #@Parameters :
    # required: 
    #  blk_param  [ int   ] An int block number, or the str "latest", "earliest" or "pending"
    # optional: 
    #  tx_call_ob [ dict  ] A transaction receipt object, or null when no receipt was found.
    #   from        [ str ] 20 Bytes, The address the transaction is sent from.
    #   to          [ int ] 20 bytes, The address the transaction is directed to.
    #   gas         [ str ] Integer of the gas provided for the transaction execution. 
    #                       eth_call consumes zero gas, but this parameter may be needed by 
    #                       some executions.
    #   gasPrice    [ int ] Integer of the gasPrice used for each paid gas
    #   value       [ str ] Integer of the value sent with this transaction
    #   data        [ int ] Hash of the method signature and encoded parameters. 
    #@Return     :
    # blk_param  [ dict  ] the return value of the executed contract method.
    def make_eth_call( self, *args, **kwargs):    
        return self.api_call( "eth_call", [kwargs, args[0]] )
    
    #@Description: Generates and returns an estimate of how much gas is necessary to 
    #              allow the transaction to complete.If no gas limit is specified geth 
    #              uses the block gas limit from the pending block as an upper bound.
    #@Method     : eth_estimateGas
    #@Parameters :	
    # required
    #  tx_call_ob [ dict  ] A transaction receipt object, or null when no receipt was found.
    #   from        [ str ] 20 Bytes, The address the transaction is sent from.
    #   to          [ int ] 20 bytes, The address the transaction is directed to.
    #   gas         [ str ] Integer of the gas provided for the transaction execution. 
    #                       eth_call consumes zero gas, but this parameter may be needed by 
    #                       some executions.
    #   gasPrice    [ int ] Integer of the gasPrice used for each paid gas
    #   value       [ str ] Integer of the value sent with this transaction
    #   data        [ int ] Hash of the method signature and encoded parameters. 
    #@Return     :
    # gas_used   [ dict  ] The amount of GAS used. 
    def get_gas_estimate( self, *args, **kwargs ):
        return self.api_call( "eth_estimateGas",[kwargs] )        

    #@Description: Returns the current gas price in wei.
    #@Method     : eth_gasPrice
    #@Parameters :	
    # tx_call_ob [ dict  ] A transaction receipt object, or null when no receipt was found.
    #  from        [ str ] 20 Bytes, The address the transaction is sent from.
    #  to          [ int ] 20 bytes, The address the transaction is directed to.
    #  gas         [ str ] Integer of the gas provided for the transaction execution. 
    #                      eth_call consumes zero gas, but this parameter may be needed by 
    #                      some executions.
    #  gasPrice    [ int ] Integer of the gasPrice used for each paid gas
    #  value       [ str ] Integer of the value sent with this transaction
    #  data        [ int ] Hash of the method signature and encoded parameters. 
    # blk_param  [ int   ] An int block number, or the str "latest", "earliest" or "pending"
    #@Return     :
    # gas_used   [ dict  ] a hex code of an integer representing the current gas price in wei.
    def get_gas_price( self ):
        return self.api_call( "eth_gasPrice", [] )
    
    #@Description: Returns the balance of the account of given address.
    #@Method     : eth_getBalance  
    #@Parameters :	
    # address    [ str  ] Astring representing the address (20 bytes) to check for balance
    # blk_param  [ int  ] An int block number, or str "latest", "earliest" or "pending"
    #@Return     :
    # balance    [ int  ] An integer of the current balance in wei.
    def get_balance( self, _address, _blk_param ):
        return self.api_call( "eth_getBalance", [str(_address),_blk_param] )

    #@Description: Returns the number of transactions in the block with the given block hash.
    #@Method     : eth_getBlockTransactionCountByHash  
    #@Parameters :
    # required:
    #  _blk_hash  [ str ] A string representing the hash (32 bytes) of a block
    #@Return     :
    # blk_tx_count[ dict] A hex code of the integer representing the number of transactions 
    #                      in the provided block
    def get_block_tx_count_by_hash( self, _blk_hash ):
        return self.api_call( "eth_getBlockTransactionCountByHash", [str(_blk_hash)] )        

    #@Description: Returns the number of transactions in the block with the given block num.
    #@Method     : eth_getBlockTransactionCountByNumber  
    #@Parameters :
    # _blk_number [ int ] an integer block number, or string "latest", "earliest" or "pending" 
    #@Return     :
    # blk_tx_count[ dict] A hex code of the integer representing the number of transactions 
    #                      in the provided block
    def get_block_tx_count_by_number( self, _blk_number ):
        return self.api_call( "eth_getBlockTransactionCountByNumber", [hex(_blk_number)] )
    
    #@Description: Returns the compiled smart contract code, if any, at a given address.
    #@Method     : eth_getCode
    #@Parameters :
    # _address    [ str ] 20 bytes, representing the address  of the code. 
    # _blk_paaram [ int ] An integer block number, or string "latest", "earliest" or "pending"
    #@Return     :
    # code        [ str ] A hex code of at the given address. 
    def get_code( self, _address, _blk_param ):
        return api_call( "eth_getCode", [str(_address),str(_blk_param)] ) 
    
    #@Description: Returns an array of all logs matching a given filter object.
    #@Method     : eth_getLogs
    #@Parameters :
    # filter_ob  [ dict  ] A transaction receipt object, or null when no receipt was found.
    #  address     [ str ] 20 Bytes, a string representing the address to check for balance
    #  fromBlock   [ int ] An int block number,or string "latest","earliest"(dflt) or "pending"
    #  toBlock     [ int ] An int block number,or string "latest","earliest"(dflt) or "pending"
    #  topics      [ list] 32 Bytes DATA topics. Topics are order-dependent.
    #  blockhash   [ str ] With the addition of EIP-234, blockHash restricts the logs returned 
    #                      to the single block with the 32-byte hash blockHash. Using blockHash
    #                      is equivalent to fromBlock = toBlock = the block number with hash 
    #                      blockHash. f blockHash is present in in the filter criteria, then
    #                      neither I fromBlock nor toBlock are allowed.
    #@Return     :
    # log_object [ dict  ] An array of log objects, or an empty array if nothing has changed since last poll.
    # For filters created with eth_newBlockFilter  
    #  return: 32 Bytes block hashes e.g. ["0x3454645634534..."]
    # For filters created with eth_newPendingTransactionFilter  
    #  return: 32 Bytes transaction hashes e.g. ["0x6345343454645..."].
    # For filters created with eth_newFilter  
    #  return: logs are objects with following params:
    #  removed     [ bool] true when the log was removed (chain reorganization). false if a valid log.
    #  logIndex    [ int ] The log index position in the block. null when its pending log.
    #  txIndex     [ int ] The tx index position log was created from. null when its pending log.
    #  txHash      [ str ] 32 Bytes, hash of the tx this log was created from. null when its pending log.
    #  blockHash   [ str ] 32 Bytes, hash of the block where this log was in. null if pending or pending log.
    #  blockNumber [ int ] The block number where this log was in. null if pending or pending log.
    #  address     [ str ] 20 Bytes, address from which this log originated.
    #  data        [ str ] 32 Bytes, contains one or more non-indexed arguments of the log.
    #  topics      [ list] 0,4,32 Bytes of indexed arguments. 
    def get_logs( self, _filter_object ):
        return self.api_call("eth_getLogs",[_filter_object] )
    
    #@Description: Returns the value from a storage position at a given address.
    #@Method     : eth_getStorageAt
    #@Parameters :
    # required: 
    #  _address    [ str ] 20 bytes, a string representing the address of the storage.
    #  _storage_pos[ str ] A hex code of the position in the storage 
    #  _blk_paaram [ int ] An integer block number, or string "latest", "earliest" or "pending"
    #@Return     :
    # storage_value[ str ] a hex code of the integer indicating the value of the storage position 
    #                      at the provided address
    def get_storage_at( self, _address, _storage_pos, _blk_param ):
        return self.api_call("eth_getStorageAt",[str(_address),_storage_pos,_blk_param])

    #@Description: Returns information about a transaction by block hash and transaction 
    #              index position.
    #@Method     : eth_getTransactionByBlockHashAndIndex
    #@Parameters :
    # required: 
    # _blk_hash   [  str ] 32 Bytes, Representing the hash of a block.
    # _tx_index_p [  str ] Hex, Of the integer representing the pos. in the block.  	
    #@Return     :
    # tx_object   [ dict ] A transaction object, or null when no transaction was found
    #  hash        [ str ] 32 Bytes,  hash of the transaction.
    #  nonce       [ str ] the number of txs made by the sender prior to this one.
    #  blockHash   [ str ] 32 Bytes hash of the block where this tx was in. null when pending.
    #  blockNumber [ str ] block number where this tx was in. null when its pending.
    #  txIndex     [ int ] tx index position in the block. null when its pending.
    #  from        [ str ] 20 Bytes address of the sender.
    #  to          [ str ] 20 Bytes address of the receiver. null when contract creation tx.
    #  value       [float] value tx in Wei.
    #  gasPrice    [float] gas price provided by the sender in Wei.
    #  gas         [float] gas provided by the sender.
    #  input       [ str ] the data send along with the transaction.
    def get_tx_by_block_hash_and_index( self,_tx_hash,_tx_index ):
        return self.api_call("eth_getTransactionByBlockHashAndIndex",[str(_tx_hash),str(_tx_index)])

    #@Description: Returns information about a transaction by block number and transaction
    #              index position.
    #@Method     : eth_getTransactionByBlockNumberAndIndex
    #@Parameters :
    # required: 
    # _blk_param  [  int ] Block number, or string "latest", "earliest" or "pending"
    # _tx_index_p [  str ] Hex, Of the integer representing the pos. in the block. 	
    #@Return     :
    # tx_object   [ dict ] A transaction object, or null when no transaction was found
    #  hash        [ str ] 32 Bytes,  hash of the transaction.
    #  nonce       [ str ] the number of txs made by the sender prior to this one.
    #  blockHash   [ str ] 32 Bytes hash of the block where this tx was in. null when pending.
    #  blockNumber [ str ] block number where this tx was in. null when its pending.
    #  txIndex     [ int ] tx index position in the block. null when its pending.
    #  from        [ str ] 20 Bytes address of the sender.
    #  to          [ str ] 20 Bytes address of the receiver. null when contract creation tx.
    #  value       [float] value tx in Wei.
    #  gasPrice    [float] gas price provided by the sender in Wei.
    #  gas         [float] gas provided by the sender.
    #  input       [ str ] the data send along with the transaction.
    def get_tx_by_block_number_and_index( self, _tx_number, _tx_index):
        return self.api_call("eth_getTransactionByBlockNumberAndIndex",[str(_tx_number),str(_tx_index)])
    
    #@Description: Returns information about a transaction for a given hash.
    #@Method     : eth_getTransactionByHash
    #@Parameters :
    # required: 
    # _tx_hash    [  str ] 32 Bytes, a string representing the hash of a transaction 	
    #@Return     :
    # tx_object   [ dict ] A transaction object, or null when no transaction was found
    #  hash        [ str ] 32 Bytes,  hash of the transaction.
    #  nonce       [ str ] the number of txs made by the sender prior to this one.
    #  blockHash   [ str ] 32 Bytes hash of the block where this tx was in. null when pending.
    #  blockNumber [ str ] block number where this tx was in. null when its pending.
    #  txIndex     [ int ] tx index position in the block. null when its pending.
    #  from        [ str ] 20 Bytes address of the sender.
    #  to          [ str ] 20 Bytes address of the receiver. null when contract creation tx.
    #  value       [float] value tx in Wei.
    #  gasPrice    [float] gas price provided by the sender in Wei.
    #  gas         [float] gas provided by the sender.
    #  input       [ str ] the data send along with the transaction.
    def get_tx_by_hash( self, _tx_hash ):
        return self.api_call("eth_getTransactionByHash",[str(_tx_hash)])

    #@Description: Returns the number of transactions sent from an address.
    #@Method     : eth_getTransactionCount
    #@Parameters :
    # required: 
    #  _address    [ str ] 20 bytes, a string representing address to check for tx count for
    #  _blk_param  [ int ] Integer, block number, or string "latest", "earliest" or "pending"
    #@Return     :
    # tx_count     [ int ] hex code of the integer representing the number of tx sent from 
    #                      this address.
    def get_tx_count( self,_address, _blk_param ):
        return self.api_call("eth_getTransactionCount",[str(_address),_blk_param])
    
    #@Description: Returns the number of uncles in a block from a block matching given block hash.
    #@Method     : eth_getUncleCountByBlockHash
    #@Parameters :
    # required: 
    # _blk_hash    [ str ] 32 Bytes, Represents the hash of a transaction
    #@Return     :
    # blk_tx_cnt   [ int ] a hex code of the integer representing the number of uncles in the 
    #                      provided block 
    def get_uncle_count_by_block_hash( self, _blk_hash):
        return self.api_call("eth_getUncleCountByBlockHash",[_blk_hash])
    
    #@Description: Returns the number of uncles in a block from a block matching given block hash.
    #@Method     : eth_getUncleCountByBlockHash
    #@Parameters :
    # required: 
    # _blk_hash    [ str ] 32 Bytes, Represents the hash of a transaction
    #@Return     :
    # blk_tx_cnt   [ int ] a hex code of the integer representing the number of uncles in the 
    #                      provided block 
    def get_uncle_count_by_block_number( self, _blk_number):
        return self.api_call("eth_getUncleCountByBlockNumber",[_blk_number])

    #@Description: Returns information about the 'Uncle' of a block by hash and the 
    #              Uncle index position.
    #@Method     : eth_getUncleByBlockHashAndIndex
    #@Parameters :
    # required: 
    # _blk_hash   [  str ] 32 Bytes, Representing the hash of a block.
    # _uncl_index [  str ] Hex, Of the integer representing the pos. in the block.
    #@Return     :
    # block       [ dict ] Block object, or null when no block was found
    #  number      [ int ] Block number. Null when the returned block is the pending block.
    #  hash        [ str ] 32 Bytes,hash of the block. Null if returned block is the pending block.
    #  parentHash  [ str ] 32 Bytes,hash of the parent block.
    #  nonce       [ str ] 8 Bytes,hash of the generated POW.Null if returned block is the pending block.
    #  sha3Uncles  [     ] 32 Bytes,SHA3 of the uncles data in the block.
    #  logsBloom   [     ] 256 Bytes,the bloom filter for the logs of the block. Null when pending block.
    #  txRoot      [     ] 32 Bytes,the root of the transaction trie of the block.
    #  stateRoot   [     ] 32 Bytes,the root of the final state trie of the block.
    #  receiptsRoot[     ] 32 Bytes,the root of the receipts trie of the block.
    #  miner       [     ] 20 Bytes,the address of the beneficiary to whom the mining rewards were given.
    #  difficulty  [ int ] The difficulty for this block.
    #  totalDiff   [ int ] The total difficulty of the chain until this block.
    #  extraData   [     ] The "extra data" field of this block.
    #  size        [ int ] Integer, the size of this block in bytes.
    #  gasLimit    [ int ] The maximum gas allowed in this block.
    #  gasUsed     [ int ] Total used gas by all transactions in this block.
    #  timestamp   [ ts  ] The unix timestamp for when the block was collated.
    #  uncles      [ list] Array of uncle hashes.
    def get_uncle_by_block_hash_and_index( self, _blk_hash,_uncle_index):
        return self.api_call("eth_getUncleByBlockHashAndIndex",[_blk_hash,_uncle_index])
    
    #@Description: Returns information about the 'Uncle' of a block by hash and the Uncle index position. 
    #              Uncle index position.
    #@Method     : eth_getUncleByBlockNumberAndIndex
    #@Parameters :
    # required: 
    # _blk_param  [  int ] Integer of block number or String "latest", "earliest" or "pending".
    # _uncl_index [  str ] Hex, Of the integer representing the pos. in the block.  	
    #@Return     :
    # block       [ dict ] Block object, or null when no block was found
    #  number      [ int ] Block number. Null when the returned block is the pending block.
    #  hash        [ str ] 32 Bytes,hash of the block. Null if returned block is the pending block.
    #  parentHash  [ str ] 32 Bytes,hash of the parent block.
    #  nonce       [ str ] 8 Bytes,hash of the generated POW.Null if returned block is the pending block.
    #  sha3Uncles  [     ] 32 Bytes,SHA3 of the uncles data in the block.
    #  logsBloom   [     ] 256 Bytes,the bloom filter for the logs of the block. Null when pending block.
    #  txRoot      [     ] 32 Bytes,the root of the transaction trie of the block.
    #  stateRoot   [     ] 32 Bytes,the root of the final state trie of the block.
    #  receiptsRoot[     ] 32 Bytes,the root of the receipts trie of the block.
    #  miner       [     ] 20 Bytes,the address of the beneficiary to whom the mining rewards were given.
    #  difficulty  [ int ] The difficulty for this block.
    #  totalDiff   [ int ] The total difficulty of the chain until this block.
    #  extraData   [     ] The "extra data" field of this block.
    #  size        [ int ] Integer, the size of this block in bytes.
    #  gasLimit    [ int ] The maximum gas allowed in this block.
    #  gasUsed     [ int ] Total used gas by all transactions in this block.
    #  timestamp   [ ts  ] The unix timestamp for when the block was collated.
    #  uncles      [ list] Array of uncle hashes.
    def get_uncle_by_block_number_and_index( self, _blk_number, _uncle_index):
        return self.api_call("eth_getUncleByBlockNumberAndIndex",[_blk_number,_uncle_index])
    
    #@Description: Returns the number of hashes per second that the node is mining with. Only 
    #              applicable when the node is mining.
    #@Method     : eth_hashrate
    #@Parameters : None
    #@Return     :
    # eth_hr      [float] the number of hashes per second that the node is mining with.
    def get_hash_rate( self ):
        return self.api_call("eth_hashrate",[])

    #@Description: Returns true if client is actively mining new blocks.
    #@Method     : eth_mining
    #@Parameters : None
    #@Return     :
    # is_mining   [ bool] a boolean indicating if the client is mining.
    # * NOTE *    Infura will always return false in response to eth_mining.
    def _is_mining( self ):
        return self.api_call("eth_mining",[])

    #@Description: Returns the current ethereum protocol version.
    #@Method     : eth_protocolVersion
    #@Parameters : None
    #@Return     :
    # version     [ str] Indicating the current ethereum protocol version.
    def get_protocol_version( self ):
        return self.api_call("eth_protocolVersion",[])

    #@Description: Returns an object with data about the sync status or false.
    #@Method     : eth_syncing
    #@Parameters : None 
    #@Return     :
    # syn_status   [ bool] Boolean, as false only when not syncing.
    # syn_blocks
    #  startBlock  [ int ] Hex code a hexcode of the integer indicating the block at 
    #                     which the import started. 
    #  currntBlock [ int ] Hex code a hexcode of the integer indicating the current block,
    #                     same as eth_blockNumber  
    #  highestBlock[ int ] a hexcode of the integer indicating the highest block. 
    def is_syncing( self ):
        return self.api_call("eth_syncing",[]) 
    
    #@Description: Returns true if client is actively listening for network connections.
    #@Method     : net_listening
    #@Parameters : None 
    #@Return     :
    # is_listening[ bool] indicating whether the client is actively listening for network 
    #                     connections
    def is_listening(self ):
        return self.api_call("net_listening",[])

    #@Description: Returns the number of peers currently connected to the client.
    #@Method     : net_peerCount
    #@Parameters : None 
    #@Return     :
    # peer_count  [ int ] The number of connected peers.
    def get_peer_count( self ):
        return self.api_call("net_peerCount",[])

    #@Description: Returns the current network id.
    #@Method     : net_version
    #@Parameters : None 
    #@Return     :
    # net_id      [ str ] String, representing the network ID.
    def get_net_version( self ):
        return self.api_call("net_version",[])

    #@Description: Returns the current client version.
    #@Method     : web3_clientVersion
    #@Parameters : None 
    #@Return     :
    # client_ver  [ str ] String,  The current client version.
    def get_client_version( self ):
        return self.api_call("web3_clientVersion",[])

    #@Description: Returns the hash of the current block, the seedHash, and the 
    #              boundary condition to be met ("target").
    #@Method     : eth_getWork
    #@Parameters : None 
    #@Return     :
    #  _work      [ list ]
    #   _hdr_hash  [ str ] 32 Bytes, Current block header pow-hash
    #   _seed_hash [ str ] 32 Bytes, The seed hash used for the DAG.
    #   _boundary  [float] 32 Bytes, Boundary condition ("target"), 2^256 / difficulty.
    #  * NOTE *    While Infura will allow this method, eth_getWork will never actually 
    #              return mining work.
    def get_work( self ):
        return self.api_call("eth_getWork",[]) 

    """ - Not Yet Implemented - """
    
    #@Description: Used for submitting a proof-of-work solution.
    #@Method     : eth_submitWork
    #@Parameters :  
    #  _work      [ list ]
    #   _nonce     [ int ] 8 Bytes , The nonce found (64 bits)
    #   _hdr_hash  [ str ] 32 Bytes, The header's pow-hash (256 bits)
    #   _digest    [ str ] 32 Bytes, The mix digest (256 bits)
    #@Return     :
    # is_valid_flag[ bool] Boolean, True if provided solution is valid, otherwise false.
    def submit_work( self ):
        pass 

    #@Description: Submits a pre-signed transaction for broadcast to the Ethereum network.
    #@Method     : eth_sendRawTransaction
    #@Parameters :
    # required: 
    # _tx_data    [ str ] The signed transaction data.
    #@Return     :
    # tx_hash     [ str ] 32 Bytes, the tx hash/ 0 hash if the tx is not yet available.  
    # * NOTE *    Infura will always return false in response to eth_mining.                      
    def send_raw_transaction( self, _tx_data={}):
        pass 


    
