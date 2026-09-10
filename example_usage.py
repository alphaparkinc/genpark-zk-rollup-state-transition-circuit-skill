from client import ZKRollupStateTransition

def main():
    print("=== Testing ZK-Rollup State Transition Circuit ===")
    rollup = ZKRollupStateTransition()
    rollup.add_account("Alice", 100, nonce=0)
    rollup.add_account("Bob", 50, nonce=0)

    old_root = rollup.compute_state_root()
    print(f"Initial state root: {old_root[:16]}...")

    txs = [{"from": "Alice", "to": "Bob", "amount": 25, "nonce": 0}]
    ok, new_root = rollup.apply_batch(txs)
    print(f"Batch applied successfully: {ok}. New state root: {new_root[:16]}...")

    assert ok is True
    assert rollup.accounts["Alice"]["balance"] == 75
    assert rollup.accounts["Bob"]["balance"] == 75
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
