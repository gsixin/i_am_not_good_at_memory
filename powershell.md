## powershell manual for myself
###### 内容总结绝大部分来自：[https://www.pstips.net/](https://www.pstips.net/)以及[微软官网](https://docs.microsoft.com/en-us/powershell/scripting/powershell-scripting?view=powershell-6)
### 简介
微软官网的介绍：

PowerShell is a task-based command-line shell and scripting language built on .NET. PowerShell helps system administrators and power-users rapidly automate tasks that manage operating systems (Linux, macOS, and Windows) and processes.

PowerShell commands let you manage computers from the command line. PowerShell providers let you access data stores, such as the registry and certificate store, as easily as you access the file system. PowerShell includes a rich expression parser and a fully developed scripting language.

总之，至于我自己的用处可能是以下几个吧：
* 装逼用
* 直接用powershell，可以抛弃cmd了
* 编写脚本，实现一些自动化的系统功能，也可有限的进行一些编程,代替csharp更方便的实现一些小功能

但是有一点很不能忍，powershell的背景色和前景色设置已经一些字体的显示太娘的扯淡了，深蓝背景，黑色字体，妈的什么也看不清楚啊。而且属性调整很费劲，而且，目前还不知道在哪里调整输入文本的颜色，不知道能不能调整。

#### 快捷键

快捷键还好，cmd用的顺手，这里直接用就行，对自己来说，最新学的一个是ctrl+c吧。在运维上并没有太严重的需求，也就没有太大必要去研究快捷键。
* ctrl+c 取消正在执行的命令
* 上/下 切换命令行的历史记录
* esc 清空当前命令行

#### 管道和重定向
* 管道：操作上一条命令的结果
* 重定向：将结果输出到某文件中   >    >>

### 交互式
* 数学运算
  * 加减乘除模;简单的进制转换
  * KB/MB/GB/TB/PB：单位间换算计算可以直接用于计算
    ```
    > 1pb/1tb
    1024
    ```
    pv:pageview,页面浏览量
* 执行外部命令
  * netstat   |   ipconfig   |   route print   |   cmd      exit etc...
  * 可以跟cmd样启动外部程序，start . 打开当前目录的资源管理器，或者打开notepad++，vscode之类的东西
* 命令集
  * 比较抱歉，没看懂这是什么意思
* 别名（alias）
  别名是命令集中命令的一些简称（别名），目的是简化命令，提高使用效率，还可自定义别名。
* 通过函数扩展别名
  命令时常需要输入一定的参数，将常用参数固化在别名中，更加提高执行效率，不过这个还没怎么研究。
* 执行文件和脚本
  这个应该好好研究下