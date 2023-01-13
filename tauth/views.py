import re

from django.conf import settings
from django.contrib import auth, messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from authlib.google import GoogleOAuth2Client
from authlib.views import retrieve_next, set_next_cookie

from tauth.utils import validate_user_access


ADMIN_OAUTH_PATTERNS = settings.ADMIN_OAUTH_PATTERNS
ADMIN_OAUTH_LOGIN_HINT = "admin-oauth-login-hint"


@never_cache
@set_next_cookie
def admin_oauth(request):
    client = GoogleOAuth2Client(
        request, login_hint=request.COOKIES.get(ADMIN_OAUTH_LOGIN_HINT) or ""
    )

    if all(key not in request.GET for key in ("code", "oauth_token")):
        return redirect(client.get_authentication_url())

    try:
        user_data = client.get_user_data()
    except Exception as exc:
        messages.error(request, exc)
        messages.error(request, _("Error while fetching user data. Please try again."))
        return redirect("admin:login")

    email = user_data.get("email")
    if email:
        for pattern, user_mail in ADMIN_OAUTH_PATTERNS:
            match = re.search(pattern, email)
            if match:
                if callable(user_mail):
                    user_mail = user_mail(match)
                User = auth.get_user_model()
                user = User.objects.filter(email=user_mail).first()
                if user is None:
                    User.objects.create(email=user_mail, username=user_mail, is_superuser=True, is_staff=True, is_active=True)

                if not validate_user_access(user_mail):
                    messages.error(request, _("You don't have access to view this page."))
                    response = redirect("admin:login")
                    response.delete_cookie(ADMIN_OAUTH_LOGIN_HINT)
                    return response

                user = auth.authenticate(email=user_mail)
                if user and user.is_staff:
                    auth.login(request, user)
                    response = redirect(retrieve_next(request) or "admin:index")
                    response.set_cookie(
                        ADMIN_OAUTH_LOGIN_HINT, email, expires=30 * 86400
                    )
                    return response

        messages.error(
            request, _("No matching staff users for email address '%s'") % email
        )
    else:
        messages.error(request, _("Could not determine your email address."))
    response = redirect("admin:login")
    response.delete_cookie(ADMIN_OAUTH_LOGIN_HINT)
    return response
