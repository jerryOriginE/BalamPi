commands = {}

def register(name):
    def decorator(func):
        commands[name] = func
        return func 
    return decorator