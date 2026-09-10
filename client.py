import hashlib

class ZKRollupStateTransition:
    """
    ZK-Rollup State Transition Verification.
    Validates batched transfer transactions:
    - Balances >= transfer amount
    - Nonces sequential
    - State root commitment correctly transitions from old_root to new_root
    """
    def __init__(self):
        self.accounts = {}

    def add_account(self, acc_id, balance, nonce=0):
        self.accounts[acc_id] = {'balance': balance, 'nonce': nonce}

    def compute_state_root(self):
        acc_str = ";".join(f"{k}:{v['balance']}:{v['nonce']}" for k, v in sorted(self.accounts.items()))
        return hashlib.sha256(acc_str.encode()).hexdigest()

    def apply_batch(self, transactions):
        for tx in transactions:
            sender = self.accounts.get(tx['from'])
            receiver = self.accounts.get(tx['to'])
            if not sender or not receiver:
                return False, "Account not found"
            if sender['nonce'] != tx['nonce']:
                return False, "Nonce mismatch"
            if sender['balance'] < tx['amount']:
                return False, "Insufficient balance"

            sender['balance'] -= tx['amount']
            sender['nonce'] += 1
            receiver['balance'] += tx['amount']

        return True, self.compute_state_root()
