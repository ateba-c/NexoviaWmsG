def is_probable_gs1(value: str) -> bool:
    return value.startswith("01") and len(value) >= 14

