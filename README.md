## webui-model-uploader

Model uploader API attacher for Stable Diffusion Webui.

# Features:

- Upload models to the webui
- Query model hashes from the webui (Note : it is different from WebUI hash calculation)
- Delete models from the webui
- Sync models between multiple WebUI instances
- Calculates the 'tokens' that will be used by prompt (Note : if you 'schedule' the prompt, the result may be different.)
- And... download ControlNet Models from huggingface repository, because it is very frequently used in Stable Diffusion.
- And... so on?

Mostly documented in the [API documentation](<path_to_ui>/docs).
In progress.


## Overview

First, the extension provides Upload, Query, and Delete API for models.
Then with interactions between Query - Upload - Delete, we can 'sync' models between multiple WebUI instances.
But it does **not** optimizes or centralizes the models, it just provides a way to sync them. Thus there are far more space for improvement, especially in sync speed.

# Query API Endpoints and usages

There exists 2 types of queries first.
First one is for querying specific model hashes, and the other one is for querying all models(by type).

## Querying specific model hashes

The POST request basically accepts two optional arguments : path and file bytes to read.
If you don't specify the path, it will query all models in the directory. (if not single model)
File bytes are set to max 1<<31 bytes, you can specify smaller size to read smaller chunks. It may make the query faster but inaccurate.

**/models/query_hash/ POST request**
    requires : <subdirectory_path> - Exact subdirectory path of the model. for example, models/Stable-Diffusion/SubModel/a.safetensors -> Stable-Diffusion/SubModel/a.safetensors
    returns : hashvalue, success, message
    example : 
    - `curl +x POST -F "path=Stable-Diffusion/SubModel/a.safetensors" "http://localhost:7860/models/query_hash/"`

**/models/query_hash_lora POST request**
    requires : <subdirectory_path> - Exact subdirectory path of the model. for example, models/Lora/SubModel/a.safetensors -> SubModel/a.safetensors
    returns : hashvalue, success, message
    example : 
    - `curl +x POST -F "path=SubModel/a.safetensors" "http://localhost:7860/models/query_hash_lora"`

**/models/query_hash_<type> POST request**
    Follows the same format as above.
    The supported types are ['lora', 'vae', 'sd', 'embedding'].
    example : 
    - `curl +x POST -F "path=SubModel" "http://localhost:7860/models/query_hash_sd"`

**/models/query_hash_<type>_all POST request**
    Follows the same format as above, but you don't have to specify the subdirectory path. You can give 'SubModel' or nothing to let it query all models matching the type in the directory.
    The supported types are ['lora', 'vae', 'sd', 'embedding'].
    example : 
    - `curl +x POST -F "path=SubModel" "http://localhost:7860/models/query_hash_sd_all"`

**/models/query_hash_all/ POST request**
    Follows the same format as above, but you don't have to specify the subdirectory path. You can give 'Stable-Diffusion' or nothing to let it query all models in the directory.
    example : 
    - `curl +x POST -F "http://localhost:7860/models/query_hash_all/"`

## Uploading models

WIP

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
    
You should **not** contain any whitespaces in the file.