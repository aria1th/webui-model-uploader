### accept file upload and save for relative paths
#pip install python-multipart for fastapi.File
import os
import shutil
from fastapi import File, UploadFile, FastAPI, Form
import gradio as gr
from pathlib import Path
from scripts.uploader import Connection
from functools import lru_cache
import json

filepath = Path(os.path.realpath(__file__))
# get parent of parent directory
basepath = filepath.parent.parent.parent.parent.absolute()

overwrite = False # if True, overwrites existing files

SELF_APP = None
# read if file_caches.json exists
if os.path.exists(os.path.join(basepath, 'file_caches.json')):
    with open(os.path.join(basepath, 'file_caches.json'), 'r') as f:
        file_caches = json.load(f)
else:
    file_caches = {}
    

@lru_cache(maxsize=40)
def get_sd_ckpt_dir() -> str:
    try:
        from modules.shared import cmd_opts
        ckpt_dir = cmd_opts.ckpt_dir
    except (ModuleNotFoundError, ImportError):
        ckpt_dir = os.path.join(basepath, 'models', 'Stable-diffusion')
    if ckpt_dir is None:
        ckpt_dir = os.path.join(basepath, 'models', 'Stable-diffusion')
    assert ckpt_dir is not None and os.path.exists(ckpt_dir), f"Could not find ckpt_dir {ckpt_dir}"
    return ckpt_dir

@lru_cache(maxsize=40)
def get_vae_ckpt_dir() -> str:
    try:
        from modules.shared import cmd_opts
        ckpt_dir = cmd_opts.vae_dir
    except (ModuleNotFoundError, ImportError):
        ckpt_dir = os.path.join(basepath, 'models', 'VAE')
    if ckpt_dir is None:
        ckpt_dir = os.path.join(basepath, 'models', 'VAE')
    assert os.path.exists(ckpt_dir), f"Could not find ckpt_dir {ckpt_dir}"
    return ckpt_dir

@lru_cache(maxsize=40)
def get_lora_ckpt_dir() -> str:
    try:
        from modules.shared import cmd_opts
        ckpt_dir = cmd_opts.lora_dir
    except (ModuleNotFoundError, ImportError):
        ckpt_dir = os.path.join(basepath, 'models', 'Lora')
    if ckpt_dir is None:
        ckpt_dir = os.path.join(basepath, 'models', 'Lora')
    assert os.path.exists(ckpt_dir), f"Could not find ckpt_dir {ckpt_dir}"
    return ckpt_dir

def register_cache(file_path:str, cache:str):
    """
    Registers a cache for a file path
    """
    file_caches[file_path] = cache
    dump_caches()
    
def dump_caches():
    """
    Dumps caches to file_caches.json
    """
    with open(os.path.join(basepath, 'file_caches.json'), 'w') as f:
        json.dump(file_caches, f)
    
def remove_cache(file_path:str):
    """
    Removes a cache for a file path
    """
    if file_path in file_caches:
        del file_caches[file_path]
        dump_caches()
        
def get_cache(file_path:str) -> str:
    """
    Gets a cache for a file path
    """
    if file_path in file_caches:
        return file_caches[file_path]
    return None

def upload_root_api(app:FastAPI):
    """
    Bind ping response to app
    """
    @app.get("/uploader/ping")
    def respond_ping():
        """
        curl http://test.api.address/uploader/ping
        """
        return {"message": "hello"}
    
def set_overwrite(overwrite_:bool):
    """
    Sets overwrite to overwrite_
    """
    global overwrite
    overwrite = overwrite_
    
def parse_response_or_dict(response_or_dict):
    """
    Parses a response or dict
    """
    if isinstance(response_or_dict, dict):
        return response_or_dict
    return response_or_dict.json()

def sync_api(app:FastAPI):
    """
    Binds sync API with app
    """
    @app.post("/sync/sd_model")
    def sync_sd_model(target_api_address:str = Form(""), model_path:str = Form(""), auth:str = Form("")):
        """
        curl -X POST -F "target_api_address=http://<target>/" -F "model_path=<model_name>" http://<this>:<port>/sync/sd_model
        """
        connection = Connection(target_api_address, auth=auth)
        try:
            return parse_response_or_dict(connection.sync_sd_model(model_path))
        except Exception as e:
            return {"message": str(e), 'success': False}
    
    @app.post("/sync/vae_model")
    def sync_vae_model(target_api_address:str = Form(""), model_path:str = Form(""), auth:str = Form("")):
        """
        curl -X POST -F "target_api_address=http://test.api.address/" -F "model_path=test/test.safetensors" http://<this>:<port>/sync/vae_model
        """
        connection = Connection(target_api_address, auth=auth)
        try:
            return parse_response_or_dict(connection.sync_vae_model(model_path))
        except Exception as e:
            return {"message": str(e), 'success': False}
        
    @app.post("/sync/lora_model")
    def sync_lora_model(target_api_address:str = Form(""), model_path:str = Form(""), auth:str = Form("")):
        """
        curl -X POST -F "target_api_address=http://test.api.address/" -F "model_path=test/test.safetensors" http://127.0.0.1:7860/sync/lora_model
        
        """
        connection = Connection(target_api_address, auth=auth)
        try:
            return parse_response_or_dict(connection.sync_lora_model(model_path))
        except Exception as e:
            return {"message": str(e), 'success': False}
        
    @app.post("/sync/all_sd_models")
    def sync_all_sd_models(target_api_address:str = Form(""), auth:str = Form("")):
        """
        curl -X POST -F "target_api_address=http://test.api.address/" http://127.0.0.1:7860/sync/all_sd_models
        """
        connection = Connection(target_api_address, auth=auth)
        try:
            connection.sync_all_sd_models()
            return {"message": "Successfully synced all sd models", 'success': True}
        except Exception as e:
            return {"message": str(e), 'success': False}
        
    @app.post("/sync/all_vae_models")
    def sync_all_vae_models(target_api_address:str = Form(""), auth:str = Form("")):
        connection = Connection(target_api_address, auth=auth)
        try:
            connection.sync_all_vae_models()
            return {"message": "Successfully synced all vae models", 'success': True}
        except Exception as e:
            return {"message": str(e), 'success': False}
        
    @app.post("/sync/all_lora_models")
    def sync_all_lora_models(target_api_address:str = Form(""), auth:str = Form("")):
        connection = Connection(target_api_address, auth=auth)
        try:
            connection.sync_all_lora_models()
            return {"message": "Successfully synced all lora models", 'success': True}
        except Exception as e:
            return {"message": str(e), 'success': False}
        
    @app.post("/sync/all_models")
    def sync_all_models(target_api_address:str = Form(""), auth:str = Form("")):
        connection = Connection(target_api_address, auth=auth)
        try:
            connection.sync_everything()
            return {"message": "Successfully synced all models", 'success': True}
        except Exception as e:
            return {"message": str(e), 'success': False}
        
def remove_cache_api(app:FastAPI):
    """
    Binds remove_cache API to app
    """
    @app.post("/remove_cache")
    def remove_cache_api(file_path:str = Form("")):
        """
        Removes the cache for file_path
        """
        remove_cache(file_path)
        if file_path in file_caches:
            return {"message": f"Successfully removed cache for {file_path}", 'success': True}
        else:
            return {"message": f"Could not find cache for {file_path}", 'success': False}
        
def upload_api(app:FastAPI):
    """
    Binds API to app
    """
    @app.post("/upload_options/overwrite")
    def set_overwrite_api(overwrite_:bool):
        """
        Sets overwrite to overwrite_
        curl -X POST -F "overwrite_=True" http://test.api.address/upload_options/overwrite
        """
        set_overwrite(overwrite_)
        return {"message": f"Set overwrite to {overwrite_}", 'value': overwrite_}
    
    @app.post("/upload")
        # test with {'file': open('images/1.png', 'rb')}
    def upload(file: UploadFile = File(...), path: str = Form('./tmp'), modeltype:str = Form("")):
        # get path
        if modeltype == "sd":
            path = os.path.join(get_sd_ckpt_dir(), path)
        elif modeltype == "vae":
            path = os.path.join(get_vae_ckpt_dir(), path)
        elif modeltype == "lora":
            path = os.path.join(get_lora_ckpt_dir(), path)
        else:
            return {"message": f"Invalid modeltype {modeltype}", 'success': False}
        real_file_path = os.path.join(path, file.filename)
        if os.path.exists(real_file_path) and not overwrite:
            return {"message": f"File {real_file_path} already exists, set overwrite to True to overwrite", 'success': False}
        elif os.path.isdir(real_file_path):
            return {"message": f"File {real_file_path} is a directory", 'success': False}
        try:
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file", 'success': False}
        finally:
            file.file.close()
        # move file to path
        try:
            os.makedirs(path, exist_ok=True)
            remove_cache(real_file_path)
            if os.path.exists(real_file_path) and overwrite:
                print(f"Removing {real_file_path} to overwrite")
                os.remove(real_file_path)
            shutil.move(file.filename, real_file_path) 
        except Exception as e:
            return {"message": f"There was an error moving the {file.filename} to {real_file_path}", 'success': False}

        return {"message": f"Successfully uploaded {file.filename} to {real_file_path}", 'success': True}

    @app.post("/upload_sd_model")
    def upload_sd_model(file:UploadFile = File(...), sd_path:str= Form("")):
        # upload file to <root>/models/Stable-diffusion/<sd_model_name>/<sd_model_name>
        # sd_model_name may be a.safetensors or /sd_path/../<model_name>
        assert '../' not in sd_path, "sd_model_name must not contain ../"
        return upload(file, os.path.join(get_sd_ckpt_dir(), sd_path), "sd")
        
    @app.post("/upload_vae_model")
    def upload_vae_model(file:UploadFile = File(...), vae_path:str = Form("")):
        # upload file to <root>/models/VAE/<vae_path>/<vae_model_name>
        assert '../' not in vae_path, "vae_path must not contain ../"
        return upload(file, os.path.join(get_vae_ckpt_dir(), vae_path), "vae")

    @app.post("/upload_lora_model")
    def upload_lora_model(file:UploadFile = File(...), lora_path:str = Form("")):
        """
        Uploads a LoRA model to <root>/models/LoRA/<lora_path>/<lora_model_name>
        """
        # upload file to <root>/models/LoRA/<lora_path>/<lora_model_name>
        # l /lora_path/<model_name>
        # assert lora_model_name does not contain ../
        assert '../' not in lora_path, "lora_path must not contain ../"
        return upload(file, os.path.join(get_lora_ckpt_dir(), lora_path), "lora")
    # can be used with curl
    #curl -X POST -F "file=@C:\\Users\\UserName\\Downloads\\test.safetensors" -F "lora_path=test" http://127.0.0.1:7860/upload_lora_model
    #curl -X POST -F "file=@C:\\Users\\UserName\\Downloads\\test.safetensors" -F "lora_path=" http://127.0.0.1:7860/upload_lora_model
    #curl -X POST -F "file=@C:\\Users\\UserName\\Downloads\\test.safetensors" http://127.0.0.1:7860/upload_lora_model
    # or with python requests
    # requests.post("<api>/upload_lora_model", files={"file": open("<path>", "rb")}, data={"lora_path": "<lora_path>"})

def fast_file_hash(file_path:str, size_to_read:int=1<<31) -> str:
    """
    Computes a hash of the file at file_path with first 1MB of file, and total file size
    """
    if file_path in file_caches and os.path.exists(file_path):
        print(f"Using cache for {file_path}")
        return get_cache(file_path)
    print(f"Computing hash for {file_path} with size_to_read {size_to_read}...")
    import hashlib
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha256 = hashlib.sha256()
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find file at {file_path}")
    filesize = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        bytes_read = 0
        while True:
            data = f.read(BUF_SIZE)
            bytes_read += BUF_SIZE
            if not data or bytes_read > size_to_read or bytes_read > filesize:
                break
            sha256.update(data)
    sha256.update(str(os.path.getsize(file_path)).encode('utf-8'))
    hashvalue = sha256.hexdigest()
    register_cache(file_path, hashvalue)
    return hashvalue
    
    

def query_api(app:FastAPI):
    """
    Binds Querying API to app
    """
    
    def walk_get_hashes(path:str, basepath:str = "", size_to_read:int=1<<31):
        """
        Walks through path and returns a dict of hashes of files in path
        Removes basepath from file paths
        """
        new_dict = {}
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path) and file.endswith(".safetensors") or file.endswith(".ckpt") or file.endswith(".pt"):
                    file_path_without_basepath = file_path.replace(basepath+'\\', "")
                    try:
                        new_dict[file_path_without_basepath] = fast_file_hash(file_path, size_to_read=size_to_read)
                    except FileNotFoundError as e:
                        new_dict[file_path_without_basepath] = ""
        return new_dict
    
    @app.post("/models/query_hash")
    def get_hash(path:str = Form(""), size_to_read:int=Form(1<<31)):
        """
        Returns the hash of the file at path.
        path may be Stable-diffusion/<model_name>
        """
        return wrap_return_hash(path, size_to_read=size_to_read)
    
    def wrap_return_hash(path:str, size_to_read:int=1<<31):
        try:
            return {"hash": fast_file_hash(path, size_to_read=size_to_read), 'success': True}
        except FileNotFoundError as e:
            return {"message": str(e),"hash":"", 'success': False}
    
    @app.post("/models/query_hash_lora")
    def get_hash_lora(path:str = Form(""), size_to_read:int=Form(1<<31)):
        """
        Returns the hash of the file at path.
        path may be <model_name> (to get LoRA/<model_name>)
        Example curl request as json:
        curl -X POST -F "path=some_path/data.safetensors" "http://127.0.0.1:7860/models/query_hash_lora"
        """
        path = os.path.join(get_lora_ckpt_dir(), path)
        return wrap_return_hash(path, size_to_read=size_to_read)
    
    @app.post("/models/query_hash_vae")
    def get_hash_vae(path:str = Form(""), size_to_read:int=Form(1<<31)):
        """
        Returns the hash of the file at path.
        path may be <model_name> (to get VAE/<model_name>)
        """
        path = os.path.join(get_vae_ckpt_dir(), path)
        return wrap_return_hash(path, size_to_read=size_to_read)
    
    @app.post("/models/query_hash_sd")
    def get_hash_sd(path:str = Form(""), size_to_read:int=Form(1<<31)):
        """
        Returns the hash of the file at path.
        path may be <model_name> (to get Stable-diffusion/<model_name>)
        curl -X POST -F "path=some_path/data.safetensors" "http://127.0.0.1:7860/models/query_hash_sd"
        """
        path = os.path.join(get_sd_ckpt_dir(), path)
        return wrap_return_hash(path, size_to_read=size_to_read)

    
    @app.post("/models/query_hash_lora_all")
    def get_hash_lora_all(path:str = Form(""), size_to_read:int=Form(1<<31)):
        """
        Returns all hashes of files in path.
        path may be some folder path
        """
        json_response = {'success' : False}
        if path is None or path == "":
            path = get_lora_ckpt_dir()
        else:
            path = os.path.join(get_lora_ckpt_dir(), path)
        if not os.path.exists(path):
            json_response['message'] = f"Path {path} does not exist"
            return json_response
        if not os.path.isdir(path):
            json_response['message'] = f"Path {path} is not a directory"
            return json_response
        # recursive
        json_response['hashes'] = walk_get_hashes(path, get_lora_ckpt_dir(), size_to_read=size_to_read)
        json_response['success'] = True
        return json_response
        
    @app.post("/models/query_hash_vae_all")
    def get_hash_vae_all(path:str = Form(""), size_to_read:int=Form(1<<31)):
        """
        Returns all hashes of files in path.
        path may be some folder path
        """
        json_response = {'success' : False}
        if path is None or path == "":
            path = get_vae_ckpt_dir()
        else:
            path = os.path.join(get_vae_ckpt_dir(), path)
        if not os.path.exists(path):
            json_response['message'] = f"Path {path} does not exist"
            return json_response
        if not os.path.isdir(path):
            json_response['message'] = f"Path {path} is not a directory"
            return json_response
        json_response['success'] = True
        json_response['hashes'] = walk_get_hashes(path, get_vae_ckpt_dir(), size_to_read=size_to_read)
        return json_response
    
    @app.post("/models/query_hash_sd_all")
    def get_hash_sd_all(path:str = Form(""), size_to_read:int=Form(1<<31)):
        """
        Returns all hashes of files in path.
        path may be some folder path
        """
        json_response = {'success' : False}
        if path is None or path == "":
            path = get_sd_ckpt_dir()
        else:
            path = os.path.join(get_sd_ckpt_dir(), path)
        if not os.path.exists(path):
            json_response['message'] = f"Path {path} does not exist"
            return json_response
        if not os.path.isdir(path):
            json_response['message'] = f"Path {path} is not a directory"
            return json_response
        json_response['success'] = True
        json_response['hashes'] = walk_get_hashes(path, get_sd_ckpt_dir(), size_to_read=size_to_read)
        return json_response
    
    @app.post("/models/query_hash_all")
    def get_hash_all(path:str = Form(""), size_to_read:int=Form(1<<31)):
        """
        Returns all hashes of files in path.
        path may be some folder path
        """
        json_response_merged = {'success' : False}
        hashes = {'lora':None, 'vae':None, 'sd':None}
        json_response_merged['hashes'] = hashes
        lora_hashes_result = get_hash_lora_all(path, size_to_read=size_to_read)
        vae_hashes_result = get_hash_vae_all(path, size_to_read=size_to_read)
        sd_hashes_result = get_hash_sd_all(path, size_to_read=size_to_read)
        hashes['lora'] = lora_hashes_result['hashes']
        hashes['vae'] = vae_hashes_result['hashes']
        hashes['sd'] = sd_hashes_result['hashes']
        json_response_merged['success'] = True
        return json_response_merged
    
    
def register_api(_:gr.Blocks, app:FastAPI):
    upload_api(app)
    query_api(app)
    upload_root_api(app)
    sync_api(app)
    remove_cache_api(app)
    SELF_APP = app
    
    
    
# only works in context of sdwebui
try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(register_api)
except:
    print("Could not bind uploader-api to app")
    pass
