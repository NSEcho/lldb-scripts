import lldb
import re

RED = '\033[91m'
END = '\033[0m'
GREEN = '\033[32m'

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f GetButtonMethod.getMethod getButtonMethod')

def getMethod(debugger, command, result, internal_dict):
    button = command
    all_targets = executeCommand('[' + button + ' allTargets]').description

    m = re.search(r'(?<=\<)([^:]+):\s([^>]+)', all_targets)

    if not m:
        print(CRED + '[-] Could not find description' + END)
        return

    controller_name = m.group(1)
    controller_addr = m.group(2)
    
    # Obtain allControlEvents
    all_control_events = executeCommand('[' + button + ' allControlEvents]').GetValue()
    method_name = executeCommand('[' + button + ' actionsForTarget:' + controller_addr + ' forControlEvent:' + all_control_events + ']').description
    m = re.search(r'(?<=\()([^\)]+)', method_name)
    if not m:
        print(CRED + '[-] Could not obtain method name' + END)
        return

    print(GREEN + '[+] Method for button is {} => {}'.format(controller_name, m.group().strip()) + END)


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
