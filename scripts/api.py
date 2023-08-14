### accept file upload and save for relative paths
#pip install python-multipart for fastapi.File
import os
import shutil
from fastapi import File, UploadFile, FastAPI
import gradio as gr
from pathlib import Path
filepath = Path(os.path.realpath(__file__))
# get parent of parent directory
basepath = filepath.parent.parent.parent.parent.absolute()


def upload_api(_:gr.Blocks, app:FastAPI):
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
            os.makedirs(path, exist_ok=True)
            shutil.move(file.filename, path) 
        except Exception as e:
            return {"message": f"There was an error moving the {file.filename} to {path}", 'success': False}

        return {"message": f"Successfully uploaded {file.filename} to {path}", 'success': True}

    @app.post("/upload_sd_model")
    def upload_sd_model(file:UploadFile = File(...), sd_path = ''):
        # upload file to <root>/models/Stable-diffusion/<sd_model_name>/<sd_model_name>
        # sd_model_name may be a.safetensors or /sd_path/../<model_name>
        assert '../' not in sd_path, "sd_model_name must not contain ../"
        return upload(file, os.path.join(basepath, 'models', 'Stable-diffusion', sd_path))
        
    @app.post("/upload_vae_model")
    def upload_vae_model(file:UploadFile = File(...), vae_path = ''):
        # upload file to <root>/models/VAE/<vae_path>/<vae_model_name>
        assert '../' not in vae_path, "vae_path must not contain ../"
        return upload(file, os.path.join(basepath, 'models', 'VAE', vae_path))

    @app.post("/upload_lora_model")
    def upload_lora_model(file:UploadFile = File(...), lora_path:str = ''):
        # upload file to <root>/models/LoRA/<lora_path>/<lora_model_name>
        # l /lora_path/<model_name>
        # assert lora_model_name does not contain ../
        assert '../' not in lora_path, "lora_path must not contain ../"
        return upload(file, os.path.join(basepath, 'models', 'LoRA', lora_path))

# only works in context of sdwebui
try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(upload_api)
except:
    print("Could not bind controlnet_api to app")
    pass