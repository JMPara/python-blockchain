from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT

class Blockchain:
    """
    A cryptocurrency's blockchain is it's public ledger of transactions.
    It is implimented by a list of blocks
    """
    
    def __init__(self):
        self.chain = [Block.genesis()]
        
    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))
        
    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        """
        Replace the chain with the incoming chain if the following applies
            - The incoming chain is longer than the local one
            - The incoming chain is formatted properly
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace, the incoming chain must be longer.')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace, the incoming chain is invalid: {e}')

        self.chain = chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a Blockchain instance.
        The result will contain a chain list of Block instances.
        """
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json), chain_json)
        )

        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain
        Enforce the rules of the blockchain:
            - chain must start with the Genesis block
            - blocks must be formatted correctly
        """
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid.')
        
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_validblock(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of blocks of transactions
            - Each transaction only appears once in the chain
            - Only one mining reward per block
            - Each transaction itself must be valid
        """
        transaction_ids = set()

        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction {transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            'There can be only one mining reward per block. '\
                                f'Check block with hash {block.hash}'
                        )
                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(
                            f'Transaction {transaction.id} has an invalid '\
                            'input amount'
                        )

                Transaction.is_valid_transaction(transaction)

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)

    print(f'blockchain.py__name__: {__name__}')

if __name__ == '__main__':
    main()