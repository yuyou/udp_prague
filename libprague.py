from ctypes import (
    Structure,
    c_int,
    c_void_p,
    CDLL,
    POINTER,
    c_int32,
    c_uint8,
    c_bool,
    byref,
)
import time

from typing import Optional

# alias
from ctypes import c_uint64 as size_tp  # size in Bytes
from ctypes import (
    c_uint64 as window_tp,
)  # fractional window size in µBytes (to match time in µs, for easy Bytes/second rate calculations)
from ctypes import c_uint64 as rate_tp  # rate in Bytes/second
from ctypes import (
    c_int32 as time_tp,
)  # timestamp or interval in microseconds, timestamps have a fixed but no meaningful reference,
from ctypes import (
    c_int32 as count_tp,
)  # count in packets (or frames), signed because it can wrap around, and we need to compare both ways

# Load the shared library
_libprague = CDLL("./libprague.so")


# Define C structs here
class ecn_tp(c_uint8):
    ecn_not_ect = 0
    ecn_l4s_id = 1
    ecn_ect0 = 2
    ecn_ce = 3


# Define argument and return types for C++ functions
_libprague.create_praguecc.argtypes = None  # [ctypes.c_int]
_libprague.create_praguecc.restype = c_void_p
_libprague.delete_praguecc.argtypes = [c_void_p]
_libprague.delete_praguecc.restype = None
_libprague.Now.argtypes = [c_void_p]
_libprague.Now.restype = time_tp
_libprague.ResetCCInfo.argtypes = [c_void_p]
_libprague.ResetCCInfo.restype = None

_libprague.PacketReceived.argtypes = [c_void_p, time_tp, time_tp]
_libprague.PacketReceived.restype = c_bool

_libprague.ACKReceived.argtypes = [
    c_void_p,
    count_tp,
    count_tp,
    count_tp,
    count_tp,
    c_bool,
]
_libprague.ACKReceived.restype = count_tp


class LibPrague:

    _praguecc: c_void_p | None

    def __init__(self) -> None:
        self._praguecc = _libprague.create_praguecc()
        assert self._praguecc is not None

    def __del__(self) -> None:
        """Deletes an instance of Prague CC"""
        if self._praguecc:
            _libprague.delete_praguecc(self._praguecc)

    def now(self) -> int:
        if self._praguecc:
            return _libprague.Now(self._praguecc)
        return -1

    def resetCCInfo(self) -> None:
        if self._praguecc:
            _libprague.ResetCCInfo(self._praguecc)

    def packet_received(self, timestamp: int, echoed_timestamp: int) -> bool:
        # timestamp from peer, freeze and keep this time
        # echoed_timestamp
        _timestamp = time_tp(timestamp)
        _echoed_timestamp = time_tp(echoed_timestamp)

        result: c_bool = _libprague.PacketReceived(
            self._praguecc, _timestamp, _echoed_timestamp
        )
        return result

    def ack_received(
        self,
        packets_received: int,
        packets_CE: int,
        packets_lost: int,
        packets_sent: int,
        error_L4S: bool = False,
    ) -> int:
        #  call this when an ACK (or a Frame ACK) is received from peer.
        if self._praguecc:
            # _inflight: count_tp = count_tp(inflight) # default value
            _inflight: count_tp = _libprague.ACKReceived(
                self._praguecc,
                packets_received,
                packets_CE,
                packets_lost,
                packets_sent,
                error_L4S,
            )
            return _inflight
        else:
            return 0


# Main logic
if __name__ == "__main__":
    praguecc = LibPrague()
    print(f"{praguecc=}")
    time.sleep(1)
    now = praguecc.now()
    print(f"{now}")
    praguecc.resetCCInfo()
    time.sleep(0.1)
    result = praguecc.packet_received(123456, 123456)
    print(f"packet_received: {result}")
    inflight = praguecc.ack_received(20, 2, 0, 20, False)
    print(f"{inflight=}")
    print("done")
