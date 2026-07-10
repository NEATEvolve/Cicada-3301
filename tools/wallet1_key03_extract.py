from __future__ import annotations

import argparse
import base64
import hashlib
import re
from pathlib import Path

from PIL import Image


XP_COMMENT_TAG = 0x9C9C

# The spaced underscore at the end of line two is the terminal cursor.
CIPHER_LINES = [
    "h( +) 4)# XYZ",
    "<^5 e!^4 +/?",
    "\\!56_^ e;8~",
]

CAPTION = (
    "At dawn the caretaker wandered through abandoned corridors where faded murals "
    "watched silent visitors and dust drifted beneath cracked arches. Beyond the "
    "library a scholar recorded strange rumors about distant beasts forgotten by time. "
    "Some accounts were contradictory while others seemed unsettlingly precise. "
    "If you seek the next clue ask me for the red monster's portrait today."
)

PHONE_B64 = "KDgzMykgMjM3LTgyOTg="

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_xp_comment(image_path: Path) -> str:
    with Image.open(image_path) as image:
        raw = image.getexif().get(XP_COMMENT_TAG)
    if raw is None:
        raise RuntimeError(f"XPComment tag not found in {image_path}")
    if isinstance(raw, bytes):
        return raw.decode("utf-16le").rstrip("\0")
    return str(raw).rstrip("\0")


def build_homophonic_key(xp_comment: str) -> dict[str, str]:
    key: dict[str, str] = {}
    for line in xp_comment.splitlines():
        parts = line.split()
        if len(parts) < 2 or len(parts[0]) != 1 or not parts[0].isalpha():
            continue
        letter = parts[0].upper()
        for symbol in parts[1:]:
            key[symbol] = letter

    # These symbols are used by the image but omitted from its XPComment table.
    # The sentence structure recovers them without changing any defined mapping.
    key.update({"/": "H", "\\": "H", "?": "E"})
    return key


def decode_visible_message(key: dict[str, str]) -> list[str]:
    return ["".join(key.get(char, char) for char in line) for line in CIPHER_LINES]


def select_caption_words() -> tuple[list[str], list[str]]:
    words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", CAPTION)
    selected = [words[index - 1] for index in range(50, 57)]
    return words, selected


def extract_red_lsb(image_path: Path, output_path: Path | None) -> tuple[int, tuple[int, int, int, int]]:
    with Image.open(image_path) as image:
        rgb = image.convert("RGB")

    width, height = rgb.size
    plane_values: list[int] = []
    xs: list[int] = []
    ys: list[int] = []

    for index, (red, _green, _blue) in enumerate(rgb.getdata()):
        bit = red & 1
        plane_values.append(bit * 255)
        if bit:
            xs.append(index % width)
            ys.append(index // width)

    if not xs:
        raise RuntimeError("Red-channel LSB contains no set pixels")

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plane = Image.new("L", (width, height))
        plane.putdata(plane_values)
        plane.save(output_path)

    return len(xs), (min(xs), min(ys), max(xs), max(ys))


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce Wallet 1 Key_03 image and caption transforms.")
    parser.add_argument(
        "--canonical-jpeg",
        type=Path,
        default=Path("Wallet-1/Key_03/Assets/e69a7acec6b.jpg"),
    )
    parser.add_argument(
        "--portrait",
        type=Path,
        default=Path("Wallet-1/Key_03/Assets/red-monster.png"),
    )
    parser.add_argument(
        "--lsb-output",
        type=Path,
        help="Optional path for the full red-channel LSB visualization.",
    )
    args = parser.parse_args()

    xp_comment = read_xp_comment(args.canonical_jpeg)
    homophonic_key = build_homophonic_key(xp_comment)
    decoded_lines = decode_visible_message(homophonic_key)
    caption_words, selected_words = select_caption_words()
    one_bits, bbox = extract_red_lsb(args.portrait, args.lsb_output)
    phone = base64.b64decode(PHONE_B64).decode("ascii")

    print(f"key_03_canonical_jpeg_sha256={sha256_file(args.canonical_jpeg)}")
    print(f"key_03_message={' / '.join(decoded_lines)}")
    print(f"key_03_phone={phone}")
    print(f"key_03_caption_word_count={len(caption_words)}")
    print(f"key_03_caption_50_56={' '.join(selected_words)}")
    print(f"key_03_caption_word_57={caption_words[56]}")
    print(f"key_03_portrait_sha256={sha256_file(args.portrait)}")
    print(f"key_03_red_lsb_one_bits={one_bits}")
    print(f"key_03_red_lsb_bbox={','.join(str(value) for value in bbox)}")
    if args.lsb_output is not None:
        print(f"key_03_red_lsb_output={args.lsb_output}")


if __name__ == "__main__":
    main()
