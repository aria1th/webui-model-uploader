
### @reference : https://huggingface.co/lllyasviel/sd_control_collection


additional_models = {

    'diffusers_xl_canny_small.safetensors': 'https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0-small/resolve/main/diffusion_pytorch_model.bin', 
    'diffusers_xl_canny_mid.safetensors': 'https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0-mid/resolve/main/diffusion_pytorch_model.bin',
    'diffusers_xl_canny_full.safetensors': 'https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model.bin', 
    'diffusers_xl_depth_small.safetensors': 'https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0-small/resolve/main/diffusion_pytorch_model.bin', 
    'diffusers_xl_depth_mid.safetensors': 'https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0-mid/resolve/main/diffusion_pytorch_model.bin', 
    'diffusers_xl_depth_full.safetensors': 'https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.bin',
    'thibaud_xl_openpose.safetensors': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/thibaud_xl_openpose.safetensors',
    'sargezt_xl_depth_faid_vidit.safetensors': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/sargezt_xl_depth_faid_vidit.safetensors', 
    'sargezt_xl_depth_zeed.safetensors': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/sargezt_xl_depth_zeed.safetensors',
    'sargezt_xl_depth.safetensors': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/sargezt_xl_depth.safetensors', 
    'sargezt_xl_softedge.safetensors': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/sargezt_xl_softedge.safetensors' ,
    'sai_xl_canny_128lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-canny-rank128.safetensors',
    'sai_xl_canny_256lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-canny-rank256.safetensors',
    'sai_xl_depth_128lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-depth-rank128.safetensors', 
    'sai_xl_depth_256lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-depth-rank256.safetensors', 
    'sai_xl_sketch_128lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-sketch-rank128-metadata.safetensors', 
    'sai_xl_sketch_256lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-sketch-rank256.safetensors', 
    'sai_xl_recolor_128lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-recolor-rank128.safetensors', 
    'sai_xl_recolor_256lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-recolor-rank256.safetensors',
    'ioclab_sd15_recolor.safetensors': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/ioclab_sd15_recolor.safetensors',
    't2i-adapter_xl_canny.safetensors': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_xl_canny.safetensors', 
    't2i-adapter_xl_openpose.safetensors': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_xl_openpose.safetensors', 
    't2i-adapter_xl_sketch.safetensors': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/t2i-adapter_xl_sketch.safetensors',
    'ip-adapter_sd15_plus.pth': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/ip-adapter_sd15_plus.pth', 
    'ip-adapter_sd15.pth': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/ip-adapter_sd15.pth', 
    'ip-adapter_xl.pth': 'https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/ip-adapter_xl.pth',
    'ip-adapter-plus-face_sd15.pth' : 'https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus-face_sd15.bin',
    'ip-adapter_sd15_light.pth' : 'https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15_light.bin'
}
# fix ext
copy_dict = additional_models.copy()
additional_models.clear()
for k, v in copy_dict.items():
    if '.pth' in v and '.safetensors' in k:
        #replace .safetenors with .pth
        additional_models[k.replace('.safetensors', '.pth')] = v
    elif '.bin' in v and '.safetensors' in k:
        #replace .safetenors with .pth
        # bin is not natively supported by torch.load
        additional_models[k.replace('.safetensors', '.pth')] = v
    else:
        additional_models[k] = v

xl_model_files = {
    k: v for k, v in additional_models.items() if '_xl' in k or '_sdxl' in k
}
base_v11_model_names = {'control_v11e_sd15_ip2p.pth',
 'control_v11e_sd15_ip2p.yaml',
 'control_v11e_sd15_shuffle.pth',
 'control_v11e_sd15_shuffle.yaml',
 'control_v11f1e_sd15_tile.pth',
 'control_v11f1e_sd15_tile.yaml',
 'control_v11f1p_sd15_depth.pth',
 'control_v11f1p_sd15_depth.yaml',
 'control_v11p_sd15_canny.pth',
 'control_v11p_sd15_canny.yaml',
 'control_v11p_sd15_inpaint.pth',
 'control_v11p_sd15_inpaint.yaml',
 'control_v11p_sd15_lineart.pth',
 'control_v11p_sd15_lineart.yaml',
 'control_v11p_sd15_mlsd.pth',
 'control_v11p_sd15_mlsd.yaml',
 'control_v11p_sd15_normalbae.pth',
 'control_v11p_sd15_normalbae.yaml',
 'control_v11p_sd15_openpose.pth',
 'control_v11p_sd15_openpose.yaml',
 'control_v11p_sd15_scribble.pth',
 'control_v11p_sd15_scribble.yaml',
 'control_v11p_sd15_seg.pth',
 'control_v11p_sd15_seg.yaml',
 'control_v11p_sd15_softedge.pth',
 'control_v11p_sd15_softedge.yaml',
 'control_v11p_sd15s2_lineart_anime.pth',
 'control_v11p_sd15s2_lineart_anime.yaml',
 'control_v11u_sd15_tile.pth'}


base_model_files = {
    name: f'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/{name}' for name in base_v11_model_names
}

def download_models(path:str, models_dict:dict):
    """Download models from huggingface"""
    # runtime import
    import requests
    import os
    for k, v in models_dict.items():
        # check if file exists
        if os.path.isfile(os.path.join(path, k)):
            # compare file size
            continue
        print(f'Downloading {k}... at {path}')
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
    # match non-xl models
    for name, url in additional_models.items():
        if '_xl' not in name and '_sdxl' not in name:
            download_models(path, {name: url})

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
    for name_ext in [pth_name, safetensors_name]:
        if name_ext in base_v11_model_names:
            return {name_ext: f'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/{name_ext}'}
        elif name_ext in xl_model_files:
            return {name_ext: xl_model_files[name_ext]}
        elif name_ext in additional_models:
            return {name_ext: additional_models[name_ext]}
    else:
        raise ValueError(f'No model found with name {name}')