from application.api.utils.data_formatter import format_message
from mongoengine.errors import DoesNotExist, NotUniqueError
from functools import wraps


# TODO all methods should return msg, status and
# the format message method should be called here
def handle_exceptions(func):
    wraps(func)

    def wrapped_func(*args, **kwargs):
        try:
            response, status = func(*args, **kwargs)
            return format_message(response, status)
        except TypeError as err:
            return format_message(str(err), 400)
        except NotUniqueError as err:
            return format_message(str(err), 400)
        except IndexError as err:
            return format_message(str(err), 404)
        except DoesNotExist as err:
            return format_message(str(err), 404)
        except Exception as err:
            return format_message(str(err), 400)

    return wrapped_func
