#!/usr/bin/env python3.6

import datetime, threading, time

class Counter:

    def __init__(self):
        self.ratelimit = 60
        self.next_call = time.time()
        self.reset()

    def reset(self):
        self.ratelimit = 60
        self.next_call = self.next_call+60
        threading.Timer( self.next_call - time.time(), self.reset ).start()

    def decrease(self):
        self.ratelimit -= 1

    def limitused(self,num):
        self.ratelimit = 60 - num
