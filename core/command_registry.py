class Registry:
    def __init__(self):
        self.commands = {}
        self.pending_args = {}

    def register_decorator(self, name: str, help_text: str = ""):
        def decorator(func):
            self.commands[name] = {
                'func': func,
                'help': help_text,
                'args': []
            }
            # Thêm các arguments đang chờ (nếu có) vào command
            if name in self.pending_args:
                self.commands[name]['args'].extend(self.pending_args[name])
                del self.pending_args[name]
            return func
        return decorator

    def register(self, name: str, func, help_text: str = ""):
        self.commands[name] = {
            'func': func,
            'help': help_text,
            'args': []
        }
        if name in self.pending_args:
            self.commands[name]['args'].extend(self.pending_args[name])
            del self.pending_args[name]

    def add_argument_decorator(self, command_name: str, *args, **kwargs):
        def decorator(func):
            if command_name in self.commands:
                self.commands[command_name]['args'].append((args, kwargs))
            else:
                # Nếu command chưa được đăng ký, lưu argument vào pending
                if command_name not in self.pending_args:
                    self.pending_args[command_name] = []
                self.pending_args[command_name].append((args, kwargs))
            return func
        return decorator

    def add_argument(self, command_name: str, *args, **kwargs):
        """Thêm argument cho command mà không cần decorator"""
        if command_name in self.commands:
            self.commands[command_name]['args'].append((args, kwargs))
        else:
            if command_name not in self.pending_args:
                self.pending_args[command_name] = []
            self.pending_args[command_name].append((args, kwargs))
# Tạo instance mặc định để sử dụng trong toàn bộ ứng dụng
registry = Registry()
