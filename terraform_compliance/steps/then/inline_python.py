import importlib.util
from radish import world

def inline_python(_step_obj, file_name, function_name):

    # if file was already imported
    if file_name in inline_python.file_names:
        mod = inline_python.file_names[file_name]

    else:
        path = _step_obj.path
        path = path[0:path.rfind('/')+1] + file_name

        spec = importlib.util.spec_from_file_location('user_imported', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        inline_python.file_names[file_name] = mod

    f = getattr(mod, function_name)

    return f(_step_obj)

inline_python.file_names = {}
