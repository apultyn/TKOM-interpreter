def get(interpreter, name: str):
    return interpreter.global_env.get(name)
