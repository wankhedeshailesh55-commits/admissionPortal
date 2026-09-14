from django.contrib.auth.models import Group


def user_roles(request):

    is_admission_staff = False

    if request.user.is_authenticated:
        is_admission_staff = request.user.groups.filter(
            name='Admission Staff'
        ).exists()

    return {
        'is_admission_staff': is_admission_staff
    }