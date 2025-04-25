from pyscript_exceptions import PyscriptException


class ErrorHandler:
    def handle_error(self, exception: PyscriptException):
        print(exception)
