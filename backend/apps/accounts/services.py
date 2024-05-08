import os

import jwt
from apps.accounts.models import Account


def resolve_token(authorization):
    try:
        decoded_token = jwt.decode(
            authorization, os.environ["SECRET_KEY"], algorithms=["HS256"]
        )
        user_info = Account.objects.get(pk=decoded_token["userId"])
        return user_info
    except jwt.DecodeError as e:
        return e
