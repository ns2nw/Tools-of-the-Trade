#Nandita Sangwan
#ns2nw

https://leetcode.com/problems/two-sum/

solution:
def two_sum(nums, target):
    d = {}
    for i in range(len(nums)):
        x = nums[i]
        if target - x in dict:
            return (d[target - x] + 1, i + 1)
        d[x] = i
    return None
