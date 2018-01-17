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

import imp
import os

from neutron_lib.api import definitions
from neutron_lib.api.definitions import base
from neutron_lib.api import validators
from neutron_lib import constants
from neutron_lib.tests import _base as test_base


def assert_bool(tester, attribute, attribute_dict, keyword, value):
    tester.assertIsInstance(
        value, bool,
        '%s must be a boolean for %s.' % (keyword, attribute))


def assert_converter(tester, attribute, attribute_dict, keyword, value):
    if ('default' not in attribute_dict or
            attribute_dict['default'] is constants.ATTR_NOT_SPECIFIED):
        return
    try:
        attribute_dict['convert_to'](attribute_dict['default'])
    except KeyError:
        try:
            attribute_dict['convert_list_to'](attribute_dict['default'])
        except KeyError:
            if validators.is_attr_set(value) and not isinstance(
                    value, (str, list)):
                tester.fail("Default value '%s' cannot be converted for "
                            "attribute %s." % (value, attribute))


def assert_true(tester, attribute, attribute_dict, keyword, value):
    tester.assertTrue(
        value, '%s must be True for %s.' % (keyword, attribute))


def assert_validator(tester, attribute, attribute_dict, keyword, value):
    tester.assertIn(list(value)[0], validators.validators,
                    '%s is not a known validator for %s.' % (value, attribute))

ASSERT_FUNCTIONS = {
    'allow_post': assert_bool,
    'allow_put': assert_bool,
    'convert_to': assert_converter,
    'convert_list_to': assert_converter,
    'default': assert_converter,
    'enforce_policy': assert_bool,
    'is_visible': assert_bool,
    'primary_key': assert_true,
    'required_by_policy': assert_bool,
    'validate': assert_validator,
}


class DefinitionBaseTestCase(test_base.BaseTestCase):

    extension_module = None
    extension_resources = ()
    extension_subresources = ()
    extension_attributes = ()

    def setUp(self):
        super(DefinitionBaseTestCase, self).setUp()
        if not self.extension_module:
            self.fail("Missing extension module definition.")
        self.alias = self.extension_module.ALIAS
        self.is_shim_extension = self.extension_module.IS_SHIM_EXTENSION
        self.is_standard_attr_extension = (
            self.extension_module.IS_STANDARD_ATTR_EXTENSION)
        self.name = self.extension_module.NAME
        self.description = self.extension_module.DESCRIPTION
        self.resource_map = self.extension_module.RESOURCE_ATTRIBUTE_MAP
        self.subresource_map = self.extension_module.SUB_RESOURCE_ATTRIBUTE_MAP
        self.action_map = self.extension_module.ACTION_MAP
        self.action_status = self.extension_module.ACTION_STATUS
        self.required_extensions = self.extension_module.REQUIRED_EXTENSIONS
        self.optional_extensions = self.extension_module.OPTIONAL_EXTENSIONS

    def test_shim_extension(self):
        if self.is_shim_extension is True:
            self.assertFalse(self.extension_resources)
            self.assertFalse(self.extension_attributes)
            self.assertFalse(self.resource_map)
            self.assertFalse(self.action_map)
            self.assertFalse(self.action_status)

    def test_is_standard_attr_extension(self):
        if self.is_standard_attr_extension:
            self.assertIn('standard-attr-', self.alias)
        else:
            self.skipTest('API definition is not related to standardattr.')

    def test_resource_map(self):
        if (not self.resource_map and not self.subresource_map
                and not self.is_shim_extension):
            self.fail('Missing resource and subresource map, '
                      'what is this extension doing?')
        elif self.is_shim_extension:
            self.skipTest('Shim extension with no API changes.')

        for resource in self.resource_map:
            self.assertIn(
                resource, base.KNOWN_RESOURCES + self.extension_resources,
                'Resource is unknown, check for typos.')
            self.assertParams(self.resource_map[resource])

    def assertParams(self, resource):
        for attribute in resource.keys():
            self.assertIn(
                attribute,
                base.KNOWN_ATTRIBUTES + self.extension_attributes,
                'Attribute is unknown, check for typos.')
            for keyword in resource[attribute]:
                self.assertIn(keyword, base.KNOWN_KEYWORDS,
                              'Keyword is unknown, check for typos.')
                value = resource[attribute][keyword]
                assert_f = ASSERT_FUNCTIONS[keyword]
                assert_f(self, attribute,
                         resource[attribute],
                         keyword, value)

    def test_subresource_map(self):
        if not self.subresource_map:
            self.skipTest('API extension has no subresource map.')
        for subresource in self.subresource_map:
            self.assertIn(
                subresource, self.extension_subresources,
                'Sub-resource is unknown, check for typos.')
            for attribute in self.subresource_map[subresource]:
                self.assertIn(attribute, ('parent', 'parameters'))
            self.assertIn(
                self.subresource_map[subresource]['parent']['collection_name'],
                base.KNOWN_RESOURCES + self.extension_resources,
                'Sub-resource parent is unknown, check for typos.')
            self.assertIn('member_name',
                          self.subresource_map[subresource]['parent'],
                          'Incorrect parent definition, check for typos.')
            self.assertParams(self.subresource_map[subresource]['parameters'])

    def test_action_map(self):
        self.assertIsInstance(self.action_map, dict)
        if not self.action_map:
            self.skipTest('API definition has no action map.')

        for key in self.action_map:
            for action in self.action_map[key].values():
                self.assertIn(action, base.KNOWN_HTTP_ACTIONS,
                              'HTTP verb is unknown, check for typos.')

    def test_action_status(self):
        if not self.action_status:
            self.skipTest('API definition has no action status.')

        for status in self.action_status.values():
            self.assertIn(status, base.KNOWN_ACTION_STATUSES,
                          'HTTP status is unknown, check for typos.')

    def test_required_extensions(self):
        self.assertIsInstance(self.required_extensions, list)
        if not self.required_extensions:
            self.skipTest('API definition has no required extensions.')

        for ext in self.required_extensions:
            self.assertIn(ext, base.KNOWN_EXTENSIONS,
                          'Required extension is unknown, check for typos.')

    def test_optional_extensions(self):
        self.assertIsInstance(self.optional_extensions, list)
        if not self.optional_extensions:
            self.skipTest('API definition has no optional extensions.')

        for ext in self.optional_extensions:
            self.assertIn(ext, base.KNOWN_EXTENSIONS,
                          'Optional extension is unknown, check for typos.')

    def test_all_api_definitions_list(self):
        # ensure _ALL_API_DEFINITIONS contains all public api-defs
        ext_aliases = []
        api_def_path = 'neutron_lib/api/definitions'
        for f in sorted(os.listdir(api_def_path)):
            mod_name, file_ext = os.path.splitext(os.path.split(f)[-1])
            ext_path = os.path.join(api_def_path, f)
            if file_ext.lower() == '.py' and not mod_name.startswith('_'):
                mod = imp.load_source(mod_name, ext_path)
                ext_alias = getattr(mod, 'ALIAS', None)
                if not ext_alias:
                    continue
                ext_aliases.append(ext_alias)

        self.assertEqual(sorted(ext_aliases),
                         sorted([d.ALIAS for d in
                                 definitions._ALL_API_DEFINITIONS]))
