#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:52
# @Author  : @乌鸦坐飞机
# Description   : 心形图

# print('\n'.join([''.join([('LoveLiTong'[(x - y) % len('LoveLiTong')] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (
#             x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(20, -30, -1)]))


# class Solution(object):
#     def twoSum(self, nums, target):
#         """
#         :type nums: List[int]
#         :type target: int
#         :rtype: List[int]
#         """
#         result = []
#         a = 0
#         b = 0
#         for i in nums:
#             for j in nums[1:]:
#                 if (i + j == target):
#                     a = nums.index(i)
#                     b = nums.index(j)
#                     break
#         result.append(a)
#         result.append(b)
#
#
#
#         return result
#
#
# if __name__ == '__main__':
#     demo = [2, 7, 11, 15]
#     t = 9
#     myS = Solution()
#     print(myS.twoSum(demo, t))
