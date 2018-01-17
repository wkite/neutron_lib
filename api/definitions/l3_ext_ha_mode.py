# Copyright (C) 2014 eNovance SAS <licensing@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_lib.api import converters
from neutron_lib.api.definitions import l3
from neutron_lib import constants


HA_INFO = 'ha'

ALIAS = constants.L3_HA_MODE_EXT_ALIAS
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'HA Router extension'
API_PREFIX = ''
DESCRIPTION = 'Adds HA capability to routers.'
UPDATED_TIMESTAMP = '2014-04-26T00:00:00-00:00'
RESOURCE_NAME = l3.ROUTER
COLLECTION_NAME = l3.ROUTERS
RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        HA_INFO: {
            'allow_post': True, 'allow_put': True,
            'default': constants.ATTR_NOT_SPECIFIED, 'is_visible': True,
            'enforce_policy': True,
            'convert_to': converters.convert_to_boolean_if_not_none
        }
    }
}
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = [l3.ALIAS]
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
