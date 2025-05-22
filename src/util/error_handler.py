from .pyscript_exceptions import PyscriptException, RuntimeException


class ErrorHandler:
    def handle_error(self, exception: PyscriptException):
        if isinstance(exception, RuntimeException):
            print("=" * 31 + " Error Context " + "=" * 31)
            print(exception.context())
        print("=" * 35 + " ERROR " + "=" * 35)
        print(exception)

        quit()
