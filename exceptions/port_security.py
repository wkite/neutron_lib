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

from neutron_lib._i18n import _
from neutron_lib import exceptions


class PortSecurityPortHasSecurityGroup(exceptions.InUse):
    message = _("Port has security group associated. Cannot disable port "
                "security or IP address until security group is removed.")


class PortSecurityAndIPRequiredForSecurityGroups(exceptions.InvalidInput):
    message = _("Port security must be enabled and port must have an IP "
                "address in order to use security groups.")
