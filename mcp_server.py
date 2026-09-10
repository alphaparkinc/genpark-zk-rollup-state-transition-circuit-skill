import sys
import json
from client import ZKRollupStateTransition

rollup = ZKRollupStateTransition()

def handle_call(name, arguments):
    if name == "add_account":
        rollup.add_account(arguments["id"], arguments["balance"], arguments.get("nonce", 0))
        return {"root": rollup.compute_state_root()}
    elif name == "apply_batch":
        ok, res = rollup.apply_batch(arguments["transactions"])
        return {"success": ok, "root_or_error": res}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_call(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
