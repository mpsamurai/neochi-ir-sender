from sender_notifications import StartIrSendingNotification
from sender_notifications import CompleteIrSendingNotification

class IrSender:

    def __init__(self):
        self.notified_val = None

        def callback(value):
            self.notified_val = value;

        StartIrSendingNotification.subscribe(callback)


    def get_signal_from_file(self, filename):
        with open(filename) as f:
            print(filename)  # TODO overwrite with actual process




    def send(self, id):

        # TODO with GPIO

        CompleteIrSendingNotification.value = id  # notify the end of sending


