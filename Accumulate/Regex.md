## 有关正则表达式的学习记录

### 效率问题

虽然正则的功能非常强大，但是据说正则的效率是个很值得商榷的问题。而且还据说跟pattern的质量有很大关系，同样功能不同pattern的效率可能差很大。

* pattern匹配数量多少的简单测试
```csharp
Stopwatch sw = new Stopwatch();
int frequency = 1000000;
sw.Restart();
for (int i = 0; i < frequency; i++)
{
    //Regex.Matches("test string","test",RegexOptions.Singleline);
    Regex.Replace("test k          string", " ","", RegexOptions.Singleline);
}
sw.Stop();
Console.WriteLine($"耗时：{sw.ElapsedMilliseconds}ms");
sw.Restart();
for (int i = 0; i < frequency; i++)
{
   // Regex.Matches("test string", "tet", RegexOptions.Singleline);
    Regex.Replace("teststr  ing", " ", "", RegexOptions.Singleline);
}
sw.Stop();
Console.WriteLine($"耗时：{sw.ElapsedMilliseconds}ms");
Console.WriteLine("Hello World!");
Console.ReadLine();
```
具体的运行时间就不贴出来了，1000000次，看到的时间差距大概几可能有几倍到十几倍吧。要是需要在循环中大量用正则，需要十分小心了，现在这个项目就要重点做这方面的优化了。