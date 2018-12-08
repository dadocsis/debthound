"""Various helpers for auth. Mainly about tokens blacklisting

heavily inspired by https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/database_blacklist/blacklist_helpers.py
"""
from datetime import datetime
from functools import wraps

from flask import request, current_app
from sqlalchemy.orm.exc import NoResultFound

from web_api.extensions import db
from web_api.models import TokenBlacklist

from flask_jwt_extended.exceptions import (
    CSRFError, FreshTokenRequired, InvalidHeaderError, NoAuthorizationError,
    UserLoadError
)

from flask_jwt_extended.utils import decode_token
from flask_jwt_extended.view_decorators import verify_jwt_in_request

def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.

    :param identity_claim: configured key to get user identity
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]
    if not current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES'):
        expires = datetime(9999, 12, 30)
    else:
        expires = datetime.fromtimestamp(decoded_token['exp'])
    revoked = False

    db_token = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_id=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(db_token)
    db.session.commit()


def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    try:
        token = TokenBlacklist.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def revoke_token(token_jti, user):
    """Revokes the given token

    Since we use it only on logout that already require a valid access token,
    if token is not found we raise an exception
    """
    try:
        token = TokenBlacklist.query.filter_by(jti=token_jti, user_id=user).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise Exception("Could not find the token {}".format(token_jti))


def local_only(fn):
    """
    A decorator to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid access token before allowing the endpoint to be called. This
    does not check the freshness of the access token.

    See also: :func:`~flask_jwt_extended.fresh_jwt_required`
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.remote_addr != '127.0.0.1':
            return 401
        return fn(*args, **kwargs)
    return wrapper


def jwt_or_local_only(fn):
    """
    A decorator to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid access token before allowing the endpoint to be called. This
    does not check the freshness of the access token.

    See also: :func:`~flask_jwt_extended.fresh_jwt_required`
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except (CSRFError, FreshTokenRequired, InvalidHeaderError, NoAuthorizationError,
                UserLoadError) as ex:
            if request.remote_addr != '127.0.0.1':
                raise ex
        return fn(*args, **kwargs)
    return wrapper
