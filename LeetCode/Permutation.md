## 排列的实现
### 全排列的递归实现
* 仅传入数组本身，递归出需要的排列类型
  使用比当前数组的减一子数组产生全排列（递归点），然后再产生当前数组的全排列。
  递归方法返回的是数组类型，数组元素是某一全排列（数组类型），针对一个全排列，在新插入一个元素时候，它又可以产生当前全排列数组元素个数+1个全排列。
~~~py
class Solution:   
    import copy
    def permute(self, nums):
        nlen=len(nums)
        if nlen==2:
            return [[nums[0],nums[1]],[nums[1],nums[0]]]
        elif nlen>2:
            conversion=nums[0:nlen-1]
            new=nums[nlen-1]
            tmpR=self.permute(conversion)
            res=[]
            for p in tmpR:
                for index in range(len(p)+1):
                    tmp=copy.deepcopy(p)
                    tmp.insert(index,new)
                    res.append(tmp)
            return res
        else:
            return [nums]
~~~