from fastapi import HTTPException


class AuthenticationSchemeException(HTTPException):
    pass


class AuthorizationCodeException(HTTPException):
    pass


class UsernameUniquenessException(HTTPException):
    pass


class EmailUniquenessException(HTTPException):
    pass


class UserNotFoundException(HTTPException):
    pass


class PasswordMissmatchException(HTTPException):
    pass


class ExpiredTokenException(HTTPException):
    pass


class InvalidTokenException(HTTPException):
    pass


class InvalidTokenTypeException(HTTPException):
    pass


class InvalidRefreshTokenException(HTTPException):
    pass
