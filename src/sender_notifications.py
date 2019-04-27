from neochi.core.dataflow.notifications import BaseNotification
from neochi.core.dataflow.data_types import Int


class StartIrSendingNotification(BaseNotification):
    data_type_cls = Int
    channel = 'start_ir_sending'


class CompleteIrSendingNotification(BaseNotification):
    data_type_cls = Int
    channel = 'complete_ir_sending'

