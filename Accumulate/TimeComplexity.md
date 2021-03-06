## 时间复杂度问题：
> 时间复杂度指的是代码的运次次数问题，次数越多，复杂程度越高，通常用几种数学模型来表示算法的复杂程度。1s内可以求出解的时间复杂度`O(*)`和数据规模的对应关系如下：

$n$---------------------->1000,000
$nlogn$--------------->100,000
$n\sqrt{n}$----------------->10,000
$n^2;n^2logn$-------->1000
$n^3$-------------------->100
$2^n$-------------------->20
$n!$--------------------->10(通常一些搜索算法)

> 性能调整问题的一个重要点
>> 固然降低算法的时间复杂度是优化执行效率的最重要手段，时间性能优化的前提是：一定要找到耗时点在哪里，找到具体那个`code statement`是耗时的，不能漫无目的的猜测着修改！利用好语言本身提供的基础的计时工具（C#的`Stopwatch`）,好好利用，它们是能靠谱反应代码执行时间的。一定要找到耗时点在哪。
