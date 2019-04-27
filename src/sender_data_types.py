from neochi.core.dataflow.data_types import Str


class IRSenderState(Str):
    def __init__(self, state):
        self._states = {
            "BOOTING": "booting",
            "READY": "ready",
            "SENDING": "sending",
            "DEAD": "dead"
        }

        self._state = state




