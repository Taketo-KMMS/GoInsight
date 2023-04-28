import unicodedata


def normalize_string(s: str):
    return unicodedata.normalize("NFKC", s)
