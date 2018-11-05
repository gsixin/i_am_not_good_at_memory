## requireJs原理介绍
## requireJs的模块加载和依赖机制的分析和简单实现
requireJs 的文件加载和依赖管理确实非常好用，相信大家都有这个体会。在此之前，我们的Html文件头部总是要有一长串的script标签来引入js文件，并且还必须非常注意script标签的先后顺序。
这篇文章对requireJs的核心功能做了简单的实现，希望能帮助大家更好立即requireJs。
下面的思路是参考requireJs 0.0.7版本实现的。之前有尝试理解当前版本的requireJs的源码，不过最后发现这不是短时间能搞定的。无奈之下找了GitHub上先前较早的版本，那时还没有那么多配置项，代码结构更简单一点。
***
### 1 首先我们有这样一个文件结构：
```js
js/require.js
js/main.js
js/a.js
js/b.js
js/a1.js
js/a2.js
js/b1.js
js/b2.js
index.html
```
我们的入口文件是main.js,在入口文件中，我们调用了require函数。
```js
require(["a","b"],function(a,b){
    //do something
});
```
我们看上面的require函数中，回调函数的执行依赖于a和b两个模块，然后我们的a.js文件像这样：
```js
define("a",["a1","a2"],function(a1,b1){
    //do something
});
```
可以看到a模块依赖于a1和a2模块。
a1模块像这样：
```js
define("a1",function(){
    //do something
});
```
同理b模块依赖于b1和b2，文件结构类似。
***
### 2 先说说require和define函数的关系。
require和define函数接收同样的参数，不同的是，define函数被建议在一个文件中只使用一次，用它来定义模块。
require函数一般在入口文件或者顶层代码中使用，用来加载和使用模块。
其实在我看来，require函数可以看做是特殊的define函数，它用来定义一个顶层匿名模块，这个模块不需要被其他模块加载。
二者的区别这里有一下介绍：[requireJs中require和define的定位以及使用区别](https://www.zhihu.com/question/21260764)
***
### 3 requireJs中的执行流程
#### 一、requireJs首先找打data-main属性，然后根据属性值（通过新建一个script标签）加载并解析入口文件。
下面看入口文件的`require(["a","b"],function(){})`调用发生了什么。
#### 二、在require函数中，我们先生成一个简单的模块对象，大概是这样的：
```{
    moduleName:"_@$1",
    deps:["a","b"],
    callback:function(){},
    callbackReturn:null,args:[]}
```
对这个模块对象属性的解释：
moduleName：模块名称，前面我们说了，require函数可以看做是定义一个匿名的顶层模块对象。所以这里生成了 一个内部名称"_@$1"
deps：依赖数组；包含当前模块依赖的模块。
callback：回调函数。require中那个回调函数。
callbackReturn：回调函数返回值。
args：数组，对应依赖模块的传递回来的值。

我们在全局设置一个context对象
```js
context={};               
context.topModule=""      //存储require函数调用生成的顶层模块对象名
context.modules={};       //存储所有的模块。使用模块名作为key，模块对象作为value
context.loaded=[];        //加载好的模块
context.waiting=[];       //等到加载完成的模块
```
我们在这里设置：
```js
context.topModule="_@$1";//因为当前定义的是一个顶层你们匿名模块，所以生成一个内部模块名。
context.modules中添加"_@$1"模块，结果见下一个代码段
```
```js
{
    "_@$1":{
        moduleName:"_@$1",     
        deps:["a","b"],
        callback:function(){},
        callbackReturn:null,
        args:[]
    }
}
```
context.waiting中添加依赖的模块，结果像这样：`["a","b"];   //把依赖的模块添加到waiting中`
然后我们便利依赖数组["a","b"]，分别创建script标签并加载，绑定好data-moduleName属性，和加载完成回调函数onscriptLoaded,在遍历中大概像这样：
```js
var script=document.createElement("script");
script.onload=onscriptLoaded;   //脚本加载后的回调函数。这个是核心函数。
script.setAttribute();  //为script元素添加data-moduleName属性，方便在回调函数中判断当前模块
script.src="js/a.js";
document.getElementsByTagName("head")[0].appendChild(script);
```
到这里，require函数就完成了。
#### 三、假设上面的js/a.js加载喊了，文件中执行了
```js
define("a",["a1","a2"],function(a1,b1){
    //do something
});
```
我们看看define中做了哪些事情。其实define函数和上面的require函数做了差不多相同的事情。
差别在于require自动生成了一个模块名"_@$1"，并且在require中设置了context.topModule。
而define
* 生成模块：
```js
{
    modulaName:"a",
    deps:["a1","a2"],
    callback:function(){},
    callbackReturn:null,
    args:[]
}
```
* 修改context变量，context.modules中添加当前模块，结果如下：
```js
{
    "_@$1":{
        moduleName:"_@$1",
        deps:["a","b"],
        callback:function(){},
        callbackReturn:null,
        args:[]
        },
    "a":{
        moduleName:"a",
        deps:["a1","a2"],
        callback:function(){},
        callbackReturn:null,
        args:[]
        }
}
```
context.waiting添加当前依赖数组。 --结果["a","b","a1","b1"]
然后接着根据依赖数组创建script标签，绑定data-moduleName属性，绑定回调函数oncsriptLoaded
##### 四、最后的关键函数onscriptLoaded
```js
function onscriptLoaded(event){
//思路大概是这样：
//1、根据event对象，我们可以得到加载完成的script元素，得到它的data-moduleName属性，这个属性就是模块名。
//2、在全局context对象中，给context.loaded数组中加上这个模块名。context.waiting数组中减去这个模块名。
//3、接下来判断，如果context.waiting数组不为空则返回。
//4、否则，如果context.waiting为空数组，表明所有的依赖都已经加载了。
//接下来是重头戏
//5、创建一个递归函数来执行模块回调函数，像这样：

function exec(module){
    var deps=module.deps;         //当前模块的依赖数组
    var args=module.args;         //当前模块的回调函数参数
    for(var i=0,len=deps.length;i<len;i++){     //遍历
        var dep=context.modules[deps[i]];       
        args[i]=exec(dep);                      //递归得到依赖返回值作为对应参数
    }
    return module.callback.apply(module,args);  //调用回调函数，传递给依赖模块对应的参数
}
var topModule=context.modules[context.topModule];    //找到顶层模块。
exec(topModule);                                     //开始执行递归函数
}                                                    //onscriptLoaded结束
```

整个实现的思路就是：我们在define和require中定义模块时，所有的依赖的模块名都被添加到了context.waiting数组中。每个依赖在加载时的script标签都绑定了onload事件，在事件回调函数中我们把当前模块名从context.waiting中删除，接着我们判断context.waiting是否为空，为空意味着所有模块的文件都加载好了，此时就可以从顶层模块开始，使用一个递归函数来执行模块的回调函数。
***
***
## 最后
我本就只是想写出一个核心的思路，所以代码中很多地方还是值得琢磨，可能并不正确，但整体的思路没错。
注意，这里我在使用define函数时，模块名参数我并没有省略，这是因为，在本篇文章的实现思路中，我并没有更多篇幅来解释怎么实现define函数的省略模块名。大概的思路可能是在define执行时，我们并不知道当前定义的模块的模块名，所以我们创建一个临时的模块名，然后全局中设置一个变量temp指向这个模块。考虑到define函数执行后，它所在的script标签的onload时间必然会紧接着触发，而且这个script标签上有data-moduleName绑定了正确的模块名，所以我们可以在onload事件回调函数中找到temp指向的模块，然后修改它的模块名。
之前本来准备写篇关于requireJs Api的详解，最后发现自己墨水有限，好多东西只可意会不能言传，最后放弃了。如果关于这篇文章大家有什么好的意见和建议，请与我讨论，我们一起来完善这篇文章。

[share link](https://www.cnblogs.com/cheerfulCoder/p/4339742.html)

![西索大大](https://timgsa.baidu.com/t36.jpg "sisoka sama")

| 表头1111111111 | 表头2111  | 表头233 |
| -------------- | :-------: | :-----: |
| 内容           | 内ddddd容 | 内容    |
| 表头           | 表头      | 表头    |





>$$y=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$$
>>$$y=\frac{\frac{1}{2}x+3}{\frac{2}{3}}$$
> 
>$33+\frac{\frac{x}{2}x+3\frac{z}{\frac{t}{5}}}{\frac{2}{3}+\frac{j}{\frac{i}{3}}}$ 