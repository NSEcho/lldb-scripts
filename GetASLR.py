import lldb
import re

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f GetASLR.getOffset getASLR')

def getOffset(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()

    module_name = command
    module_index = 0
    found = False

    for module in target.module_iter():
        if module_name == module.GetFileSpec().GetFilename():
            found = True
            break
        module_index += 1

    if not found:
        print('[-] Could not find module')
        return

    base_address = int(target.GetModuleAtIndex(module_index).GetObjectFileHeaderAddress().GetFileAddress())
    load_address = int(target.GetModuleAtIndex(module_index).GetObjectFileHeaderAddress().GetLoadAddress(target))
    offset = load_address - base_address
    print('[*] Offset is ' + hex(offset))
