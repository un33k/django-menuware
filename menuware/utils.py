from importlib import import_module


def get_callable(func_or_path):
    """
    Receives a dotted path or a callable, Returns a callable or None
    """
    if callable(func_or_path):
        return func_or_path

    module_name = '.'.join(func_or_path.split('.')[:-1])
    function_name = func_or_path.split('.')[-1]
    _module = import_module(module_name)
    func = getattr(_module, function_name)
    return func


def is_superuser(request):
    return is_authenticated(request) and request.user.is_superuser


def is_staff(request):
    return is_authenticated(request) and request.user.is_staff


def is_authenticated(request):
    return request.user.is_authenticated


def is_anonymous(request):
    return not request.user.is_authenticated
