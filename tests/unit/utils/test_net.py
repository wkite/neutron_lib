# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import socket

import mock

from neutron_lib import constants
from neutron_lib.tests import _base as base
from neutron_lib.utils import net


class TestGetHostname(base.BaseTestCase):

    @mock.patch.object(socket, 'gethostname',
                       return_value='fake-host-name')
    def test_get_hostname(self, mock_gethostname):
        self.assertEqual('fake-host-name',
                         net.get_hostname())
        mock_gethostname.assert_called_once_with()


class TestGetRandomMac(base.BaseTestCase):

    @mock.patch.object(random, 'getrandbits', return_value=0xa2)
    def test_first_4_octets_unchanged(self, mock_rnd):
        mac = net.get_random_mac(['aa', 'bb', '00', 'dd', 'ee', 'ff'])
        self.assertEqual('aa:bb:00:dd:a2:a2', mac)
        mock_rnd.assert_called_with(8)

    @mock.patch.object(random, 'getrandbits', return_value=0xa2)
    def test_first_4th_octet_generated(self, mock_rnd):
        mac = net.get_random_mac(['aa', 'bb', 'cc', '00', 'ee', 'ff'])
        self.assertEqual('aa:bb:cc:a2:a2:a2', mac)
        mock_rnd.assert_called_with(8)


class TestPortDeviceOwner(base.BaseTestCase):

    def test_is_port_trusted(self):
        self.assertTrue(net.is_port_trusted(
            {'device_owner':
             constants.DEVICE_OWNER_NETWORK_PREFIX + 'dev'}))

    def test_is_port_not_trusted(self):
        self.assertFalse(net.is_port_trusted(
            {'device_owner': constants.DEVICE_OWNER_COMPUTE_PREFIX + 'dev'}))
