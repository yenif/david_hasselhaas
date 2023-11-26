import os
import inspect
from .filter import Filter


class RestrictPathToDir(Filter):
    def __init__(self, restricted_directory, tool):
        super().__init__(tool)
        self.restricted_directory = os.path.abspath(restricted_directory)

    def _convert_to_absolute(self, path):
        # Convert a relative path to absolute path relative to 'restricted_directory'.
        # If it's already absolute, verify it is a subpath of 'restricted_directory'.
        abs_path = os.path.abspath(os.path.join(self.restricted_directory, path))
        if not abs_path.startswith(self.restricted_directory):
            raise ValueError(f"The path {path} is not within the restricted directory {self.restricted_directory}")
        return abs_path

    def do_it(self, *args, **kwargs):
        # Get list of argument names for the tool's do_it
        arg_names = [param.name for param in inspect.signature(self.tool.do_it).parameters.values()]

        # Determine the key used for the path argument, if any
        path_keys = set(arg_names) & set(['path', 'relative_path'])
        try:
            path_key = path_keys.pop()
        except KeyError as e:
            raise ValueError(f"Tool {self.tool.name} does not have a path argument.") from e

        # Update the path in kwargs
        if path_key in kwargs:
            kwargs[path_key] = self._convert_to_absolute(kwargs[path_key])
        else:
            path_index = arg_names.index(path_key)
            args = list(args)
            args[path_index] = self._convert_to_absolute(args[path_index])
            args = tuple(args)

        # Call the original method with possibly modified arguments
        return super().do_it(*args, **kwargs)
