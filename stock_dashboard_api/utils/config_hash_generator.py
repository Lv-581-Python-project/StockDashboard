import uuid


def generate_uuid(all_config_hashes: list) -> str:
    """Generating unique config hash with 8 characters

    :param all_config_hashes: list of all hashes in Dashboard table
    :return: unique config hash with 8 characters
    """
    config_hash = str(uuid.uuid4())[:8]
    while config_hash in all_config_hashes:
        config_hash = str(uuid.uuid4())[:8]
    return config_hash
