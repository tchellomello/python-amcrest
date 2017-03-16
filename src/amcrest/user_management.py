# -*- coding: utf-8 -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# vim:sw=4:ts=4:et


class UserManagement(object):

    def info_user(self, username):
        ret = self.command(
            'userManager.cgi?action=getUserInfo&name={0}'.format(username)
        )
        return ret.content.decode('utf-8')

    @property
    def info_all_users(self):
        ret = self.command(
            'userManager.cgi?action=getUserInfoAll'
        )
        return ret.content.decode('utf-8')

    @property
    def info_all_active_users(self):
        ret = self.command(
            'userManager.cgi?action=getActiveUserInfoAll'
        )
        return ret.content.decode('utf-8')

    def info_group(self, group):
        ret = self.command(
            'userManager.cgi?action=getGroupInfo&name={0}'.format(group)
        )
        return ret.content.decode('utf-8')

    @property
    def info_all_groups(self):
        ret = self.command(
            'userManager.cgi?action=getGroupInfoAll'
        )
        return ret.content.decode('utf-8')

    def delete_user(self, username):
        ret = self.command(
            'userManager.cgi?action=deleteUser&name={0}'.format(username)
        )
        return ret.content.decode('utf-8')

    def add_user(self, username, password, group, sharable=True,
                 reserved=False, memo=None):
        """
        Params:
            username - username for user
            password - password for user
            group - string the range is "admin" and "user". In different group,
                    the user has different authorities.

            sharable - bool, true means allow multi-point login

            reserved - bool, true means this user can't be deleted

            memo - memo to user
        """

        cmd = "userManager.cgi?action=addUser&user.Name={0}" \
              "&user.Password={1}&user.Group={2}&user.Sharable={3}" \
              "&user.Reserved={4}".format(
                  username, password, group.lower(), sharable.lower(),
                  reserved.lower())

        if memo:
            cmd += "&user.Memo=%s" % memo

        ret = self.command(cmd)
        return ret.content.decode('utf-8')

    def modify_password(self, username, newpwd, oldpwd):
        """
        Params:
            username - user name
            newpwd - new password
            oldpwd - old password
        """
        ret = self.command(
            'userManager.cgi?action=modifyPassword&name={0}&pwd={1}'
            '&pwdOld={2}'.format(username, newpwd, oldpwd)
        )
        return ret.content.decode('utf-8')

    def modify_user(self, username, attribute, value):
        """
        Params:
            username - username for user
            attribute - the attribute name that will change:
                        group, sharable, reserved, memo

            value - the new value for attribute
        """

        cmd = "userManager.cgi?action=modifyUser&name={0}".format(
            username)

        if attribute.lower() == "group":
            cmd += "&user.Group=%s" % value.lower()

        elif attribute.lower() == "sharable":
            cmd += "&user.Sharable=%s" % value.lower()

        elif attribute.lower() == "reserved":
            cmd += "&user.Reserved=%s" % value.lower()

        elif attribute == "memo":
            cmd += "&user.Memo=%s" % value.lower()

        ret = self.command(cmd)
        return ret.content.decode('utf-8')
