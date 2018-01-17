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

# neutron-fwaas constants
from neutron_lib import constants

FIREWALL_GROUPS = 'firewall_groups'
FIREWALL_POLICIES = 'firewall_policies'
FIREWALL_RULES = 'firewall_rules'
FIREWALLS = 'firewalls'

FWAAS_ALLOW = "allow"
FWAAS_DENY = "deny"
FWAAS_REJECT = "reject"
FW_VALID_ACTION_VALUES = [FWAAS_ALLOW, FWAAS_DENY, FWAAS_REJECT]

# Firewall Protocol List

FW_PROTOCOL_VALUES = list(constants.IPTABLES_PROTOCOL_MAP.keys()) + [None]

# a default resource, such as auto allocated topology is_default network
IS_DEFAULT = 'is_default'
