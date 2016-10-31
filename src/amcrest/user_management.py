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


class UserManagement:

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
