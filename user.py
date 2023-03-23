# coding:utf-8

"""
    1. user 类的初始化
    2. get_user 时间的转变
    3. 查看奖品列表

    1. 抽奖函数 随机判断第一层（level1) 1:50%  2:30%  3:15%  4:5%
    2. 抽奖函数 随机判断第二层（level2）1:80%  2:15%  3:5%
    3. 抽奖函数 随机获取到对应层级的真实奖品，查看奖品数量是否为0
        奖品数量不为0，则使奖品数量减1，更新奖品库，提示用户中奖
        奖品数量为0，则未中奖
"""


from common.utils import timestamp_to_str
from base import Base
from common.error import NotUserError, RoleError, UserActiveError, CountError

import os
import random


class User(Base):
    def __init__(self, username, user_json, gift_json):
        self.username = username
        self.gift_random = list(range(1, 101))

        super().__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()

        if self.username not in users:
            raise NotUserError('%s 用户不存在' % self.username)

        current_user = users.get(self.username)

        if current_user.get('active') == False:
            raise UserActiveError('此用户 %s 已经不可用了' % self.username)

        if current_user.get('role') != 'normal':
            raise RoleError('请使用普通账号登录')

        self.user = current_user
        self.name = current_user.get('username')
        self.role = current_user.get('role')
        self.gifts = current_user.get('gifts')
        self.create_time = timestamp_to_str(current_user.get('create_time'))

    def get_gifts(self):
        gifts = self._Base__read_gifts()
        gift_lists = []

        for level_one, level_one_pool in gifts.items():
            for level_two, level_two_pool in level_one_pool.items():
                for name, detail in level_two_pool.items():
                    gift_lists.append(detail.get('name'))
        return gift_lists

    def choice_gift(self):
        self.get_user()
        # level1 get
        first_level, second_level = None, None
        level_one_count = random.choice(self.gift_random)
        if 1 <= level_one_count <= 50:
            first_level = 'level1'
        elif 51 <= level_one_count <= 80:
            first_level = 'level2'
        elif 81 <= level_one_count < 95:
            first_level = 'level3'
        elif level_one_count >= 95:
            first_level = 'level4'
        else:
            raise CountError('level_one_count 需要取值在0~100之间')

        gifts = self._Base__read_gifts()
        level_one = gifts.get(first_level)

        level_two_count = random.choice(self.gift_random)
        if 1 <= level_two_count <= 80:
            second_level = 'level1'
        elif 81 <= level_two_count <= 95:
            second_level = 'level2'
        elif 95 < level_two_count <=100:
            second_level = 'level3'
        else:
            raise CountError('level_two_count 需要取值在0~100之间')

        level_two = level_one.get(second_level)
        if len(level_two) == 0:
            print('nice try')
            return

        gift_names = []
        for k, _ in level_two.items():
            gift_names.append(k)

        gift_name = random.choice(gift_names)
        gift_info = level_two.get(gift_name)
        if gift_info.get('count') <= 0:
            print('nice try')
            return

        gift_info['count'] -= 1
        level_two[gift_name] = gift_info
        level_one[second_level] = level_two
        gifts[first_level] = level_one

        self._Base__save(gifts, self.gift_json)
        self.user['gifts'].append(gift_name)
        self.updata()
        print('恭喜你抽中了 %s 一个' % gift_name)

    def updata(self):
        users = self._Base__read_users()
        users[self.username] = self.user

        self._Base__save(users, self.user_json)


if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    user = User('zhiyadi', user_path, gift_path)
    # print(user.name, user.create_time, user.gifts, user.role)
    # result = user.get_gifts()
    # print(result)
    user.choice_gift()
