# Tools

Small reproducibility helpers used by the Wallet 1 writeups.

## `wallet1_key01_extract.py`

Decodes the starting media for Key 01 and Key 02:

- Key 01 `Clue-1.mp4` Morse audio
- Key 02 `Clue-1.png` dark QR payload

Run from the repository root:

```powershell
python tools\wallet1_key01_extract.py --ffmpeg <path-to-ffmpeg>
```

If `ffmpeg` is already on `PATH`, the `--ffmpeg` argument can be omitted.

Python dependencies:

```text
opencv-python
numpy
```

## `wallet1_x_cipher_decode.py`

Reproduces the homophonic substitution decode for the Key 02 X profile bio:

```powershell
python tools\wallet1_x_cipher_decode.py
```

Expected plaintext:

```text
IN THE PAGE TWENTY YOU SHALL FIND YOUR WAY
```
