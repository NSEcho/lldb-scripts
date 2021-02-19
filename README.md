# Description

`getButtonMethod` is a useful lldb command for reverse engineering and analyzing iOS applications. It enables you to find out what method is responsible for button and inside which controller(header file).

Simply pass the memory address of button and wait for the green color.

# Installation
```
$ git clone https://github.com/XdaemonX/lldb-scripts.git
$ lldb
...
(lldb) command script import /path/to/lldb-script/directory/GetButtonMethod.py
$ getButtonMethod 0xdeadbeef
[+] Method for button is ExampleController => buttonTouched:
```

# Note
To get full lldb experience, add following into your `.lldbinit` file:

`command alias -- printSubviews expression -l objc -O -- [[[[[UIApplication sharedApplication] keyWindow] rootViewController] view] recursiveDescription]`. 

This will dump entire view hierarychy just like `ios ui dump` in _objection_ does or `[[UIApp keyWindow] recursiveDescription]` inside _Cycrypt_ does so you can easily find a button whose method you want to see.
