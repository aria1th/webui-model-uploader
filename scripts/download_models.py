### @reference : https://huggingface.co/lllyasviel/sd_control_collection
from scripts.repository_utils import SD_CONTROL_COLLECTION, CONTROLNET_V11_MODELS


additional_models = {
    'ip-adapter-plus-face_sd15.pth' : 'https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus-face_sd15.bin',
    'ip-adapter_sd15_light.pth' : 'https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15_light.bin',
    'ip-adapter-plus-face_sdxl_vit-h.pth' : 'https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus-face_sdxl_vit-h.bin',
}

all_model_dict = {**SD_CONTROL_COLLECTION, **CONTROLNET_V11_MODELS, **additional_models}

xl_model_files = {
    k:v for k,v in all_model_dict.items() if '_xl' in k or '_sdxl' in k
}
base_model_files = {
    k:v for k,v in all_model_dict.items() if '_xl' not in k and '_sdxl' not in k
}

all_models = list(all_model_dict.keys())

def download_models(path:str, models_dict:dict):
    """Download models from huggingface"""
    # runtime import
    import requests
    import os
    try:
        from tqdm import tqdm
    except (ImportError, ModuleNotFoundError):
        tqdm = lambda x: x
    for k, v in tqdm(models_dict.items()):
        # check if file exists
        if os.path.isfile(os.path.join(path, k)):
            # compare file size, when?
            print(f'File {k} exists, skipping')
            continue
        print(f'Downloading {k} at {path}')
        try:
            r = requests.get(v, allow_redirects=True)
            lock_path = os.path.join(path, k + '.lock')
            if os.path.isfile(lock_path):
                print(f'Lock file {lock_path} exists, skipping')
                continue
            with open(lock_path, 'wb') as lockfile:
                # dummy
                lockfile.write(b'')
            with open(os.path.join(path, k), 'wb') as file:
                file.write(r.content)
            print(f'Downloaded {k} at {path}')
        except Exception as err:
            print(f'Failed to download {k} at {path}')
            print(err)
        finally:
            if os.path.isfile(lock_path):
                os.remove(lock_path)
            print(f'Removed lock file {lock_path}')

def download_controlnet_xl_models(path:str):
    """
    Downloads ControlNet XL models from huggingface
    """
    download_models(path, xl_model_files)

def download_controlnet_v11_models(path:str):
    """
    Downloads ControlNet v1.1 models from huggingface
    """
    download_models(path, base_model_files)

def download_model_by_name(path:str, name:str):
    """
    Downloads a model by name from huggingface
    """
    download_models(path, match_model_name(name))
    
def match_model_name(name:str):
    """
    Matches a model name to a huggingface url
    """
    # remove ' [something]' from name
    if ' [' in name:
        name = name[:name.index(' [')]
    # match .pth or .safetensors extension
    pth_name = name + '.pth'
    safetensors_name = name + '.safetensors'
    for name_ext in [pth_name, safetensors_name, name]:
        if name_ext in all_model_dict:
            return {name_ext:all_model_dict[name_ext]}
    raise ValueError(f'Could not find model {name}')

def list_controlnet_models():
    return all_models.copy()