import bcrypt
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from core.config import settings


class UsernameAndPasswordProvider(AuthProvider):

    async def login(
            self,
            username: str,
            password: str,
            remember_me: bool,
            request: Request,
            response: Response,
    ) -> Response:
        if len(username) < 3:
            raise FormValidationError({"username": "Ensure username has at least 03 characters"})

        print(bcrypt.checkpw(password.encode(), settings.WEB_ADMIN_PASSWD.encode()))
        if username == settings.WEB_ADMIN_USERNAME and bcrypt.checkpw(password.encode(),
                                                                      settings.WEB_ADMIN_PASSWD.encode()):
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get('username', None) == settings.WEB_ADMIN_USERNAME:
            request.state.user = settings.WEB_ADMIN_USERNAME
            return True
        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        return AdminConfig(app_title='Admin page')

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user
        return AdminUser(username=user)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
