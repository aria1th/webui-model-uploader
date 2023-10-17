# webui-model-uploader

Model uploader API attacher for Stable Diffusion Webui.

Features:

    Mostly documented in the [API documentation](<path_to_ui>/docs).
    In progress.

## Command Line Arguments

    --api-auth master:user
        The extension basically uses same auth from webui too, but for safety, you can specify a different one with following options:
    --api-aux-auth someuser:password
        This will prevent api-auth for being used for the aux API, and instead use this one.
    --basic-auth-file F:/stable-diffusion-webui/basic_auth.txt
        This will use the specified file for auxilary api auth. The file can contain multiple lines or single lines separated by commas and newlines. The username and password are separated by a colon. Example:
        ```
        user1:password1,userx:passwordx
        user2:password2
        ```
        You should not contain any whitespaces in the file.