from hashlib import blake2b


def generate_uuid(stock_names: str) -> str:
    """Generating unique config hash with 8 characters

    :param stock_names: string of all names
    :return: unique config hash with 8 characters
    """
    hash_object = blake2b(stock_names.encode('UTF-8'), digest_size=4)
    return hash_object.hexdigest()
