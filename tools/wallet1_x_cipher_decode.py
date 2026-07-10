from __future__ import annotations

from string import ascii_uppercase


BIO_CIPHER = (
    "02 12 / 06 14 22 / 26 21 17 28 / "
    "96 13 22 12 96 08 / 08 18 16 / "
    "30 14 21 07 42 / 05 41 12 20 / "
    "08 85 94 49 / 13 40 08"
)

# X displays newest posts first. Treat the newest post as A and continue A-Z.
POST_GROUPS_NEWEST_FIRST = [
    "21 27 31 40",
    "15",
    "01 33",
    "20 34",
    "22 28 32 36 37",
    "05",
    "17",
    "14",
    "02 29 38 41",
    "19",
    "03",
    "07 39 42",
    "09 43",
    "12 48 97",
    "18 60 85",
    "26 44",
    "25",
    "24 49",
    "10 30 45 99",
    "06 96 55",
    "16 94",
    "23",
    "13",
    "11",
    "08",
    "04",
]


def build_homophonic_key(groups: list[str]) -> dict[str, str]:
    key: dict[str, str] = {}
    for letter, group in zip(ascii_uppercase, groups):
        for token in group.split():
            key[token] = letter
    return key


def decode(cipher_text: str, key: dict[str, str]) -> str:
    words: list[str] = []
    for word in cipher_text.split(" / "):
        words.append("".join(key.get(token, "?") for token in word.split()))
    return " ".join(words)


def main() -> None:
    newest_first_key = build_homophonic_key(POST_GROUPS_NEWEST_FIRST)
    oldest_first_key = build_homophonic_key(list(reversed(POST_GROUPS_NEWEST_FIRST)))
    print(f"newest_first={decode(BIO_CIPHER, newest_first_key)}")
    print(f"oldest_first={decode(BIO_CIPHER, oldest_first_key)}")


if __name__ == "__main__":
    main()
