from functools import lru_cache
from pathlib import Path
import os
# TODO : make paths as yaml config

filepath = Path(os.path.realpath(__file__))
# get parent of parent directory
basepath = filepath.parent.parent.parent.parent.absolute()

@lru_cache(maxsize=40)
def get_sd_ckpt_dir() -> str:
    try:
        from modules.shared import cmd_opts
        ckpt_dir = cmd_opts.ckpt_dir
        print("Using ckpt_dir", ckpt_dir)
    except (ModuleNotFoundError, ImportError):
        ckpt_dir = os.path.join(basepath, 'models', 'Stable-diffusion')
    if ckpt_dir is None:
        ckpt_dir = os.path.join(basepath, 'models', 'Stable-diffusion')
    assert ckpt_dir is not None and os.path.exists(ckpt_dir) and ckpt_dir, f"Could not find ckpt_dir {ckpt_dir}"
    return ckpt_dir

@lru_cache(maxsize=40)
def get_vae_ckpt_dir() -> str:
    try:
        from modules.shared import cmd_opts
        ckpt_dir = cmd_opts.vae_dir
        print("Using vae_dir", ckpt_dir)
    except (ModuleNotFoundError, ImportError):
        ckpt_dir = os.path.join(basepath, 'models', 'VAE')
    if ckpt_dir is None:
        ckpt_dir = os.path.join(basepath, 'models', 'VAE')
    assert os.path.exists(ckpt_dir) and ckpt_dir, f"Could not find ckpt_dir {ckpt_dir}"
    return ckpt_dir

@lru_cache(maxsize=40)
def get_lora_ckpt_dir() -> str:
    try:
        from modules.shared import cmd_opts
        ckpt_dir = cmd_opts.lora_dir
        print("Using lora_dir", ckpt_dir)
    except (ModuleNotFoundError, ImportError):
        ckpt_dir = os.path.join(basepath, 'models', 'Lora')
    if ckpt_dir is None:
        ckpt_dir = os.path.join(basepath, 'models', 'Lora')
    assert os.path.exists(ckpt_dir) and ckpt_dir, f"Could not find ckpt_dir {ckpt_dir}"
    return ckpt_dir

@lru_cache(maxsize=40)
def get_textual_inversion_dir() -> str:
    try:
        from modules.shared import cmd_opts
        ckpt_dir = cmd_opts.embeddings_dir
        print("Using embeddings_dir", ckpt_dir)
    except (ModuleNotFoundError, ImportError):
        ckpt_dir = os.path.join(basepath, 'embeddings')
    if ckpt_dir is None:
        ckpt_dir = os.path.join(basepath, 'embeddings')
    assert os.path.exists(ckpt_dir), f"Could not find ckpt_dir {ckpt_dir}"
    return ckpt_dir

@lru_cache(maxsize=1)
def get_basic_auth_file() -> str:
    try:
        from modules.shared import cmd_opts
        auth_file = cmd_opts.basic_auth_file
        print("Using auth_file", auth_file)
    except (ModuleNotFoundError, ImportError):
        auth_file = os.path.join(basepath, 'auth.json')
    if auth_file is None:
        auth_file = os.path.join(basepath, 'auth.json')
    print("Using auth_file", auth_file)
    return auth_file

@lru_cache(maxsize=1)
def get_controlnet_dir() -> str:
    if os.path.exists(os.path.join(basepath, 'models', 'ControlNet')):
        return os.path.join(basepath, 'models', 'ControlNet')
    from modules.shared import opts
    cnet_models_path = opts.data.get('control_net_modules_path', None)
    if not cnet_models_path:
        extension_path = os.path.join(basepath, 'extensions')
        if not os.path.exists(extension_path):
            # vladmantic fork
            extension_path = os.path.join(basepath, 'extensions-builtin')
            if not os.path.exists(extension_path):
                print(f"Could not find extensions at {basepath}, searched 'extensions' and 'extensions-builtin'")
                return ""
        cnet_extension_path = os.path.join(extension_path, 'sd-webui-controlnet')
        if not os.path.exists(cnet_extension_path):
            print(f"Could not find controlnet extension at {cnet_extension_path}")
            return ""
        cnet_models_path = os.path.join(cnet_extension_path, 'models')
    return cnet_models_path