from typing import Union
import hashlib
import os
from environs import Env
import canvasapi
import base64


def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29

    :return: bytes representation of the CSCI salt
    """
    return bytes.fromhex(os.environ["CSCI_SALT"])


def get_csci_pepper() -> bytes:
    """Returns the appropriate pepper for CSCI E-29

    This is similar to the salt, but defined as the UUID of the Canvas course,
    available from the Canvas API.

    This value should never be recorded or printed.

    :return: bytes representation of the pepper
    """

    env = Env()
    canvas = canvasapi.Canvas(env.str("CANVAS_URL"), env.str("CANVAS_TOKEN"))
    course = canvas.get_course(env.int("CANVAS_COURSE_ID"))
    return base64.b64decode(course.uuid)


def hash_str(some_val: Union[str, bytes], salt: Union[str, bytes] = "") -> bytes:
    """Converts strings to hash digest

    See: https://en.wikipedia.org/wiki/Salt_(cryptography)

    :param some_val: thing to hash, can be str or bytes
    :param salt: Add randomness to the hashing, can be str or bytes
    :return: sha256 hash digest of some_val with salt, type bytes
    """

    if type(some_val) == str:
        hash_input = some_val.encode()
    else:
        hash_input = some_val
    if type(salt) == str:
        salt_input = salt.encode()
    else:
        salt_input = salt

    m = hashlib.sha256()
    m.update(salt_input)
    m.update(hash_input)
    return m.digest()


def get_user_id(username: str) -> str:
    """returns user id as defined for this project
    param username: the github username of the user
    """

    salt = get_csci_salt() + get_csci_pepper()
    return hash_str(username.lower(), salt=salt).hex()[:8]
