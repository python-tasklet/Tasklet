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

import tasklet

@tasklet.coroutine
def async_func():
    count = 0

    while True:
        count_by = (yield)

        count += count_by
        print count

f = async_func()

for x in xrange(5 ** 10):
    f.send(x,)


def to_run():
    print ("ran... idek...")

@tasklet.coroutine
def runtime():
    while True:
        yield; to_run()

f = runtime()

for _ in xrange(100000000):
    f.next()