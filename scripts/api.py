### accept file upload and save for relative paths
#pip install python-multipart for fastapi.File
import os
import shutil
from fastapi import File, UploadFile, FastAPI, Form
import gradio as gr
from pathlib import Path

filepath = Path(os.path.realpath(__file__))
# get parent of parent directory
basepath = filepath.parent.parent.parent.parent.absolute()

overwrite = False # if True, overwrites existing files

file_caches = {}

def register_cache(file_path:str, cache:str):
    """
    Registers a cache for a file path
    """
    file_caches[file_path] = cache
    
def remove_cache(file_path:str):
    """
    Removes a cache for a file path
    """
    if file_path in file_caches:
        del file_caches[file_path]
        
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
        return {"message": "hello"}

def upload_api(app:FastAPI):
    """
    Binds API to app
    """
    @app.post("/upload")
        # test with {'file': open('images/1.png', 'rb')}
    def upload(file: UploadFile = File(...), path: str = './tmp'):
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
            if os.path.exists(path) and not overwrite:
                return {"message": f"File {path} already exists, set overwrite to True to overwrite", 'success': False}
            os.makedirs(path, exist_ok=True)
            remove_cache(path)
            if os.path.exists(path) and overwrite:
                print(f"Removing {path} to overwrite")
                os.remove(path)
            shutil.move(file.filename, path) 
        except Exception as e:
            return {"message": f"There was an error moving the {file.filename} to {path}", 'success': False}

        return {"message": f"Successfully uploaded {file.filename} to {path}", 'success': True}

    @app.post("/upload_sd_model")
    def upload_sd_model(file:UploadFile = File(...), sd_path:str= Form("")):
        # upload file to <root>/models/Stable-diffusion/<sd_model_name>/<sd_model_name>
        # sd_model_name may be a.safetensors or /sd_path/../<model_name>
        assert '../' not in sd_path, "sd_model_name must not contain ../"
        return upload(file, os.path.join(basepath, 'models', 'Stable-diffusion', sd_path))
        
    @app.post("/upload_vae_model")
    def upload_vae_model(file:UploadFile = File(...), vae_path:str = Form("")):
        # upload file to <root>/models/VAE/<vae_path>/<vae_model_name>
        assert '../' not in vae_path, "vae_path must not contain ../"
        return upload(file, os.path.join(basepath, 'models', 'VAE', vae_path))

    @app.post("/upload_lora_model")
    def upload_lora_model(file:UploadFile = File(...), lora_path:str = Form("")):
        """
        Uploads a LoRA model to <root>/models/LoRA/<lora_path>/<lora_model_name>
        """
        # upload file to <root>/models/LoRA/<lora_path>/<lora_model_name>
        # l /lora_path/<model_name>
        # assert lora_model_name does not contain ../
        assert '../' not in lora_path, "lora_path must not contain ../"
        return upload(file, os.path.join(basepath, 'models', 'Lora', lora_path))
    # can be used with curl
    #curl -X POST -F "file=@C:\\Users\\UserName\\Downloads\\test.safetensors" -F "lora_path=test" http://127.0.0.1:7860/upload_lora_model
    #curl -X POST -F "file=@C:\\Users\\UserName\\Downloads\\test.safetensors" -F "lora_path=" http://127.0.0.1:7860/upload_lora_model
    #curl -X POST -F "file=@C:\\Users\\UserName\\Downloads\\test.safetensors" http://127.0.0.1:7860/upload_lora_model
    # or with python requests
    # requests.post("<api>/upload_lora_model", files={"file": open("<path>", "rb")}, data={"lora_path": "<lora_path>"})

def fast_file_hash(file_path:str) -> str:
    """
    Computes a hash of the file at file_path with first 1MB of file, and total file size
    """
    if file_path in file_caches:
        return get_cache(file_path)
    import hashlib
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha256 = hashlib.sha256()
    model_path = os.path.join(basepath, 'models')
    real_file_path = os.path.join(model_path, file_path)
    if not os.path.exists(real_file_path):
        raise FileNotFoundError(f"Could not find file at {real_file_path}")
    with open(real_file_path, 'rb') as f:
        bytes_read = 0
        while True:
            data = f.read(BUF_SIZE)
            bytes_read += BUF_SIZE
            if not data or bytes_read > 1000000:
                break
            sha256.update(data)
    sha256.update(str(os.path.getsize(real_file_path)).encode('utf-8'))
    hashvalue = sha256.hexdigest()
    register_cache(file_path, hashvalue)
    return hashvalue

def query_api(app:FastAPI):
    """
    Binds Querying API to app
    """
    @app.post("/models/query_hash")
    def get_hash(path:str):
        """
        Returns the hash of the file at path.
        path may be Stable-diffusion/<model_name>
        """
        return {"hash": fast_file_hash(path)}
    
    @app.post("/models/query_hash_lora")
    def get_hash_lora(path:str):
        """
        Returns the hash of the file at path.
        path may be <model_name> (to get LoRA/<model_name>)
        """
        path = os.path.join('Lora', path)
        return {"hash": fast_file_hash(path)}
    
    @app.post("/models/query_hash_vae")
    def get_hash_vae(path:str):
        """
        Returns the hash of the file at path.
        path may be <model_name> (to get VAE/<model_name>)
        """
        path = os.path.join('VAE', path)
        return {"hash": fast_file_hash(path)}
    
    @app.post("/models/query_hash_sd")
    def get_hash_sd(path:str):
        """
        Returns the hash of the file at path.
        path may be <model_name> (to get Stable-diffusion/<model_name>)
        """
        path = os.path.join('Stable-diffusion', path)
        return {"hash": fast_file_hash(path)}
    
    
def register_api(_:gr.Blocks, app:FastAPI):
    upload_api(app)
    query_api(app)
    upload_root_api(app)
    
    
    
# only works in context of sdwebui
try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(register_api)
except:
    print("Could not bind controlnet_api to app")
    pass