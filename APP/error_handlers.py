from django.shortcuts import render


def error_400(request, exception=None):

    context = {
        'error_code': 400,
        'error_title': 'Bad Request',
        'error_message': 'The request could not be processed.'
    }

    return render(
        request,
        'error.html',
        context,
        status=400
    )


def error_403(request, exception=None):

    context = {
        'error_code': 403,
        'error_title': 'Access Denied',
        'error_message': 'You do not have permission to access this page.'
    }

    return render(
        request,
        'error.html',
        context,
        status=403
    )


def error_404(request, exception=None):

    if request.path.startswith('/admission/view/'):
        message = 'The requested student record could not be found.'

    elif request.path.startswith('/admission/edit/'):
        message = 'The student record you are trying to edit could not be found.'

    elif request.path.startswith('/admission/delete/'):
        message = 'The student record you are trying to delete could not be found.'

    else:
        message = 'The page you are looking for does not exist or may have been moved.'

    context = {
        'error_code': 404,
        'error_title': 'Page Not Found',
        'error_message': message
    }

    return render(
        request,
        'error.html',
        context,
        status=404
    )


def error_500(request):

    context = {
        'error_code': 500,
        'error_title': 'Server Error',
        'error_message': 'Something went wrong on our server. Please try again later.'
    }

    return render(
        request,
        'error.html',
        context,
        status=500
    )