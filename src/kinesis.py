# MIT License
#
# Copyright (c) 2019 Morning Project Samurai (MPS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


__author__ = 'Junya Kaneko <junya@mpsamurai.org>'


import time
import redis
from neochi.core.dataflow.notifications import (brain as brain_notification,
                                                clap_detector as clap_detector_notification,
                                                ir_sender as ir_sender_notification)
from neochi.core.dataflow.data import kinesis as kinesis_data


class BaseController:
    def __init__(self, request_notification, response_notification):
        self._request_notification = request_notification
        self._response_notification = response_notification
        self._response_notification.subscribe(self._response_notification_callback)
        self._is_completed = False

    def _response_notification_callback(self, value, channel):
        print('complete', channel, value)
        self._is_completed = True

    def execute(self, parameters):
        self._is_completed = False
        self._request_notification.value = parameters
        while not self._is_completed:
            time.sleep(0.1)


class IrController(BaseController):
    def __init__(self, server):
        started_ir_sending = ir_sender_notification.StartIrSending(server)
        completed_ir_sending = ir_sender_notification.CompleteIrSending(server)
        super().__init__(started_ir_sending, completed_ir_sending)


class Kinesis:
    controller_classes = {'ir': IrController}

    def __init__(self, server):
        self._server = server
        self._action_plan = kinesis_data.ActionPlan(server)
        self._action_plan_detail = kinesis_data.ActionPlanDetail(server)
        self._detector_notifications = []
        self._controllers = {
            device:controller(server) for device, controller in self.controller_classes.items()
        }

    def _detector_notification_callback(self, value, channel):
        try:
            plan_id = self._action_plan[channel]
            plan_detail = self._action_plan_detail[plan_id]
            print('take action', channel)
            for action in plan_detail['actions']:
                self._controllers[action['type']].execute(action['parameters'])
            print('complete action', channel)
        except KeyError:
            print('invalid action')

    def add_detector_notification(self, notification):
        self._detector_notifications.append(notification)
        notification.subscribe(self._detector_notification_callback)

    def waits_subscriptin_end(self):
        for notification in self._detector_notifications:
            notification.wait_subscription_end()


if __name__ == '__main__':
    action_plan = {
        'detected_sleep': 0,
        'detected_clap': 1
    }
    action_plan_detail = {
        "actionSets": [
            {
                'id': 0,
                'name': '寝落ち検出',
                'actions': [
                    {'type': 'ir', 'parameters': {'id': 0}},

                ]
            },
            {
                'id': 1,
                'name': '拍手検出',
                'actions': [
                    {'type': 'ir', 'parameters': {'id': 1}},
                ]
            }
        ]
    }

    server = redis.StrictRedis('redis')
    detected_sleep = brain_notification.DetectedSleep(server)
    detected_clap = clap_detector_notification.DetectedClap(server)

    kinesis = Kinesis(server)
    kinesis.add_detector_notification(detected_sleep)
    kinesis.add_detector_notification(detected_clap)

    kinesis._action_plan.value = action_plan
    kinesis._action_plan_detail.value = action_plan_detail

    kinesis.waits_subscriptin_end()

