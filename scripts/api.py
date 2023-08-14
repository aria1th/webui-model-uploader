### accept file upload and save for relative paths
#pip install python-multipart for fastapi.File
import os
from fastapi import File, UploadFile, FastAPI
import gradio as gr

filepath = os.path.realpath(__file__)
# get parent of parent directory
basepath = os.path.dirname(os.path.dirname(filepath))


def upload_api(_:gr.Blocks, app:FastAPI):
    """
    Binds API to app
    """
    @app.post("/upload")
        # test with {'file': open('images/1.png', 'rb')}
    def upload(file: UploadFile = File(...), path: str = '/tmp'):
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
            os.rename(file.filename, os.path.join(path, file.filename))
        except Exception:
            return {"message": "There was an error moving the file", 'success': False}

        return {"message": f"Successfully uploaded {file.filename}", 'success': True}

    @app.post("/upload_sd_model")
    def upload_sd_model(file:UploadFile = File(...), sd_model_name = 'a.safetensors'):
        # upload file to <root>/models/Stable-diffusion/<sd_model_name>
        # sd_model_name may be a.safetensors or /some_path/../<model_name>
        # assert endswith safetensors or ckpt
        assert sd_model_name.endswith('safetensors') or sd_model_name.endswith('ckpt'), "sd_model_name must end with safetensors or ckpt"
        # assert sd_model_name does not contain ../
        assert '../' not in sd_model_name, "sd_model_name must not contain ../"
        return upload(file, os.path.join(basepath, 'models', 'Stable-diffusion', sd_model_name))
        
    @app.post("/upload_vae_model")
    def upload_vae_model(file:UploadFile = File(...), vae_model_name = 'a.pt'):
        # upload file to <root>/models/VAE/<vae_model_name>
        # vae_model_name may be a.pt or /some_path/../<model_name>
        # assert endswith pt or ckpt
        assert vae_model_name.endswith('pt') or vae_model_name.endswith('ckpt'), "vae_model_name must end with pt or ckpt"
        # assert vae_model_name does not contain ../
        assert '../' not in vae_model_name, "vae_model_name must not contain ../"
        return upload(file, os.path.join(basepath, 'models', 'VAE', vae_model_name))

    @app.post("/upload_lora_model")
    def upload_lora_model(file:UploadFile = File(...), lora_model_name = 'a.safetensors'):
        # upload file to <root>/models/LoRA/<lora_model_name>
        # lora_model_name may be a.safetensors or /some_path/../<model_name>
        # assert endswith safetensors or ckpt
        assert lora_model_name.endswith('safetensors') or lora_model_name.endswith('ckpt'), "lora_model_name must end with safetensors or ckpt"
        # assert lora_model_name does not contain ../
        assert '../' not in lora_model_name, "lora_model_name must not contain ../"
        return upload(file, os.path.join(basepath, 'models', 'LoRA', lora_model_name))

# only works in context of sdwebui
try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(upload_api)
except:
    print("Could not bind controlnet_api to app")
    pass