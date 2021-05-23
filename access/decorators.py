from functools import wraps
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import (user_passes_test, login_required)

from account.models import Profile

default_message = 'This is default_message by creator'


def superuser_only(function):
    """Limit view to superusers only."""

    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return _inner


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL
    actual_decorator = user_passes_test_custom(
        lambda u: u.is_anonymous(),
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test_custom(in_groups)


# How to use:
# @group_required(‘admins’, ‘seller’)


def guest_type_only(function):
    """Limit view to guests only."""

    def _inner(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        if not profile.type_user == 'guest':
            # message
            messages.warning(request, 'Вибачте, ця сторінка доступна тільки Гостям!')
            return redirect(request.META.get('HTTP_REFERER'))
        return function(request, *args, **kwargs)

    return _inner


def parent_type_only(function):
    """Limit view to parent only."""

    def _inner(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        if not profile.type_user == 'parent':
            messages.warning(request, 'Вибачте, ця сторінка доступна тільки Батькам!')
            return redirect(request.META.get('HTTP_REFERER'))
        return function(request, *args, **kwargs)

    return _inner


def student_type_only(function):
    """Limit view to student only."""

    def _inner(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        if not profile.type_user == 'student':
            messages.warning(request, 'Вибачте, ця сторінка доступна тільки Студентам!')
            return redirect(request.META.get('HTTP_REFERER'))
        return function(request, *args, **kwargs)

    return _inner


def tutor_type_only(function):
    """Limit view to tutor only."""

    def _inner(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        if not profile.type_user == 'tutor':
            messages.warning(request, 'Вибачте, ця сторінка доступна тільки Тьюторам!')
            return redirect(request.META.get('HTTP_REFERER'))
        return function(request, *args, **kwargs)

    return _inner


def head_teacher_type_only(function):
    """Limit view to head_teacher only."""

    def _inner(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        if not profile.type_user == 'head-teacher':
            messages.warning(request, 'Вибачте, ця сторінка доступна тільки Хед-тічерам!')
            return redirect(request.META.get('HTTP_REFERER'))
        return function(request, *args, **kwargs)

    return _inner


def user_passes_test_custom(function, message=default_message):
    """
    Decorator for views that checks that the user passes the given test,
    setting a message in case of no success. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not function(request.user):
                messages.error(request, message)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def login_required_message(function=None, message=default_message):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test_custom(
        lambda u: u.is_authenticated,
        message=message,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
