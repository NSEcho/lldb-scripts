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

def executeCommand(command):
    debugger = lldb.debugger
    process = debugger.GetSelectedTarget().GetProcess()
    frame = process.GetSelectedThread().GetSelectedFrame()
    target = debugger.GetSelectedTarget()

    expr_options = lldb.SBExpressionOptions()
    expr_options.SetIgnoreBreakpoints(False);
    expr_options.SetFetchDynamicValue(lldb.eDynamicCanRunTarget);
    expr_options.SetTimeoutInMicroSeconds (30*1000*1000) # 30 second timeout
    expr_options.SetTryAllThreads (True)
    expr_options.SetUnwindOnError(False)
    expr_options.SetGenerateDebugInfo(True)
    expr_options.SetLanguage (lldb.eLanguageTypeObjC)
    expr_options.SetCoerceResultToId(True)
    return frame.EvaluateExpression(command, expr_options)
