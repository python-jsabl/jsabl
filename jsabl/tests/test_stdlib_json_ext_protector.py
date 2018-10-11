from json import JSONEncoder

import pytest

from jsabl import add_protection_to_json_encoder


def test_protection():
    """Tests that the protection method works"""

    class MyInt(int):
        pass

    # create an instance
    i = MyInt(12)

    # ------
    # 1- default json lib behaviour: the int is encoded :(
    std_lib_encoder = JSONEncoder()
    assert std_lib_encoder.encode(i) == '12'

    # ------
    # 2- an encoder for which we add the protection, but not the custom object hook
    dummy_encoder = JSONEncoder()
    add_protection_to_json_encoder(dummy_encoder)

    # should raise an error instead of encoding the int
    with pytest.raises(TypeError) as exc_info:
        dummy_encoder.encode(i)

    e = exc_info.value
    try:
        # raise the default exception ...
        JSONEncoder.default(None, i)
    except TypeError as e2:
        # ... so that we can compare
        assert str(e) == str(e2)
    else:
        # we should never reach this line, make sure of that.
        assert False

    # ------
    # 3- an encoder for which we add the protection AND the custom object hook should encode correctly
    def custom_object_hook(o):
        if isinstance(o, MyInt):
            return o
        else:
            # raise the default error message
            JSONEncoder.default(None, o)

    encoder = JSONEncoder(default=custom_object_hook)
    add_protection_to_json_encoder(encoder)

    assert encoder.encode(i) == '12'

    with pytest.raises(TypeError) as exc_info:
        encoder.encode(object())