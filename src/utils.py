import hashlib


def load_cleanfiles():
    with open("src/cleanfiles", "r") as f:
        lines = f.readlines()
    print(lines)


def calculate_hash_of_file_content():
    with open("src/cleanfiles", "rb") as f:
        f_byte = f.read()
        result = hashlib.sha256(f_byte)
        print(result.hexdigest())


load_cleanfiles()
calculate_hash_of_file_content()
