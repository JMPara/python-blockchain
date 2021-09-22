import hashlib
import json

def crypto_hash(*args):
    """
    Returns the sha-256 hash for the given arguments.
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = ''.join(stringified_args)

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"Crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"Crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")

if __name__ == '__main__':
    main()