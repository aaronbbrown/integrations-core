# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

from datadog_checks.utils.common import get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(HERE, "resources")
LOCAL_TMP_DIR = os.getenv('LOCAL_TMP_DIR', '/tmp')

HOST = get_docker_hostname()
PORT = "1521"

CHECK_NAME = "oracle"

TABLESPACE_METRICS = [
    'oracle.tablespace.used',
    'oracle.tablespace.size',
    'oracle.tablespace.in_use',
    'oracle.tablespace.offline',
]

CONFIG = {
    'server': '{}:{}'.format(HOST, PORT),
    'user': 'system',
    'password': 'oracle',
    'service_name': 'xe',
    'tags': ['optional:tag1']
}
