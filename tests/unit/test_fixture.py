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

import mock

from oslo_config import cfg
from oslo_db import options
from oslotest import base

from neutron_lib.api import attributes
from neutron_lib.api.definitions import port
from neutron_lib.callbacks import registry
from neutron_lib.clients import placement
from neutron_lib.db import model_base
from neutron_lib import fixture
from neutron_lib.plugins import directory
from neutron_lib.tests.unit.api import test_attributes


class PluginDirectoryFixtureTestCase(base.BaseTestCase):

    def setUp(self):
        super(PluginDirectoryFixtureTestCase, self).setUp()
        self.directory = mock.Mock()
        self.useFixture(fixture.PluginDirectoryFixture(
            plugin_directory=self.directory))

    def test_fixture(self):
        directory.add_plugin('foo', 'foo')
        self.assertTrue(self.directory.add_plugin.called)


class CallbackRegistryFixtureTestCase(base.BaseTestCase):

    def setUp(self):
        super(CallbackRegistryFixtureTestCase, self).setUp()
        self.manager = mock.Mock()
        self.useFixture(fixture.CallbackRegistryFixture(
            callback_manager=self.manager))

    def test_fixture(self):
        registry.notify('a', 'b', self)
        self.assertTrue(self.manager.notify.called)


class SqlFixtureTestCase(base.BaseTestCase):

    def setUp(self):
        super(SqlFixtureTestCase, self).setUp()
        options.set_defaults(
            cfg.CONF,
            connection='sqlite://')
        self.useFixture(fixture.SqlFixture())

    def test_fixture(self):
        self.assertIsNotNone(model_base.BASEV2.metadata.sorted_tables)


class APIDefinitionFixtureTestCase(base.BaseTestCase):

    def _test_all_api_definitions_fixture(self, global_cleanup=True):
        apis = fixture.APIDefinitionFixture.all_api_definitions_fixture()
        apis.backup_global_resources = global_cleanup
        apis.setUp()

        asserteq = self.assertNotEqual if global_cleanup else self.assertEqual
        asserteq({}, apis._orig_resources)

        for r in test_attributes.TestCoreResources.CORE_DEFS:
            attributes.RESOURCES[r.COLLECTION_NAME]['_test_'] = {}
            r.RESOURCE_ATTRIBUTE_MAP['_test_'] = {}

        apis.cleanUp()
        for r in test_attributes.TestCoreResources.CORE_DEFS:
            self.assertNotIn('_test_', r.RESOURCE_ATTRIBUTE_MAP)
            global_assert = (self.assertNotIn
                             if global_cleanup else self.assertIn)
            global_assert('_test_', attributes.RESOURCES[r.COLLECTION_NAME])
            # cleanup
            if not global_cleanup:
                del attributes.RESOURCES[r.COLLECTION_NAME]['_test_']

    def test_all_api_definitions_fixture_no_global_backup(self):
        self._test_all_api_definitions_fixture(global_cleanup=False)

    def test_all_api_definitions_fixture_with_global_backup(self):
        self._test_all_api_definitions_fixture(global_cleanup=True)

    def test_global_resources_reference_updated(self):
        resources_ref = attributes.RESOURCES
        apis = fixture.APIDefinitionFixture()

        apis.setUp()
        attributes.RESOURCES['test_resource'] = {}
        self.assertIn('test_resource', resources_ref)
        attributes.RESOURCES[port.COLLECTION_NAME]['test_port_attr'] = {}
        self.assertIn('test_port_attr',
                      attributes.RESOURCES[port.COLLECTION_NAME])
        apis.cleanUp()

        self.assertNotIn('test_port_attr',
                         attributes.RESOURCES[port.COLLECTION_NAME])
        self.assertNotIn('test_resource', resources_ref)

    def test_api_def_reference_updated(self):
        api_def_ref = port.RESOURCE_ATTRIBUTE_MAP
        apis = fixture.APIDefinitionFixture()

        apis.setUp()
        port.RESOURCE_ATTRIBUTE_MAP[port.COLLECTION_NAME]['test_attr'] = {}
        self.assertIn('test_attr', api_def_ref[port.COLLECTION_NAME])
        apis.cleanUp()

        self.assertNotIn('test_attr',
                         port.RESOURCE_ATTRIBUTE_MAP[port.COLLECTION_NAME])
        self.assertNotIn('test_attr', api_def_ref[port.COLLECTION_NAME])


class PlacementAPIClientFixtureTestCase(base.BaseTestCase):

    def _create_client_and_fixture(self):
        placement_client = placement.PlacementAPIClient(mock.Mock())
        placement_fixture = self.useFixture(
            fixture.PlacementAPIClientFixture(placement_client))
        return placement_client, placement_fixture

    def test_post(self):
        p_client, p_fixture = self._create_client_and_fixture()
        p_client.create_resource_provider('resource')
        p_fixture.mock_post.assert_called_once()

    def test_put(self):
        p_client, p_fixture = self._create_client_and_fixture()
        p_client.update_inventory('resource', mock.ANY, 'class_name')
        p_fixture.mock_put.assert_called_once()

    def test_delete(self):
        p_client, p_fixture = self._create_client_and_fixture()
        p_client.delete_resource_provider('resource')
        p_fixture.mock_delete.assert_called_once()

    def test_get(self):
        p_client, p_fixture = self._create_client_and_fixture()
        p_client.list_aggregates('resource')
        p_fixture.mock_get.assert_called_once()
