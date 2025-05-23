from .pyscript_exceptions import PyscriptException, RuntimeException


class ErrorHandler:
    def handle_error(self, exception: PyscriptException):
        if isinstance(exception, RuntimeException):
            print("=" * 31 + " Error Context " + "=" * 31)
            context = exception.context()
            if context.count("\n") > 21:
                context_list = context.split("\n")
                context = (
                    "\n".join(context_list[:10])
                    + f"\n...{len(context_list) - 20} frames omitted...\n"
                    + "\n".join(context_list[-10:])
                )
            print(context)
        print("=" * 35 + " ERROR " + "=" * 35)
        print(exception)

        quit()
