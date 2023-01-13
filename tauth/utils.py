import requests

from django.conf import settings


def validate_user_access(email):
    url = f'{settings.ADMIN_AUTH_API_URL}/api/v1/sso-users/{email}/services/'
    try:
        response = requests.get(url)
        allowed_services = response.json()

        for service in allowed_services:
            if service['name'] == settings.APP_NAME:
                return True
    except:
        return False

    return False
