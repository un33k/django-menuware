from importlib import import_module


def get_func(dotted_path):
    module_name = '.'.join(dotted_path.split('.')[:-1])
    function_name = dotted_path.split('.')[-1]
    _module = import_module(module_name)
    func = getattr(_module, function_name)
    return func
