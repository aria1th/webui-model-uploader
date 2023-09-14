
### @reference : https://huggingface.co/lllyasviel/sd_control_collection


xl_model_files = {

'diffusers_xl_canny_small.safetensors': 'https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0-small/resolve/main/diffusion_pytorch_model.bin', 'diffusers_xl_canny_mid.safetensors': 'https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0-mid/resolve/main/diffusion_pytorch_model.bin', 'diffusers_xl_canny_full.safetensors': 'https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model.bin', 'diffusers_xl_depth_small.safetensors': 'https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0-small/resolve/main/diffusion_pytorch_model.bin', 'diffusers_xl_depth_mid.safetensors': 'https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0-mid/resolve/main/diffusion_pytorch_model.bin', 'diffusers_xl_depth_full.safetensors': 'https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.bin',

'thibaud_xl_openpose.safetensors': 'https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0/resolve/main/OpenPoseXL2.safetensors',

'sargezt_xl_depth_faid_vidit.safetensors': 'https://huggingface.co/SargeZT/controlnet-sd-xl-1.0-depth-faid-vidit/resolve/main/diffusion_pytorch_model.bin', 'sargezt_xl_depth_zeed.safetensors': 'https://huggingface.co/SargeZT/controlnet-sd-xl-1.0-depth-zeed/resolve/main/diffusion_pytorch_model.bin', 'sargezt_xl_depth.safetensors': 'https://huggingface.co/SargeZT/controlnet-v1e-sdxl-depth/resolve/main/diffusion_pytorch_model.bin', 'sargezt_xl_softedge.safetensors': 'https://huggingface.co/SargeZT/controlnet-sd-xl-1.0-softedge-dexined/resolve/main/controlnet-sd-xl-1.0-softedge-dexined.safetensors',

'sai_xl_canny_128lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-canny-rank128.safetensors', 'sai_xl_canny_256lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-canny-rank256.safetensors', 'sai_xl_depth_128lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-depth-rank128.safetensors', 'sai_xl_depth_256lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-depth-rank256.safetensors', 'sai_xl_sketch_128lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-sketch-rank128-metadata.safetensors', 'sai_xl_sketch_256lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-sketch-rank256.safetensors', 'sai_xl_recolor_128lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank128/control-lora-recolor-rank128.safetensors', 'sai_xl_recolor_256lora.safetensors': 'https://huggingface.co/stabilityai/control-lora/resolve/main/control-LoRAs-rank256/control-lora-recolor-rank256.safetensors',

'ioclab_sd15_recolor.safetensors': 'https://huggingface.co/ioclab/control_v1p_sd15_brightness/resolve/main/diffusion_pytorch_model.safetensors',

't2i-adapter_xl_canny.safetensors': 'https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models_XL/adapter-xl-canny.pth', 't2i-adapter_xl_openpose.safetensors': 'https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models_XL/adapter-xl-openpose.pth', 't2i-adapter_xl_sketch.safetensors': 'https://huggingface.co/TencentARC/T2I-Adapter/resolve/main/models_XL/adapter-xl-sketch.pth',

'ip-adapter_sd15_plus.safetensors': 'https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.bin', 'ip-adapter_sd15.safetensors': 'https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15.bin', 'ip-adapter_xl.safetensors': 'https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter_sdxl.bin',

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
        print(f'Downloading {k}...')
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
    for name_ext in [pth_name, safetensors_name]:
        if name_ext in base_v11_model_names:
            return {name_ext: f'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/{name_ext}'}
        elif name_ext in xl_model_files:
            return {name_ext: xl_model_files[name_ext]}
    else:
        raise ValueError(f'No model found with name {name}')