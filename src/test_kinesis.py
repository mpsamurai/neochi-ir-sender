import time
import redis
from neochi.core.dataflow.notifications import brain as brain_notification
from neochi.core.dataflow.notifications import ir_sender as ir_sender_notification


server = redis.StrictRedis('redis')
detected_sleep = brain_notification.DetectedSleep(server)
detected_sleep.notify()