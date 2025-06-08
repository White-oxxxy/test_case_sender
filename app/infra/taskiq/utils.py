import random
import string


def generate_random_strings(n: int) -> list[str]:
    strings: list[str] = [''.join(random.choices(string.ascii_letters + string.digits, k=16)) for _ in range(n)]

    return strings
