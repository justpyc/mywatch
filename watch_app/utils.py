#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base64 import b64encode,b64decode

def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj

def byte_to_str(o):
    if isinstance(o, bytes):
        return str(o, encoding="utf-8")
    elif isinstance(o, str):
        return o
    else:
        raise TypeError(str(type(o)))

def string_to_bytes(o):
    if isinstance(o, str):
        return bytes(o,encoding="utf-8")
    elif isinstance(o, bytes):
        return o
    else:
        raise TypeError(str(type(o)))

def my_base64_encode(o):
    b = b64encode(string_to_bytes(byte_to_str(o)))
    return byte_to_str(b)

def my_base64_decode(o):
    return byte_to_str(b64decode(o))


# if __name__ == "__main__":
#     s = "duanbin"
#     print(string_to_bytes(s))
#     encode = my_base64_encode(s)
#     print(encode)
#     print(my_base64_decode(encode))