from config import AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE
import json
from functools import wraps
from urllib.request import urlopen
from flask import request
from jose import jwt


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    This function extract the authorization part from the header
    in case if exist, if not a proper error will be raised!
    """
    headers = request.headers
    if 'Authorization' not in headers:
        raise AuthError({
            'success': False,
            'code': 'invalid_claims',
            'description': 'Authorization key is not found!'
        }, 401)
    auth_header = headers["Authorization"]
    auth_parts = auth_header.split(' ')
    if len(auth_parts) != 2:
        raise AuthError({
            'success': False,
            'code': 'invalid_claims',
            'description': 'token is not found!'
        }, 401)
    if auth_parts[0].lower() != "bearer":
        raise AuthError({
            'success': False,
            'code': 'invalid_claims',
            'description': 'bearer keyword is not found!'
        }, 401)

    return auth_parts[1]


def check_permissions(permission, payload):
    """
    check if the user has the right permission to
    access the resource or not, it checks first if
    permission part exist in the payload, if not error will
    be raised!
    """
    if "permissions" not in payload:
        raise AuthError({
            'success': False,
            'code': 'invalid_claims',
            'description': 'permissions are not providded!'
        }, 401)
    if permission not in payload['permissions']:
        raise AuthError({
            'success': False,
            'code': 'invalid_claims',
            'description': 'method not allowed'
        }, 401)
    return True


def verify_decode_jwt(token):
    """
    this function is used to verfiy if the token is
    valid or not
    """
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
