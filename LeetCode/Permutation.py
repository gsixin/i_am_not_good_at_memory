import copy


class Solution:
    def permute(self, nums):
        nlen = len(nums)
        if nlen == 2:
            return [[nums[0], nums[1]], [nums[1], nums[0]]]
        elif nlen > 2:
            conversion = nums[0:nlen-1]
            new = nums[nlen-1]
            tmpR = self.permute(conversion)
            res = []
            for p in tmpR:
                for index in range(len(p)+1):
                    tmp = copy.deepcopy(p)
                    tmp.insert(index, new)
                    res.append(tmp)
            return res
        else:
            return [nums]


obj = Solution()
print(obj.permute([1, 2, 3]))
