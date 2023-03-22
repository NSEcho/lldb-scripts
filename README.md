# Description

Repo for my lldb scripts, you too may find them useful. They are mostly developed with iOS debugging in mind.



# Installation
```
$ git clone https://github.com/lateralusd/lldb-scripts.git
$ lldb
...
(lldb) command script import /path/to/lldb-scripts/directory/GetButtonMethod.py
(lldb) command script import /path/to/lldb-scripts/directory/GetASLR.py
(lldb) command script import /path/to/lldb-scripts/directory/PPBlock.py
$ getButtonMethod 0xdeadbeef
[+] Method for button is ExampleController => buttonTouched:
$ aslr PushKit
[*] Offset is 0x1a2d0000
(lldb) ppblock 0x0000000100004050
Info for block @0x0000000100004050

Body @0x0000000100003f00
Sel @0x0000000100004030
Sel encoding "v24@?0@\"NSString\"8@\"NSString\"16"
Number of arguments: 2
	Argument 0 "@\"NSString\""
	Argument 1 "@\"NSString\""
Return type: "v"
```

# getButtonMethod


`getButtonMethod` is a useful lldb command for reverse engineering and analyzing iOS applications. It enables you to find out what method is responsible for button and inside which controller(header file).

Simply pass the memory address of button and wait for the green color.

# aslr

`aslr` command enables you to find ASLR offset for specific module. Sometimes when you want to set a breakpoint on certain memory location from disassembled binary, you can't do it directly without adding ASLR offset to it, like `address = base_address + aslr_offset`

# ppblock

`ppblock` makes a bit sense of objective c blocks, it prints following information:

* body of the block
* number of arguments that the block receives
* types of arguments
* return type

All types are in objective c encoding(e.g. `v` means `void`)

# Remotely debugging 

I have already described it at my [blog - Debugging apps on jailbroken device](https://lateralusd.github.io/debugging/) but basically you attach to the app using `debugserver` on your iPhone and then on your Mac you start lldb and connect to it and start debugging just like it was running locally.

# Note
To get full lldb experience, add following into your `.lldbinit`(lldb config file that gets loaded when lldb is run) file:

`command alias -- printSubviews expression -l objc -O -- [[[[[UIApplication sharedApplication] keyWindow] rootViewController] view] recursiveDescription]`. 

This will dump entire view hierarychy just like `ios ui dump` in _objection_ does or `[[UIApp keyWindow] recursiveDescription]` inside _Cycrypt_ does so you can easily find a button whose method you want to see.
