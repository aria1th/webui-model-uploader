import os
from secrets import compare_digest
from fastapi import HTTPException
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from scripts.paths import get_basic_auth_file

api_credentials = {}
wrapper_methods = {
    'post' : None,
    'get' : None,
    'put' : None,
    'delete' : None
} # dict of method name to wrapped method
deps = None

def secure_post(*args, **kwargs):
    """
    @app.post wrapper with dependencies
    """
    if wrapper_methods['post'] is None:
        raise Exception("init_auth not called")
    return wrapper_methods['post'](*args, **kwargs)

def secure_get(*args, **kwargs):
    """
    @app.get wrapper with dependencies
    """
    if wrapper_methods['get'] is None:
        raise Exception("init_auth not called")
    return wrapper_methods['get'](*args, **kwargs)

def secure_put(*args, **kwargs):
    """
    @app.put wrapper with dependencies. You can put this instead of @app.post
    """
    if wrapper_methods['put'] is None:
        raise Exception("init_auth not called")
    return wrapper_methods['put'](*args, **kwargs)

def secure_delete(*args, **kwargs):
    """
    @app.delete wrapper with dependencies
    """
    if wrapper_methods['delete'] is None:
        raise Exception("init_auth not called")
    return wrapper_methods['delete'](*args, **kwargs)


def init_auth(app: FastAPI):
    global deps
    global api_credentials
    deps = None
    api_credentials.clear() # clear credentials, this does not replace pointer so deps will still work
    from modules import shared
    if hasattr(shared.cmd_opts, "api_aux_auth") or os.path.isfile(get_basic_auth_file()):
        if hasattr(shared.cmd_opts, "api_aux_auth") and shared.cmd_opts.api_aux_auth:
            for cred in shared.cmd_opts.api_aux_auth.split(","):
                if ":" not in cred or cred.count(":") > 1:
                    # skip invalid credentials
                    continue
                user, password = cred.split(":")
                if user in api_credentials:
                    # skip duplicate users
                    continue
                api_credentials[user] = password
        if os.path.exists(get_basic_auth_file()): # read from file too
            with open(get_basic_auth_file(), 'r', encoding='utf-8') as f:
                file_contents = f.read()
                # split by newline and ','
                for cred in file_contents.split('\n'):
                    for cred2 in cred.split(','):
                        if ":" not in cred2 or cred2.count(":") > 1:
                            # skip invalid credentials
                            continue
                        user, password = cred2.split(":")
                        if user in api_credentials:
                            # skip duplicate users
                            continue
                        api_credentials[user] = password
    if not api_credentials and shared.cmd_opts.api_auth:
        api_credentials = {}
        for cred in shared.cmd_opts.api_auth.split(","): #duplicate code lines, fix when
            if ":" not in cred or cred.count(":") > 1:
                # skip invalid credentials
                continue
            user, password = cred.split(":")
            if user in api_credentials:
                # skip duplicate users
                continue
            api_credentials[user] = password
    def auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
        if credentials.username in api_credentials:
            if compare_digest(credentials.password, api_credentials[credentials.username]):
                return True

        raise HTTPException(
            status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Basic"}
        )
    if api_credentials:
        deps = [Depends(auth)]
        
    def wrap_app_method(app_method, deps):
        """
        Wrap app method with dependencies
        targets @app.post, @app.get, @app.put, @app.delete
        This will attach dependencies=deps to the wrapper.
        @wrapped_method(*args, **kwargs) will call app_method(*args, **kwargs, dependencies=deps)
        """
        def wrapped_method(*args, **kwargs):
            """
            Decorator for app_method
            """
            if 'dependencies' in kwargs:
                raise Exception("dependencies already set")
            return app_method(*args, **kwargs, dependencies=deps)
        return wrapped_method
        
    def wrapped_app_methods():
        returns = {} # dict of method name to wrapped method
        for method in ["post", "get", "put", "delete"]:
            returns[method] = wrap_app_method(getattr(app, method), deps)
        return returns
    global wrapper_methods
    wrapper_methods.update(wrapped_app_methods())