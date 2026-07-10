from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

import cv2
import numpy as np


MORSE = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    ".-.-.-": ".",
    "-..-.": "/",
}


def caesar_letters(text: str, shift: int) -> str:
    out: list[str] = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)


def decode_qr(image_path: Path) -> tuple[str, str]:
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(image_path)

    detector = cv2.QRCodeDetector()
    for threshold in range(1, 129):
        _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        bordered = cv2.copyMakeBorder(binary, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=255)
        scaled = cv2.resize(bordered, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
        decoded, _, _ = detector.detectAndDecode(scaled)
        if decoded:
            return decoded, f"threshold={threshold}"
    raise RuntimeError("QR decode failed")


def read_audio(ffmpeg: Path, media_path: Path, sample_rate: int) -> np.ndarray:
    command = [
        str(ffmpeg),
        "-v",
        "error",
        "-i",
        str(media_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-f",
        "s16le",
        "pipe:1",
    ]
    raw = subprocess.check_output(command)
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def decode_morse(ffmpeg: Path, media_path: Path, sample_rate: int = 8000) -> tuple[str, str]:
    audio = read_audio(ffmpeg, media_path, sample_rate)
    window = max(1, int(sample_rate * 0.01))
    usable = audio[: len(audio) // window * window]
    env = np.sqrt(np.mean(usable.reshape(-1, window) ** 2, axis=1))
    threshold = max(float(env.max()) * 0.25, 1e-4)
    active = env > threshold

    runs: list[tuple[bool, int]] = []
    current = bool(active[0])
    start = 0
    for idx, value in enumerate(active[1:], 1):
        value = bool(value)
        if value != current:
            runs.append((current, idx - start))
            current = value
            start = idx
    runs.append((current, len(active) - start))
    runs = [(is_on, length) for is_on, length in runs if length >= 2]
    while runs and not runs[0][0]:
        runs.pop(0)
    while runs and not runs[-1][0]:
        runs.pop()

    letters: list[str] = []
    current_symbol = ""
    for is_on, length in runs:
        duration = length * 0.01
        if is_on:
            current_symbol += "." if duration < 0.15 else "-"
        elif duration >= 0.15:
            if current_symbol:
                letters.append(current_symbol)
                current_symbol = ""
        else:
            continue
    if current_symbol:
        letters.append(current_symbol)

    morse = " ".join(letters)
    text = "".join(MORSE.get(symbol, "?") for symbol in letters)
    return morse, text


def normalize_qr_payload(decoded: str) -> str:
    marker = "->"
    if marker not in decoded:
        return decoded
    shift_text, payload = decoded.split(marker, 1)
    shift = -int(shift_text.strip())
    plaintext = caesar_letters(payload.strip(), shift)
    return (
        plaintext.replace("dot", ".")
        .replace("slash", "/")
        .replace("www.x.com", "https://www.x.com")
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Decode Wallet 1 Key_01 and Key_02 starting clues.")
    parser.add_argument(
        "--ffmpeg",
        type=Path,
        default=Path(os.environ.get("FFMPEG", "ffmpeg")),
    )
    parser.add_argument(
        "--key-01-clue-1",
        dest="key_01_clue_1",
        type=Path,
        default=Path("Wallet-1/Key_01/Clues/Clue-1.mp4"),
    )
    parser.add_argument(
        "--key-02-clue-1",
        dest="key_02_clue_1",
        type=Path,
        default=Path("Wallet-1/Key_02/Clues/Clue-1.png"),
    )
    args = parser.parse_args()

    morse, morse_text = decode_morse(args.ffmpeg, args.key_01_clue_1)
    qr_raw, qr_method = decode_qr(args.key_02_clue_1)
    qr_normalized = normalize_qr_payload(qr_raw)

    print(f"key_01_clue_1_morse={morse}")
    print(f"key_01_clue_1_text={morse_text}")
    print(f"key_02_clue_1_method={qr_method}")
    print(f"key_02_clue_1_qr_raw={qr_raw}")
    print(f"key_02_clue_1_normalized={qr_normalized}")


if __name__ == "__main__":
    main()
