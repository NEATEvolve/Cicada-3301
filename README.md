# Cicada-3301
The hunt begins anew.

## Description
Cicada 3301 has appeared to have made a return on pump.fun (https://pump.fun/coin/Dur39Hv43Uw4HU9Zr4RUB7mH6kqmYdPpZfENup6Xpump?clip=20260704_112742%3A2344277_20260704_112429). This repository will act as a documentary in the progress in solving the puzzles, riddles, and challenges set forth by Cicada 3301. Beginning with the first clue here at the link pasted from before.

## LARP
![](Assets/I-AM-INTELLIGENT.gif)

# Cicada 3301 Wallet Hunt

This repository documents the 2026 Cicada 3301 wallet hunt centered on the
`$3301` token and the deployed bounty wallets.

The notes here are written as a reproducible investigation log: each key
walkthrough records the clue surface, the transform that was applied, the
evidence that supported it, and the resulting fragment.

## Wallets

- [Wallet 1](Wallet-1/README.md)

## Current Public Package

The public-facing Wallet 1 package currently covers:

- [Key 01 / Fragment 1](Wallet-1/Key_01/README.md)
- [Key 02 / Fragment 2](Wallet-1/Key_02/README.md)
- [Key 03 / Master Decryption Key](Wallet-1/Key_03/README.md)
- [Wallet 1 fragments](Wallet-1/Fragments.md)

The package now documents the complete public puzzle chain through the final
master decryption key. It intentionally excludes the server-returned wallet
private key, seed phrases, signing material, and transaction instructions.

## How The Hunt Works

See [How-The-Hunt-Works.md](How-The-Hunt-Works.md) for the hunt flow: receive a
clue, solve its puzzle chain, validate the fragment, complete the final
decryptor hunt, and unlock the wallet.

## Repository Layout

```text
Wallet-1/
  README.md
  Fragments.md
  Investigation-Log.md
  Release-Post.md
  Key_01/
    README.md
    Clues/
    Assets/
  Key_02/
    README.md
    Clues/
    Assets/
  Key_03/
    README.md
    Clues/
    Assets/
tools/
  wallet1_key01_extract.py
  wallet1_key03_extract.py
  wallet1_x_cipher_decode.py
```

## Safety Note

Do not publish seed phrases, wallet private keys, signing material, or transaction
plans. The Key 03 walkthrough stops at the public master input and does not
perform the final server action that returns wallet-private material.
