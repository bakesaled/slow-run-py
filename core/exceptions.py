from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
  response = exception_handler(exc, context)
  handlers = {
      'ProfileDoesNotExist': _handle_generic_error,
      'ValidationError': _handle_generic_error,
      'NotAuthenticated': _handle_generic_error_with_detail,
      'Unauthorized': _handle_generic_error_with_detail,
  }

  exception_class = exc.__class__.__name__

  if exception_class in handlers:
    return handlers[exception_class](exc, context, response)

  return response


def _handle_generic_error(exc, context, response):
  response.data = {
      'errors': response.data
  }

  return response


def _handle_generic_error_with_detail(exc, context, response):
  response.data = {
      'errors': {
          'error': response.data['detail']
      }
  }

  return response
