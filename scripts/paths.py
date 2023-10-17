from functools import lru_cache
from pathlib import Path
import os

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