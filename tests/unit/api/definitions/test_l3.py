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

from neutron_lib.api.definitions import l3
from neutron_lib.tests.unit.api.definitions import base


class L3DefinitionTestCase(base.DefinitionBaseTestCase):
    extension_module = l3
    extension_resources = (l3.ROUTERS, l3.FLOATINGIPS,)
    extension_attributes = (l3.FLOATING_IP_ADDRESS,
                            l3.FLOATING_NETWORK_ID,
                            l3.ROUTER_ID,
                            l3.PORT_ID,
                            l3.FIXED_IP_ADDRESS,
                            l3.SUBNET_ID,
                            l3.EXTERNAL_GW_INFO)
