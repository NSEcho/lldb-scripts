import lldb
import re

RED = '\033[91m'
GREEN = '\033[32m'
CYAN = '\033[36m'
END = '\033[0m'

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f PPBlock.getBlock ppblock')

def getBlock(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    if len(command) == 0:
        err("missing address of the block")
        return 
    info("Info for block @" + command + "\n")

    res = lldb.SBCommandReturnObject()
    intr = debugger.GetCommandInterpreter()

    cmd = 'memory read --size 8 --format x {} -c4'.format(command)
    output = get_command_output(intr, res, cmd).split()

    body = output[4].strip()

    cmd = 'memory read --size 4 --format x {} -c3'.format(command)
    flags = get_command_output(intr, res, cmd).split()[3]
    has_sel = int(flags[2:], 16) & (1 << 30)

    if has_sel == 0:
        err("Block has no selector")
        return

    has_copy_dispose = int(flags[2:], 16) & (1 << 25)

    if has_copy_dispose != 0:
        err("Block with copy and dispose helpers are not supported")
        return

    sel_struct = output[5].strip()

    outt("Body @" + body)
    outt("Sel @" + sel_struct)

    cmd = 'memory read --size 8 --format x {}+0x10 -c1'.format(sel_struct)
    output = get_command_output(intr, res, cmd)
    encoding_addr = output.split()[1]

    cmd = 'expr -l objc -O -- (char*){}'.format(encoding_addr)
    encoding = get_command_output(intr, res, cmd)
    outt('Sel encoding ' + encoding)

    cmd = 'expr -l objc -O -- [(NSMethodSignature*)[NSMethodSignature signatureWithObjCTypes:{}] numberOfArguments]'.format(encoding)
    num_arguments = int(get_command_output(intr, res, cmd))
    outt("Number of arguments: " + str(num_arguments-1))

    for i in range(num_arguments-1):
        cmd = 'expr -l objc -O -- [(NSMethodSignature*)[NSMethodSignature signatureWithObjCTypes:{}] getArgumentTypeAtIndex:{}]'.format(encoding, i+1)
        ar_type = get_command_output(intr, res, cmd)
        outt("\tArgument " + str(i) + " " + ar_type)

    cmd = 'expr -l objc -O -- [(NSMethodSignature*)[NSMethodSignature signatureWithObjCTypes:{}] methodReturnType]'.format(encoding)
    ret_type = get_command_output(intr, res, cmd)
    outt("Return type: " + ret_type)


def get_command_output(intr, res, cmd):
    intr.HandleCommand(cmd, res)
    ret = res.GetOutput().strip()
    return ret

def info(message):
    print(GREEN + message + END)

def err(err):
    print(RED + err + END)

def outt(message):
    print(CYAN + message + END)
