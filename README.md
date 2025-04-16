
# Timing Attack Simulation (C + Python)

This project demonstrates how a timing side-channel can leak a secret string and how a constant-time comparison fixes it.

## Contents
- `src/leaky.c` — Insecure string compare that leaks time per matching byte.
- `src/fixed.c` — Constant-time style compare that removes the leak.
- `scripts/attack.py` — Python script that recovers the secret from the leaky binary using timing.
- `Makefile` — Build targets for both binaries.

## Build
```sh
make
```

This produces two binaries: `./leaky` and `./fixed`.

## Run the attack
```sh
cd scripts
# Attack the leaky binary (default TRIALS=5; increase for stability)
python3 attack.py
# or specify env vars
BIN=../leaky TRIALS=8 python3 attack.py
```

You should see the script recover the secret one character at a time by choosing the character that makes the program run the longest.

## Verify the fix
Try pointing the attack at the constant-time binary:
```sh
BIN=../fixed python3 attack.py
```
The recovery should fail, because runtime is (much more) independent of how many prefix characters match.

## Notes
- The demo artificially amplifies the leak using a `usleep(2000)` per matched byte to make timing differences clear and stable.
- Real-world leaks are smaller and noisier; practitioners collect many more samples and use statistics to distinguish signals.
- Constant-time programming avoids data-dependent branches and memory accesses on secrets and executes the same number of operations regardless of the secret value.
