## How to: Make Thread-Safe Calls to Windows Forms Controls
> Reference to [!How to:Make Thread-Safe Calls to Winform controls from MS doc...](https://docs.microsoft.com/en-us/dotnet/framework/winforms/controls/how-to-make-thread-safe-calls-to-windows-forms-controls)

非控件创建线程直接修改当前控件，这个操作是不允许的，VS debug模式下会直接报错[Control control name accessed from a thread other than the thread it was created on.]，release模式并没试过，总之非线程安全的操作是不对的。本篇分享怎么多线程修改UI控件的问题。

* 1使用InvokeRequired属性和Invoke方法
```csharp
//假设我们要异步/多线程修改一个textbox的text值
private void someBtn_Click(object sender,EventArgs e){
    Task.Run(()=>{
        this.ChangeTextBox1Value("some new string value");
    });
}
//定义一个方法用于检查InvokeRequired属性
//并且通过this.Invoke方法调用对象设置方法
//目前觉得这个方法的不好是：每次修改一个ui control的时候都要新建一个方法去操作它，比较繁琐
//不过还好的是，一般也不会同时修改N多个ui control
private void _ChangeTextBox1Value(string newString){
    if(this.textBox1.InvokeRequired){
        Action<string> tAc=this._ChangeTextBox1Value;
        this.Invoke(tAc,new object[]{newstring});
    }
    else{
        this.textBox1.text=newString;
    }
}
```

* 2使用Winform提供的BackgroundWorker控件
```csharp
//通过winform控件拖拽的方式产生this.backgroundWorker1
//通过属性界面给控件注册DoWork和ProgressChanged两个事件委托
//实现了点击执行，异步修改progressBar控件进度条的功能
private void bkgroundBtn_Click(object sender,EventArgs e){
    this.backgroundWorker1.RunWorkerAsync();
}
private void backgroundWorker1_DoWork(object sender,System.ComponentModel.DoWorkerEventArgs e){
Thread.Sleep(1000);
this.backgroundWorkers.ReportProgress(10);
Thread.Sleep(1000);
this.backgroundWorkers.ReportProgress(40);
Thread.Sleep(1000);
this.backgroundWorkers.ReportProgress(80);
Thread.Sleep(1000);
this.backgroundWorkers.ReportProgress(100);
}

private void backgroundWorker1_ProgressChanged(object sender,System.ComponentModel.ProgressChangedEventArgs e){
    //这句就是修后台修改UI Control的
    //这里可以写多个修改UI control的 statement  算是这种实现方式的一个优点
    this.progressBar1.Value=e.ProgressPercentage;
}
```
* 3修改Control.CheckForIllegalCrossThreadCalls属性，及其不推荐。