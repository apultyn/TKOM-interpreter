from src.interpreter.interpreter_objects import Value

def get_typeof(value: Value):
    try:
        return value.type_of()
    except AttributeError:
        raise AttributeError(f"Object {value.__class__.__qualname__} does not have type_of method")