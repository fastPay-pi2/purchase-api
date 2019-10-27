from functools import wraps
from application.api.utils.data_formatter import format_message
from mongoengine.errors import DoesNotExist, NotUniqueError


def handle_exceptions(func):
    wraps(func)

    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except TypeError as err:
            return format_message(str(err), 400)
        except NotUniqueError as err:
            return format_message(str(err), 400)
        except IndexError as err:
            return format_message(str(err), 404)
        except DoesNotExist as err:
            return format_message(str(err), 404)
        except Exception as err:
            return format_message(str(err), 500)

    return wrapped_func
