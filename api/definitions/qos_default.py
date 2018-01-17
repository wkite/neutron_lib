# Copyright (c) 2017 Intel Corporation.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron_lib.api import converters
from neutron_lib.api.definitions import qos as qos_apidef

ALIAS = 'qos-default'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'QoS default policy'
API_PREFIX = ''
DESCRIPTION = 'Expose the QoS default policy per project'
UPDATED_TIMESTAMP = '2017-041-06T10:00:00-00:00'
RESOURCE_ATTRIBUTE_MAP = {
    qos_apidef.POLICIES: {
        'is_default': {
            'allow_post': True,
            'allow_put': True,
            'default': False,
            'convert_to': converters.convert_to_boolean,
            'is_visible': True
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [qos_apidef.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
