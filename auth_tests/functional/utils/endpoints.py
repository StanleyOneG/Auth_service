from enum import Enum


class Endpoints(Enum):
    
    TestHelloWorld = "/hello"
    UserSignUp = '/api/v1/user/register'
    UserLogIn = '/api/v1/user/login'
    Refresh = '/api/v1/user/refresh'
    UserLogOut = '/api/v1/user/logout'
    ShowUserLogInHistory = '/api/v1/user/show_login_history'
    ChangeUserCredentials = '/api/v1/user/change_credentials'
    CreatePermission = '/api/v1/permission/create_permission'
    DeletePermission = '/api/v1/permission/delete_permission'
    SetUserPermission = '/api/v1/user/set_permission'
    ChangePermission = '/api/v1/permission/change_permission'
    ShowUserPermissions = '/api/v1/user/show_user_permissions'
    ShowPermissions = '/api/v1/permission/show_permissions'
    DeleteUserPermission = '/api/v1/user/delete_user_permission'
