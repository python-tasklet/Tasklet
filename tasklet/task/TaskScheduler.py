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
from tasklet.error.TaskGeneratorError import TaskGeneratorError

class TaskScheduler(object):
    __slots__ = ['_max_workers', '_running_queue', '_waiting_queue', '_scheduler_shutdown']

    def __init__(self, max_workers=None):
        self._max_workers = max_workers
        self._running_queue = {}
        self._waiting_queue = {}
        self._scheduler_shutdown = False

    @property
    def max_workers(self):
        return self._max_workers

    @max_workers.setter
    def max_workers(self, max_workers):
        self._max_workers = max_workers

    @property
    def running_queue(self):
        return self._running_queue

    @running_queue.setter
    def running_queue(self, running_queue):
        self._running_queue = running_queue

    @property
    def waiting_queue(self):
        return self._waiting_queue

    @waiting_queue.setter
    def waiting_queue(self, waiting_queue):
        self._waiting_queue = waiting_queue

    @property
    def scheduler_shutdown(self):
        return self._scheduler_shutdown

    @scheduler_shutdown.setter
    def scheduler_shutdown(self, scheduler_shutdown):
        self._scheduler_shutdown = scheduler_shutdown

    def add_task(self, task_obj):
        task_name = task_obj.name

        if task_name in self.waiting_queue.keys() or self.running_queue.keys():
            raise TaskError('Failed to add task "%s", because a task already exists with that name!' % (
                task_name,))

        self.waiting_queue[task_name] = task_obj

    def remove_task(self, task_obj):
        task_name = task_obj.name

        if task_name not in self.waiting_queue.keys() or self.running_queue.keys():
            raise TaskError('Failed to remove task "%s", because it doesn\'t exist in the queue!' % (
                task_name,))

        if task_name in self.waiting_queue.keys():
            del self.waiting_queue[task_name]
        else:
            del self.running_queue[task_name]

    def run_scheduler(self):
        if not len(self.running_queue.keys()):
            for task_name in self.waiting_queue.keys():
                if self.max_workers is not None:
                    if len(self.running_queue.keys()) >= self.max_workers:
                        break

                self.running_queue[task_name] = self.waiting_queue.pop(
                    task_name)

        while not self.scheduler_shutdown:
            if len(self.waiting_queue.keys()) > 0:
                for task_name in self.waiting_queue.keys():
                    if self.max_workers is not None:
                        if len(self.running_queue.keys()) >= self.max_workers:
                            break

                    self.running_queue[task_name] = self.waiting_queue.pop(
                        task_name)

            for task_name in self.running_queue.keys():
                try:
                    self.running_queue[task_name].process().next()
                except TaskGeneratorError:
                    self.running_queue[task_name].process().close(); self.running_queue[task_name].shutdown(); del self.running_queue[task_name]
                    continue
                except TaskError as e:
                    raise (e,)

                self.waiting_queue[task_name] = self.running_queue.pop(
                    task_name)

    def shutdown_scheduler(self):
        self.scheduler_shutdown = True