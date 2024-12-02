from ctypes import Structure, c_int, c_void_p, CDLL, POINTER, c_int32
import time

from typing import Optional

# alias
from ctypes import c_int32 as time_tp

# Load the shared library
libprague = CDLL("./libprague.so")


# Define C structs here


# Define argument and return types for C++ functions
libprague.create_praguecc.argtypes = None # [ctypes.c_int]
libprague.create_praguecc.restype = c_void_p
libprague.delete_praguecc.argtypes = [c_void_p]
libprague.delete_praguecc.restype = None
libprague.Now.argtypes = [c_void_p]
libprague.Now.restype = time_tp


class LibPrague:

    instance: c_void_p | None

    def __init__(self) -> None:
        self.instance = libprague.create_praguecc()
        assert(self.instance is not None)


    def __del__(self) -> None:
        """Deletes an instance of Prague CC"""
        if self.instance:
            libprague.delete_praguecc(self.instance)

    def now(self) -> int:
        if self.instance:
            return libprague.Now(self.instance)
        return -1
    
# Main logic
if __name__ == "__main__":
    praguecc = LibPrague()
    print (f"{praguecc=}")
    time.sleep(1)
    now = praguecc.now()
    print (f"{now}")

    print ("done")