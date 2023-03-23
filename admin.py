# coding:utf-8

"""
    1. admin 类的搭建
    2. 获取用户函数（包含获取身份）
    3. 添加用户（判断当前身份是否是管理员）
    4. 冻结与恢复用户
    5. 修改用户身份

    6. admin 的验证（只有admin的用户才能使用这个类）
    7. 任何函数都应该动态的更新getuser
    8. 奖品的添加
    9. 奖品的删除
    10. 奖品数量的更新
"""

import os

from base import Base
from common.error import NotUserError, UserActiveError, RoleError


class Admin(Base):

    def __init__(self, username, user_json, gift_json):
        self.username = username
        super().__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()
        current_user = users.get(self.username)
        if current_user == None:
            raise NotUserError('%s 用户不存在' % self.username)

        # if current_user.get('active') == False:
            # raise UserActiveError('此用户 %s 已经不可用了' % self.username)

        if current_user.get('role') != 'admin':
            raise RoleError('请使用管理员账号登录')

        self.activity(current_user)

        self.user = current_user
        self.role = current_user.get('role')
        self.name = current_user.get('username')
        self.active = current_user.get('active')

        print('用户：%s 已经成功登录' % self.name)

    def __check(self, message):
        self.get_user()
        if self.role != 'admin':
            raise Exception(message)

    def add_user(self, username, role):
        self.__check('没有权限')
        self._Base__write_user(username=username, role=role)

    def updata_user_active(self, username):
        self.__check('没有权限')
        self._Base__change_active(username=username)

    def updata_user_role(self, username, role):
        self.__check('没有权限')
        self._Base__change_role(username=username, role=role)

    def add_gift(self, first_level, second_level, gift_name, gift_count):
        self.__check('没有权限')
        self._Base__write_gift(first_level=first_level, second_level=second_level, gift_name=gift_name, gift_count=gift_count)

    def delete_gift(self, first_level, second_level, gift_name):
        self.__check('没有权限')
        self._Base__delete_gift(first_level=first_level, second_level=second_level, gift_name=gift_name)

    def updata_gift(self, first_level, second_level, gift_name, gift_count, is_admin):
        self.__check('没有权限')
        self._Base__gift_updata(first_level=first_level, second_level=second_level, gift_name=gift_name, gift_count=gift_count, is_admin=is_admin)


if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    admin = Admin('lice', user_path, gift_path)
    # print(admin.name, admin.role)
    # admin.updata_user_role(username='zhiyadi', role='admin')
    # admin.updata_gift(first_level='level1', second_level='level2', gift_name='iphone15', gift_count=100, is_admin=True)
