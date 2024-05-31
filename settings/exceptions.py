from fastapi import HTTPException, status


class BadUserCredsException(BaseException):
    pass


signature_doesnt_match_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are probably trying to authenticate the second time "
                   "or you are using an old link or you are already "
                   "authenticated. If you think your "
                   "session was accidentally deleted or expired, just "
                   "generate a new link using /auth command and try again.",
            headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
)

relogin_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your credentials expired. Please login again.",
            headers={"WWW-Authenticate": "Bearer"},
)

access_token_invalid_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired. Create new token with /refresh",
            headers={"WWW-Authenticate": "Bearer"},
)


wrong_username_or_password = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
)


def entity_doesnt_exist(name: str, value: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"{name} {value} doesn't exist",
        headers={"WWW-Authenticate": "Bearer"},
    )


too_many_requests = HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
            headers={"WWW-Authenticate": "Bearer"},
)
