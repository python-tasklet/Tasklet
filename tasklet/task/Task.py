"""
* Copyright @ Tasklet 2016, All rights reserved.
* 
* Licensed to the Apache Software Foundation (ASF) under one
* or more contributor license agreements.  See the NOTICE file
* distributed with this work for additional information
* regarding copyright ownership.  The ASF licenses this file
* to you under the Apache License, Version 2.0 (the
* "License"); you may not use this file except in compliance
* with the License.  You may obtain a copy of the License at
* 
*   http://www.apache.org/licenses/LICENSE-2.0
* 
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied.  See the License for the
* specific language governing permissions and limitations
* under the License.
"""

from tasklet.error.TaskError import TaskError
from tasklet import coroutine

class Task(object):
    __slots__ = [
        '_name', '_target', '_args', '_kwargs', '_is_active']

    def __init__(self, name=None, target=None, args=(), kwargs={}):
        self._name = name
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._is_active = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        self._kwargs = kwargs

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        self._is_active = is_active

    @coroutine
    def process(self):
        while self.is_active:
            yield; self.target(*self.args, **self.kwargs)

    def shutdown(self):
        if not self.is_active:
            raise TaskError('Cannot shutdown task "%s" because it is not running!' % (
                self.name,))

        self.is_active = False