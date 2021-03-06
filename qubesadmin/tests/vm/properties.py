# -*- encoding: utf8 -*-
#
# The Qubes OS Project, http://www.qubes-os.org
#
# Copyright (C) 2017 Marek Marczykowski-Górecki
#                               <marmarek@invisiblethingslab.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>.

import qubesadmin.tests.vm


class TC_00_Properties(qubesadmin.tests.vm.VMTestCase):

    def test_000_list(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.List', None, None)] = \
            b'0\x00prop1\nprop2\n'
        self.assertEqual(
            self.vm.property_list(),
            ['prop1', 'prop2'])
        self.assertAllCalled()

    def test_001_get_str(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=False type=str value'
        self.assertEqual(self.vm.prop1, 'value')
        self.assertAllCalled()

    def test_002_get_int(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=False type=int 123'
        self.assertEqual(self.vm.prop1, 123)
        self.assertAllCalled()

    def test_003_get_bool(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=False type=bool True'
        self.assertEqual(self.vm.prop1, True)
        self.assertAllCalled()

    def test_004_get_vm(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=False type=vm test-vm'
        self.assertIsInstance(self.vm.prop1, qubesadmin.vm.QubesVM)
        self.assertEqual(self.vm.prop1.name, 'test-vm')
        self.assertAllCalled()

    def test_005_get_none_vm(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=False type=vm '
        self.assertEqual(self.vm.prop1, None)
        self.assertAllCalled()

    def test_006_get_none_bool(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=False type=bool '
        with self.assertRaises(AttributeError):
            self.vm.prop1
        self.assertAllCalled()

    def test_007_get_none_int(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=False type=int '
        with self.assertRaises(AttributeError):
            self.vm.prop1
        self.assertAllCalled()

    def test_008_get_none_str(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=False type=str '
        self.assertEqual(self.vm.prop1, '')
        self.assertAllCalled()

    def test_010_get_default(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=False type=str value'
        self.assertEqual(self.vm.property_is_default('prop1'), False)
        self.assertAllCalled()

    def test_011_get_default(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'prop1', None)] = \
            b'0\x00default=True type=str value'
        self.assertEqual(self.vm.property_is_default('prop1'), True)
        self.assertAllCalled()

    def test_012_get_invalid(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Get', 'invalid', None)] = \
            b'2\x00QubesNoSuchPropertyError\x00\x00Invalid property ' \
            b'\'invalid\' on test-vm\x00'
        with self.assertRaises(qubesadmin.exc.QubesNoSuchPropertyError):
            self.vm.invalid
        self.assertFalse(hasattr(self.vm, 'invalid'))
        self.assertAllCalled()

    def test_020_set_str(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Set', 'prop1', b'value')] = \
            b'0\x00'
        self.vm.prop1 = 'value'
        self.assertAllCalled()

    def test_021_set_int(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Set', 'prop1', b'123')] = \
            b'0\x00'
        self.vm.prop1 = 123
        self.assertAllCalled()

    def test_022_set_bool(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Set', 'prop1', b'True')] = \
            b'0\x00'
        self.vm.prop1 = True
        self.assertAllCalled()

    def test_023_set_vm(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Set', 'prop1', b'test-vm')] = \
            b'0\x00'
        self.vm.prop1 = self.vm
        self.assertAllCalled()

    def test_024_set_none(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Set', 'prop1', b'')] = \
            b'0\x00'
        self.vm.prop1 = None
        self.assertAllCalled()

    def test_030_reset(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Reset', 'prop1', None)] = \
            b'0\x00'
        self.vm.prop1 = qubesadmin.DEFAULT
        self.assertAllCalled()

    def test_031_reset(self):
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Reset', 'prop1', None)] = \
            b'0\x00'
        del self.vm.prop1
        self.assertAllCalled()


class TC_01_SpecialCases(qubesadmin.tests.vm.VMTestCase):
    def test_000_get_name(self):
        # should not make any mgmt call
        self.assertEqual(self.vm.name, 'test-vm')
        self.assertAllCalled()

    def test_001_set_name(self):
        # but this one should still do a call
        self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Set', 'name', b'test-vm2')] = \
            b'0\x00'
        self.vm.name = 'test-vm2'
        # here should be no separate mgmt.vm.property.Get+name call
        self.assertEqual(self.vm.name, 'test-vm2')
        self.assertAllCalled()

        # check if VM list cache was cleared
        self.app.actual_calls = []
        del self.app.expected_calls[
            ('test-vm', 'admin.vm.property.Set', 'name', b'test-vm2')]
        vm = self.app.domains['test-vm']
        self.assertAllCalled()

    def test_010_power_state_running(self):
        self.app.expected_calls[('test-vm', 'admin.vm.List', None, None)] = \
            b'0\x00test-vm class=AppVM state=Running\n'
        self.assertEqual(self.vm.get_power_state(), 'Running')
        self.assertTrue(self.vm.is_running())
        self.assertFalse(self.vm.is_halted())
        self.assertFalse(self.vm.is_paused())

    def test_011_power_state_paused(self):
        self.app.expected_calls[('test-vm', 'admin.vm.List', None, None)] = \
            b'0\x00test-vm class=AppVM state=Paused\n'
        self.assertEqual(self.vm.get_power_state(), 'Paused')
        self.assertTrue(self.vm.is_running())
        self.assertFalse(self.vm.is_halted())
        self.assertTrue(self.vm.is_paused())

    def test_012_power_state_halted(self):
        self.app.expected_calls[('test-vm', 'admin.vm.List', None, None)] = \
            b'0\x00test-vm class=AppVM state=Halted\n'
        self.assertEqual(self.vm.get_power_state(), 'Halted')
        self.assertFalse(self.vm.is_running())
        self.assertTrue(self.vm.is_halted())
        self.assertFalse(self.vm.is_paused())

    def test_012_power_state_transient(self):
        self.app.expected_calls[('test-vm', 'admin.vm.List', None, None)] = \
            b'0\x00test-vm class=AppVM state=Transient\n'
        self.assertEqual(self.vm.get_power_state(), 'Transient')
        self.assertTrue(self.vm.is_running())
        self.assertFalse(self.vm.is_halted())
        self.assertFalse(self.vm.is_paused())
