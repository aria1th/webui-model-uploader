
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
    import requests
    import os
    for k, v in models_dict.items():
        # check if file exists
        if os.path.isfile(os.path.join(path, k)):
            # compare file size
            continue
        print(f'Downloading {k}...')
        r = requests.get(v, allow_redirects=True)
        with open(os.path.join(path, k), 'wb') as f:
            f.write(r.content)
        print(f'Downloaded {k} at {path}')
    
    
def download_controlnet_xl_models(path:str):
    download_models(path, xl_model_files)
        
def download_controlnet_v11_models(path:str):
    download_models(path, base_model_files)