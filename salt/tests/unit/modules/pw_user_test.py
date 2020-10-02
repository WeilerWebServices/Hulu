# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Rupesh Tare <rupesht@saltstack.com>`
'''

# Import Salt Testing Libs
from salttesting import TestCase, skipIf
from salttesting.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON
)

# Import Salt Libs
from salt.modules import pw_user
from salt.exceptions import CommandExecutionError
import pwd


# Globals
pw_user.__grains__ = {}
pw_user.__salt__ = {}
pw_user.__context__ = {}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class PwUserTestCase(TestCase):
    '''
    Test cases for salt.modules.pw_user
    '''
    def test_add(self):
        '''
        Test for adding a user
        '''
        with patch.dict(pw_user.__grains__, {'os_family': 'RedHat'}):
            mock = MagicMock(return_value={'retcode': 0, 'stdout': 'salt'})
            with patch.dict(pw_user.__salt__, {'cmd.run_all': mock}):
                self.assertTrue(pw_user.add('a'))

    def test_delete(self):
        '''
        Test for deleting a user
        '''
        mock = MagicMock(return_value={'retcode': 0})
        with patch.dict(pw_user.__salt__, {'cmd.run_all': mock}):
            self.assertTrue(pw_user.delete('A'), 1)

    @patch('salt.modules.pw_user.__context__', MagicMock(return_value='A'))
    def test_getent(self):
        '''
        Test if user.getent already have a value
        '''
        self.assertTrue(pw_user.getent())

        mock = MagicMock(return_value='A')
        with patch.object(pw_user, 'info', mock):
            self.assertEqual(pw_user.getent(True)[0], 'A')

    def test_chuid(self):
        '''
        Test if user id given is same as previous id
        '''
        mock = MagicMock(return_value={'uid': 'A'})
        with patch.object(pw_user, 'info', mock):
            self.assertTrue(pw_user.chuid('name', 'A'))

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'uid': 'A'}, {'uid': 'A'}])
            with patch.object(pw_user, 'info', mock):
                self.assertFalse(pw_user.chuid('name', 'B'))

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'uid': 'A'}, {'uid': 'B'}])
            with patch.object(pw_user, 'info', mock):
                self.assertTrue(pw_user.chuid('name', 'A'))

    def test_chgid(self):
        '''
        Test if group id given is same as previous id
        '''
        mock = MagicMock(return_value={'gid': 1})
        with patch.object(pw_user, 'info', mock):
            self.assertTrue(pw_user.chgid('name', 1))

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'gid': 2}, {'gid': 2}])
            with patch.object(pw_user, 'info', mock):
                self.assertFalse(pw_user.chgid('name', 1))

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'gid': 1}, {'gid': 2}])
            with patch.object(pw_user, 'info', mock):
                self.assertTrue(pw_user.chgid('name', 1))

    def test_chshell(self):
        '''
        Test if shell given is same as previous shell
        '''
        mock = MagicMock(return_value={'shell': 'A'})
        with patch.object(pw_user, 'info', mock):
            self.assertTrue(pw_user.chshell('name', 'A'))

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'shell': 'B'}, {'shell': 'B'}])
            with patch.object(pw_user, 'info', mock):
                self.assertFalse(pw_user.chshell('name', 'A'))

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'shell': 'A'}, {'shell': 'B'}])
            with patch.object(pw_user, 'info', mock):
                self.assertTrue(pw_user.chshell('name', 'A'))

    def test_chhome(self):
        '''
        Test if home directory given is same as previous home directory
        '''
        mock = MagicMock(return_value={'home': 'A'})
        with patch.object(pw_user, 'info', mock):
            self.assertTrue(pw_user.chhome('name', 'A'))

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'home': 'B'}, {'home': 'B'}])
            with patch.object(pw_user, 'info', mock):
                self.assertFalse(pw_user.chhome('name', 'A'))

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'home': 'A'}, {'home': 'B'}])
            with patch.object(pw_user, 'info', mock):
                self.assertTrue(pw_user.chhome('name', 'A'))

    def test_chgroups(self):
        '''
        Test if no group needs to be added
        '''
        mock = MagicMock(return_value=False)
        with patch.dict(pw_user.__salt__, {'cmd.retcode': mock}):
            mock = MagicMock(return_value=['a', 'b', 'c', 'd'])
            with patch.object(pw_user, 'list_groups', mock):
                self.assertTrue(pw_user.chgroups('name', 'a, b, c, d'))

        mock = MagicMock(return_value=False)
        with patch.dict(pw_user.__salt__, {'cmd.retcode': mock}):
            mock = MagicMock(return_value=['a', 'b'])
            with patch.object(pw_user, 'list_groups', mock):
                self.assertTrue(pw_user.chgroups('name', 'a, b, c'))

    def test_chfullname(self):
        '''
        Change the user's Full Name
        '''
        mock = MagicMock(return_value=False)
        with patch.object(pw_user, '_get_gecos', mock):
            self.assertFalse(pw_user.chfullname('name', 'fullname'))

        mock = MagicMock(return_value={'fullname': 'fullname'})
        with patch.object(pw_user, '_get_gecos', mock):
            self.assertTrue(pw_user.chfullname('name', 'fullname'))

        mock = MagicMock(return_value={'fullname': 'fullname'})
        with patch.object(pw_user, '_get_gecos', mock):
            mock = MagicMock(return_value=None)
            with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
                mock = MagicMock(return_value={'fullname': 'fullname2'})
                with patch.object(pw_user, 'info', mock):
                    self.assertFalse(pw_user.chfullname('name', 'fullname1'))

        mock = MagicMock(return_value={'fullname': 'fullname2'})
        with patch.object(pw_user, '_get_gecos', mock):
            mock = MagicMock(return_value=None)
            with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
                mock = MagicMock(return_value={'fullname': 'fullname2'})
                with patch.object(pw_user, 'info', mock):
                    self.assertFalse(pw_user.chfullname('name', 'fullname1'))

    def test_chroomnumber(self):
        '''
        Change the user's Room Number
        '''
        mock = MagicMock(return_value=False)
        with patch.object(pw_user, '_get_gecos', mock):
            self.assertFalse(pw_user.chroomnumber('name', 1))

        mock = MagicMock(return_value={'roomnumber': '1'})
        with patch.object(pw_user, '_get_gecos', mock):
            self.assertTrue(pw_user.chroomnumber('name', 1))

        mock = MagicMock(return_value={'roomnumber': '2'})
        with patch.object(pw_user, '_get_gecos', mock):
            mock = MagicMock(return_value=None)
            with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
                mock = MagicMock(return_value={'roomnumber': '3'})
                with patch.object(pw_user, 'info', mock):
                    self.assertFalse(pw_user.chroomnumber('name', 1))

        mock = MagicMock(return_value={'roomnumber': '3'})
        with patch.object(pw_user, '_get_gecos', mock):
            mock = MagicMock(return_value=None)
            with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
                mock = MagicMock(return_value={'roomnumber': '3'})
                with patch.object(pw_user, 'info', mock):
                    self.assertFalse(pw_user.chroomnumber('name', 1))

    def test_chworkphone(self):
        '''
        Change the user's Work Phone
        '''
        mock = MagicMock(return_value=False)
        with patch.object(pw_user, '_get_gecos', mock):
            self.assertFalse(pw_user.chworkphone('name', 1))

        mock = MagicMock(return_value={'workphone': '1'})
        with patch.object(pw_user, '_get_gecos', mock):
            self.assertTrue(pw_user.chworkphone('name', 1))

        mock = MagicMock(return_value={'workphone': '2'})
        with patch.object(pw_user, '_get_gecos', mock):
            mock = MagicMock(return_value=None)
            with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
                mock = MagicMock(return_value={'workphone': '3'})
                with patch.object(pw_user, 'info', mock):
                    self.assertFalse(pw_user.chworkphone('name', 1))

        mock = MagicMock(return_value={'workphone': '3'})
        with patch.object(pw_user, '_get_gecos', mock):
            mock = MagicMock(return_value=None)
            with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
                mock = MagicMock(return_value={'workphone': '3'})
                with patch.object(pw_user, 'info', mock):
                    self.assertFalse(pw_user.chworkphone('name', 1))

    def test_chhomephone(self):
        '''
        Change the user's Home Phone
        '''
        mock = MagicMock(return_value=False)
        with patch.object(pw_user, '_get_gecos', mock):
            self.assertFalse(pw_user.chhomephone('name', 1))

        mock = MagicMock(return_value={'homephone': '1'})
        with patch.object(pw_user, '_get_gecos', mock):
            self.assertTrue(pw_user.chhomephone('name', 1))

        mock = MagicMock(return_value={'homephone': '2'})
        with patch.object(pw_user, '_get_gecos', mock):
            mock = MagicMock(return_value=None)
            with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
                mock = MagicMock(return_value={'homephone': '3'})
                with patch.object(pw_user, 'info', mock):
                    self.assertFalse(pw_user.chhomephone('name', 1))

        mock = MagicMock(return_value={'homephone': '3'})
        with patch.object(pw_user, '_get_gecos', mock):
            mock = MagicMock(return_value=None)
            with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
                mock = MagicMock(return_value={'homephone': '3'})
                with patch.object(pw_user, 'info', mock):
                    self.assertFalse(pw_user.chhomephone('name', 1))

    def test_info(self):
        '''
        Return user information
        '''
        self.assertEqual(pw_user.info('name'), {})

        mock = MagicMock(return_value=pwd.struct_passwd(('_TEST_GROUP',
                                                         '*',
                                                         83,
                                                         83,
                                                         'AMaViS Daemon',
                                                         '/var/virusmails',
                                                         '/usr/bin/false')))
        with patch.object(pwd, 'getpwnam', mock):
            mock = MagicMock(return_value='Group Name')
            with patch.object(pw_user, 'list_groups', mock):
                self.assertEqual(pw_user.info('name')['name'], '_TEST_GROUP')

    @patch('salt.utils.get_group_list', MagicMock(return_value='A'))
    def test_list_groups(self):
        '''
        Return a list of groups the named user belongs to
        '''
        self.assertEqual(pw_user.list_groups('name'), 'A')

    def test_list_users(self):
        '''
        Return a list of all users
        '''
        self.assertTrue(pw_user.list_users())

    def test_rename(self):
        '''
        Change the username for a named user
        '''
        mock = MagicMock(return_value=False)
        with patch.object(pw_user, 'info', mock):
            self.assertRaises(CommandExecutionError, pw_user.rename, 'name', 1)

        mock = MagicMock(return_value=True)
        with patch.object(pw_user, 'info', mock):
            self.assertRaises(CommandExecutionError, pw_user.rename, 'name', 1)

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'name': ''},
                                          False, {'name': 'name'}])
            with patch.object(pw_user, 'info', mock):
                self.assertTrue(pw_user.rename('name', 'name'))

        mock = MagicMock(return_value=None)
        with patch.dict(pw_user.__salt__, {'cmd.run': mock}):
            mock = MagicMock(side_effect=[{'name': ''}, False, {'name': ''}])
            with patch.object(pw_user, 'info', mock):
                self.assertFalse(pw_user.rename('name', 'name'))

if __name__ == '__main__':
    from integration import run_tests
    run_tests(PwUserTestCase, needs_daemon=False)
