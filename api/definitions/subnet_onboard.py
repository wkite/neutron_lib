# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
#
# All Rights Reserved.
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
from neutron_lib.api.definitions import subnet as subnet_def
from neutron_lib.api.definitions import subnetpool as subnetpool_def
import neutron_lib.constants

ALIAS = "subnet_onboard"
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Subnet Onboard"
DESCRIPTION = "Provides support for onboarding subnets into subnet pools"
UPDATED_TIMESTAMP = "2017-07-27T10:00:00-00:00"


ONBOARD_SUBNETS = 'onboard_network_subnets'

ONBOARD_SUBNETS_SPECS = {
    'id': {'type:uuid': None, 'required': True},
    'network_id': {'type:uuid': None, 'required': True},
    'ip_version': {'convert_to': converters.convert_to_int,
                   'type:values': [4, 6],
                   'required': True}
}


RESOURCE_ATTRIBUTE_MAP = {
    subnetpool_def.COLLECTION_NAME: {
        subnet_def.COLLECTION_NAME: {
            'allow_post': True, 'allow_put': True,
            'validate': {
                'type:list_of_any_key_specs_or_none': ONBOARD_SUBNETS_SPECS
            }
        }
    }
}

# The subresource attribute map for the extension.  This extension has only
# top level resources, not child resources, so this is set to an empty dict.
SUB_RESOURCE_ATTRIBUTE_MAP = {
}

# The action map.
ACTION_MAP = {
    subnetpool_def.RESOURCE_NAME: {
        ONBOARD_SUBNETS: 'PUT'
    }
}

# The action status.
ACTION_STATUS = {
}

# The list of required extensions.
REQUIRED_EXTENSIONS = [neutron_lib.constants.SUBNET_ALLOCATION_EXT_ALIAS]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = [
]
