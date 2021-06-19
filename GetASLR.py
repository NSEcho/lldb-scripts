import lldb

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
END='\033[0m'

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f GetASLR.getOffset aslr')

def getOffset(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()

    module_index = 0

    if command != "":
        module_name = command

        found = False

        for module in target.module_iter():
            if module_name == module.GetFileSpec().GetFilename():
                found = True
                break
            module_index += 1

        if not found:
            print('\033[0;31m[-] Could not find module\033[0m')
            return

    base_address = int(target.GetModuleAtIndex(module_index).GetObjectFileHeaderAddress().GetFileAddress())
    load_address = int(target.GetModuleAtIndex(module_index).GetObjectFileHeaderAddress().GetLoadAddress(target))
    offset = load_address - base_address
    print('[*] Offset is ' + hex(offset))
