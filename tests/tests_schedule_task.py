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

from tasklet.task import Task, TaskScheduler

scheduler = TaskScheduler.TaskScheduler()

def run_0():
    # performs an endless loop.
    print 'run_0'

def run_1():
    # performs an endless loop.
    print 'run_1'

scheduler.add_task(Task.Task(run_0.__name__, run_0))
scheduler.add_task(Task.Task(run_1.__name__, run_1))

# run the scheduler main loop.
scheduler.run_scheduler()