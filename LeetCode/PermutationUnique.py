import copy


class Solution:
    def permuteUnique(self, nums):
        nums.sort()
        nlen = len(nums)
        if nlen == 1:
            return [[nums[0]]]
        elif nlen > 1:
            conversion = nums[0:nlen-1]
            new = nums[nlen-1]
            tmpR = self.permuteUnique(conversion)
            res = []
            for p in tmpR:
                countE = 0
                coiuntNotE = 0
                for index in range(len(p)+1):
                    tmp = copy.deepcopy(p)
                    if index < len(p):
                        if tmp[index] == new:
                            coiuntNotE = 0
                            countE += 1
                        else:
                            coiuntNotE += 1
                            countE = 0
                        if countE == 1:
                            tmp.insert(index, new)
                            res.append(tmp)
                        if coiuntNotE > 1:
                            tmp.insert(index, new)
                            res.append(tmp)
                        if coiuntNotE == 1 and index == 0:
                            tmp.insert(index, new)
                            res.append(tmp)
                    else:
                        if coiuntNotE >= 1:
                            tmp.insert(index, new)
                            res.append(tmp)
            return res
        else:
            return [nums]


obj = Solution()
print(obj.permute([1, 2]))
