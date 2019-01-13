#!/usr/bin/python3
import sys, os, time
import infura as inf
import json

_PROJECT_ID   = ""
_PROJECT_SCRT = ""

       
# Description : Unit testing infura.py
def main():
    
    #-- Start test  Node information 
    remoteNode   = inf.INFURA(_PROJECT_ID,_PROJECT_SCRT)
    
    # test 1 : endpoint 
    print()   
    print("Testing : get_url ()  .. ")
    print("Return  : {} ".format(remoteNode.get_url()))
    print()
    
    # test 2 : get_accounts 
    print("Testing : get_accounts() .. ")
    print("Return  : {} ".format(remoteNode.get_accounts()))
    print()
    
    # test 3 : get_block_number() 
    print("Get the latest block .. ")
    _latest_block_number = remoteNode.get_block_number()
    print("Return :  {} ".format(_latest_block_number))
    print() 
    
    # test 4 : Make Ethereum call
    params = {} 
    print("Testing : make_eth_call() .. ")
    _eth_call = remoteNode.make_eth_call("latest",params)
    print("Return  :  {} ".format(_eth_call))
    print()
    
    # test 5 : get gas estimate 
    params = {"from": "0xb60e8dd61c5d32be8058bb8eb970870f07233155",
                  "to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567",
                  "gas": "0x76c0",
                  "gasPrice": "0x9184e72a000",
                  "value": "0x9184e72a",
                  "data": "0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675"
                  }
    print("Testing : get_gas_estimate() .. ")
    _eth_estimateGas = remoteNode.get_gas_estimate(params)
    print("Return  :  {} ".format(_eth_estimateGas))
    print()
        
    # test 6 : get gas price 
    print("Testing : get_gas_prace() .. ")
    _eth_estimatePrice = remoteNode.get_gas_price()
    print("Return  :  {} ".format(_eth_estimatePrice))
    print()
            
    # test 7 : get balances at specified address.  
    print("Testing : get_balance() .. ")
    _account_address = "0xc94770007dda54cF92009BFF0dE90c06F603a09f"
    _eth_balance = remoteNode.get_balance(_account_address,'latest')
    print("Return  :  {} ".format(_eth_balance))
    print()
                
    # test 8 : get block transaction count by block hash.  
    print("Testing : get_block_tx_count_by_hash() .. ")
    _hash = "0xb3b20624f8f0f86eb50dd04688409e5cea4bd02d700bf6e79e9384d47d6a5a35"
    _eth_tx_count = remoteNode.get_block_tx_count_by_hash(_hash)
    print("Return  :  {} ".format(_eth_tx_count))
    print()
                
    # test 9 : get block transaction count by block number  
    print("Testing : get_block_tx_count_by_number() .. ")
    _block_number = _latest_block_number
    _eth_tx_count = remoteNode.get_block_tx_count_by_number(_block_number)
    print("Return  :  {} ".format(_eth_tx_count))
    print()
                
    # test 10 : get block transaction count by block number  
    params = {
        "blockHash":"0x7c5a35e9cb3e8ae0e221ab470abae9d446c3a5626ce6689fc777dcffcab52c70",
        "topics":["0x241ea03ca20251805084d27d4440371c34a0b85ff108f6bb5611248f73818b80"]
        }
    print("Testing : get_logs() .. ")
    _eth_logs = remoteNode.get_logs(params)
    print("Return  :  {} ".format(json.dumps(_eth_logs,indent=4)))
    print()

    # test 11 :
    _address     = "0x295a70b2de5e3953354a6a8344e616ed314d7251"
    _storage_pos = "0x6661e9d6d8b923d5bbaab1b96e1dd51ff6ea2a93520fdc9eb75d059238b8c5e9"
    _block_param = "0x65a8db"
    print("Testing : get_storage_at() .. ")
    _data_at_storage = remoteNode.get_storage_at(_address, _storage_pos,_block_param)
    print("Return  :  {} ".format(_data_at_storage))
    print()

    # test 12 : Get a tx by specifying the block hash and the tx position 
    _blk_hash = "0xb3b20624f8f0f86eb50dd04688409e5cea4bd02d700bf6e79e9384d47d6a5a35"
    _tx_index = "0x0"
    print("Testing :get_tx_by_block_hash_and_index() .. ")
    _tx = remoteNode.get_tx_by_block_hash_and_index(_blk_hash,_tx_index)
    print("Return  :  {} ".format(_tx))
    print()

    # test 13 : Get a tx by specifying the block number and the tx position 
    _blk_param = "0x5BAD55"
    _tx_index  = "0x0"
    print("Testing :get_tx_by_block_number_and_index() .. ")
    _tx = remoteNode.get_tx_by_block_number_and_index(_blk_param,_tx_index)
    print("Return  :  {} ".format(_tx))
    print()

    # test 14 :  Get information about a txgiven it's transaction hash
    _tx_hash  = "0xbb3a336e3f823ec18197f1e13ee875700f08f03e2cab75f0d0b118dabb44cba0"
    print("Testing :get_tx_by_hash() .. ")
    _tx = remoteNode.get_tx_by_hash(_tx_hash)
    print("Return  :  {} ".format(_tx))
    print()
    
    # test 15 : Get a tx count given a block  
    _address   = "0xc94770007dda54cF92009BFF0dE90c06F603a09f"
    _blk_param = "0x5bad55"
    print("Testing : get_tx_count() .. ")
    _tx_count = remoteNode.get_tx_count(_address,_blk_param)
    print("Return  :  {} ".format(_tx_count))
    print()
        
    # test 16 : Get the number of uncles for a givn block hash.    
    _block_hash = "0xb3b20624f8f0f86eb50dd04688409e5cea4bd02d700bf6e79e9384d47d6a5a35"
    _uncle_pos  = "0x0"
    print("Testing : get_uncle_count_by_block_hash() .. ")
    _tx = remoteNode.get_uncle_count_by_block_hash(_block_hash) 
    print("Return  :  {} ".format(_tx))
    print()
        
    # test 17 : Get the number of uncles for a givn block hash.
    _block_number = "0x29c"
    print("Testing : get_uncle_count_by_block_number() .. ")
    _tx = remoteNode.get_uncle_count_by_block_number(_block_number) 
    print("Return  :  {} ".format(_tx))
    print()
        
    # test 18 : Get the number of uncles for a givn block hash.    
    _block_hash   = "0xb3b20624f8f0f86eb50dd04688409e5cea4bd02d700bf6e79e9384d47d6a5a35"
    _uncle_index  = "0x0"
    print("Testing : get_uncle_by_block_hash_and_index() .. ")
    _tx = remoteNode.get_uncle_by_block_hash_and_index(_block_hash,_uncle_index) 
    print("Return  :  {} ".format(_tx))
    print()
        
    # test 19 : Get the number of uncles for a givn block hash.
    _block_number = "0x29c"
    _uncle_index = "0x0"
    print("Testing : get_uncle_by_block_number_and_index() .. ")
    _tx = remoteNode.get_uncle_by_block_number_and_index(_block_number,_uncle_index) 
    print("Return  :  {} ".format(_tx))
    print()
    
    # test 20 : Get the hash rate 
    print("Testing : get_hash_rate() .. ")
    _tx = remoteNode.get_hash_rate() 
    print("Return  :  {} ".format(_tx))
    print()

    # test 21 : Check if the node is a mining node, or it it's mining. 
    print("Testing : _is_minining() .. ")
    _tx = remoteNode._is_mining() 
    print("Return  :  {} ".format(_tx))
    print()
    
    # test 22 : Get the hash rate 
    print("Testing : get_protocol_version() .. ")
    _tx = remoteNode.get_protocol_version() 
    print("Return  :  {} ".format(_tx))
    print()
    
    # test 23 : Returns an object with data about the sync status or false.
    print("Testing : is_syncing() .. ")
    _tx = remoteNode.is_syncing() 
    print("Return  :  {} ".format(_tx))
    print()
    
    # test 24 : Returns true if client is actively listening for network connections.
    print("Testing : is_listening() .. ")
    _tx = remoteNode.is_listening() 
    print("Return  :  {} ".format(_tx))
    print()
        
    # test 25 : number of peers currently connected to the client.
    print("Testing : get_peer_count() .. ")
    _tx = remoteNode.get_peer_count() 
    print("Return  :  {} ".format(_tx))
    print()
        
    # test 26 : Returns the current network id.
    print("Testing : get_net_version() .. ")
    _tx = remoteNode.get_net_version() 
    print("Return  :  {} ".format(_tx))
    print()
            
    # test 27 : Returns the current client version.
    print("Testing : get_client_version() .. ")
    _tx = remoteNode.get_client_version() 
    print("Return  :  {} ".format(_tx))
    print()

            
    # test 28 : number of peers currently connected to the client.
    print("Testing : get_work() .. ")
    _tx = remoteNode.get_work() 
    print("Return  :  {} ".format(_tx))
    print()
    


    
    
    #print("Done plotting  pandas data frame boxplot .. ")
    
if __name__ == "__main__":
    main() 
