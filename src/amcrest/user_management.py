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
from typing import Optional

from .http import Http


class UserManagement(Http):
    def info_user(self, username: str) -> str:
        return self._user_manager(f"getUserInfo&name={username}")

    async def async_info_user(self, username: str) -> str:
        return await self._async_user_manager(f"getUserInfo&name={username}")

    @property
    def info_all_users(self) -> str:
        return self._user_manager("getUserInfoAll")

    @property
    async def async_info_all_users(self) -> str:
        return await self._async_user_manager("getUserInfoAll")

    @property
    def info_all_active_users(self) -> str:
        return self._user_manager("getActiveUserInfoAll")

    @property
    async def async_info_all_active_users(self) -> str:
        return await self._async_user_manager("getActiveUserInfoAll")

    def info_group(self, group: str) -> str:
        return self._user_manager(f"getGroupInfo&name={group}")

    async def async_info_group(self, group: str) -> str:
        return await self._async_user_manager(f"getGroupInfo&name={group}")

    @property
    def info_all_groups(self) -> str:
        return self._user_manager("getGroupInfoAll")

    @property
    async def async_info_all_groups(self) -> str:
        return await self._async_user_manager("getGroupInfoAll")

    def delete_user(self, username: str) -> str:
        return self._user_manager(f"deleteUser&name={username}")

    async def async_delete_user(self, username: str) -> str:
        return await self._async_user_manager(f"deleteUser&name={username}")

    def add_user(
        self,
        username: str,
        password: str,
        group: str,
        sharable: bool = True,
        reserved: bool = False,
        memo: Optional[str] = None,
    ) -> str:
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

        cmd = (
            "addUser"
            f"&user.Name={username}"
            f"&user.Password={password}"
            f"&user.Group={group.lower()}"
            f"&user.Sharable={str(sharable).lower()}"
            f"&user.Reserved={str(reserved).lower()}"
        )

        if memo:
            cmd += f"&user.Memo={memo}"

        return self._user_manager(cmd)

    async def async_add_user(
        self,
        username: str,
        password: str,
        group: str,
        sharable: bool = True,
        reserved: bool = False,
        memo: Optional[str] = None,
    ) -> str:
        cmd = (
            "addUser"
            f"&user.Name={username}"
            f"&user.Password={password}"
            f"&user.Group={group.lower()}"
            f"&user.Sharable={str(sharable).lower()}"
            f"&user.Reserved={str(reserved).lower()}"
        )

        if memo:
            cmd += f"&user.Memo={memo}"

        return await self._async_user_manager(cmd)

    def modify_password(self, username: str, newpwd: str, oldpwd: str) -> str:
        """
        Params:
            username - user name
            newpwd - new password
            oldpwd - old password
        """
        return self._user_manager(
            f"modifyPassword&name={username}&pwd={newpwd}&pwdOld={oldpwd}"
        )

    async def async_modify_password(
        self, username: str, newpwd: str, oldpwd: str
    ) -> str:
        return await self._async_user_manager(
            f"modifyPassword&name={username}&pwd={newpwd}&pwdOld={oldpwd}"
        )

    def modify_user(self, username: str, attribute: str, value: str) -> str:
        """
        Params:
            username - username for user
            attribute - the attribute name that will change:
                        group, sharable, reserved, memo

            value - the new value for attribute
        """

        cmd = f"modifyUser&name={username}"

        if attribute.lower() == "group":
            cmd += f"&user.Group={value.lower()}"

        elif attribute.lower() == "sharable":
            cmd += f"&user.Sharable={value.lower()}"

        elif attribute.lower() == "reserved":
            cmd += f"&user.Reserved={value.lower()}"

        elif attribute == "memo":
            cmd += f"&user.Memo={value.lower()}"

        return self._user_manager(cmd)

    async def async_modify_user(
        self, username: str, attribute: str, value: str
    ) -> str:
        cmd = f"modifyUser&name={username}"

        if attribute.lower() == "group":
            cmd += f"&user.Group={value.lower()}"

        elif attribute.lower() == "sharable":
            cmd += f"&user.Sharable={value.lower()}"

        elif attribute.lower() == "reserved":
            cmd += f"&user.Reserved={value.lower()}"

        elif attribute == "memo":
            cmd += f"&user.Memo={value.lower()}"

        return await self._async_user_manager(cmd)

    def _user_manager(self, action: str) -> str:
        ret = self.command(f"userManager.cgi?action={action}")
        return ret.content.decode()

    async def _async_user_manager(self, action: str) -> str:
        ret = await self.async_command(f"userManager.cgi?action={action}")
        return ret.content.decode()
