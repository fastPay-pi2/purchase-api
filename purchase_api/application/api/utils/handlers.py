from application.api.utils.data_formatter import format_message
from mongoengine.errors import DoesNotExist, NotUniqueError


def handle_exceptions(method, success_message, *args):
    try:
        if method:
            method(*args)
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
    else:
        return format_message(success_message, 200)
