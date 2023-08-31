"""
    Uploads the model to the server / syncs / etc
"""
import os
import glob
from typing import List
from pathlib import Path
from logging import getLogger
import tqdm
import requests
from fastapi import FastAPI, APIRouter

try:
    import requests_toolbelt
    has_toolbelt = True
except (ImportError, ModuleNotFoundError):
    getLogger(__name__).warning("requests_toolbelt not found. Please install it with 'pip install requests_toolbelt'")
    #print("requests_toolbelt not found. Please install it with 'pip install requests_toolbelt'")
    has_toolbelt = False
#Session = requests.Session()

SELF_APP = None
try:
    from scripts.api import SELF_APP
except (ImportError, ModuleNotFoundError):
    pass

PORT = 7860
try:
    from modules.shared import cmd_opts
    PORT = cmd_opts.port
except (ImportError, ModuleNotFoundError):
    pass

filepath = Path(os.path.realpath(__file__))
# check 'extension' is in the path
if 'extension' not in str(filepath):
    basepath = filepath.absolute()
    print("WARN : You are trying to run the script as standalone mode. Some features will be disabled")
    is_stand_alone = True
else:
# get parent of parent directory
    basepath = filepath.parent.parent.parent.parent.absolute() # base webui path
    is_stand_alone = False
    
def standalone(func):
    """
    Wrapper that makes function disabled when standalone is on.
    Some functions expect relative path to 'sync' models.
    """
    def wrapper(*args, **kwargs):
        if is_stand_alone:
            return None
        return func(*args, **kwargs)
    return wrapper

#curl -X POST -F "file=@C:\\Users\\UserName\\Downloads\\test.safetensors" -F "lora_path=test" http://127.0.0.1:7860/upload_lora_model
def join_path(path1 : str, path2 : str) -> str:
    """
    Joins two paths together.
    pathA : windows_path + pathB : '/' separated path etc...
    """
    return os.path.join(path1, *path2.split('/'))

def progress_callback(monitor) -> None:
    """
    Callback for the upload progress
    """
    percentage = monitor.bytes_read / monitor.len * 100
    print("Uploaded: ", monitor.bytes_read, " of ", monitor.len, " bytes", f"{percentage:.2f}%")

class Connection:
    """
        Connects and handles the communication with the server
        standalone example:
        Connection('http://test.example.api/', "username:password").upload_lora_to('/data3/test/test.safetensors', 'test')
    """
    master_ap_address = f'http://127.0.0.1:{PORT}/'
    def __init__(self, target_ap_address: str = 'http://127.0.0.1:7860/', auth:str = "") -> None:
        """
        @param target_ap_address: address of the server
        @param auth: username:password
        """
        self.target_ap_address = target_ap_address
        # if not ends with /, add it
        if not self.target_ap_address.endswith('/'):
            self.target_ap_address += '/'
        self.session = requests.Session()
        # if not starts with http://, add it
        if not self.target_ap_address.startswith('http://') and not self.target_ap_address.startswith('https://'):
            self.target_ap_address = 'http://' + self.target_ap_address
        if auth:
            self.session.auth = auth.split(':')
            
    def create_self_request(self, accessor:str = 'models/query_hash_vae', data= None) -> requests.Response:
        """
        Post request to required path
        """
        global SELF_APP
        if SELF_APP is not None:
            assert isinstance(SELF_APP, FastAPI)
            assert isinstance(SELF_APP.router, APIRouter)
        else:
            # use master ap address
            target_address = self.master_ap_address + accessor
            return self.session.post(target_address, data=data)
        return SELF_APP.router.post(path=accessor,data=data)
    
    @staticmethod
    def create_progressbar_callback(encoder_obj):
        """
        Creates a callback for the progressbar
        @param encoder_obj: MultipartEncoder object
        """
        pbar = tqdm.tqdm(total=encoder_obj.len, unit="B", unit_scale=True)
        def callback(monitor):
            if not hasattr(monitor, 'bytes_read'):
                return
            pbar.update(monitor.bytes_read - pbar.n)
        return callback
        
    def decorate_check_connection(func):
        """
        Decorator that checks if the server is running
        """
        def wrapper(self, *args, **kwargs):
            self.check_connection()
            return func(self, *args, **kwargs)
        return wrapper
        
    def check_connection(self) -> bool:
        """
        Send GET request to "/uploader/ping" to check if server is running
        """
        url = self.target_ap_address + 'uploader/ping'
        response = self.session.get(url)
        if response.status_code == 200:
            return True
        raise Exception('Server not running')
    
    def send_data(self, file_binary: bytes,
                  model_path_arg:str = 'sd_path',
                  model_target_dir:str = 'test',
                  url:str = 'upload_sd_model',
                  file_basename:str = 'test.safetensors'
                  ) -> requests.Response:
        if has_toolbelt:
            #curl -X POST -F "file=@F:\stable-diffusion-webui\models\Lora\Sketch_Like\\SketchLike.safetensors" -F "lora_path=test" http://onomaai.ngrok.dev/upload_lora_model
            encoder = requests_toolbelt.MultipartEncoder(fields={
                'file': (file_basename, file_binary, 'application/octet-stream'),
                model_path_arg: model_target_dir
            })
            monitor = requests_toolbelt.MultipartEncoderMonitor(encoder,
                callback=self.create_progressbar_callback(encoder_obj=encoder))
            response = self.session.post(url, headers={'Content-Type': monitor.content_type}, data=monitor)
        else:
            files = {'file': (file_basename, file_binary, 'application/octet-stream')}
            response = self.session.post(url, files=files, data={model_path_arg: model_target_dir})
        return response
        
    def upload_lora_to(self, lora_path:str = 'test/test.safetensors', target_path:str = 'test') -> requests.Response:
        """
        Uploads lora from absolute path to target_path
        """
        url = self.target_ap_address + 'upload_lora_model'
        real_model_path = os.path.abspath(lora_path)
        with open(real_model_path, 'rb') as f:
            response = self.send_data(f, 'lora_path', target_path, url, file_basename=os.path.basename(real_model_path))
        return response
    
    def upload_loras_to(self, lora_paths:list = ['test/test.safetensors'], target_path:str = 'test') -> List[requests.Response]:
        """
        Uploads lora from absolute path to target_path
        """
        url = self.target_ap_address + 'upload_lora_model'
        responses = []
        for lora_path in lora_paths:
            real_model_path = os.path.abspath(lora_path)
            with open(real_model_path, 'rb') as f:
                response = self.send_data(f, 'lora_path', target_path, url, file_basename=os.path.basename(real_model_path))
                responses.append(response)
        return responses
    
    def upload_loras_glob_to(self, lora_paths:str = 'test/*.safetensors', target_path:str = 'test') -> List[requests.Response]:
        """
        Uploads lora from absolute path to target_path
        """
        url = self.target_ap_address + 'upload_lora_model'
        responses = []
        for lora_path in glob.glob(lora_paths):
            real_model_path = os.path.abspath(lora_path)
            with open(real_model_path, 'rb') as f:
                response = self.send_data(f, 'lora_path', target_path, url, file_basename=os.path.basename(real_model_path))
                responses.append(response)
        return responses
        
    @decorate_check_connection
    def upload_sd_model(self, model_path: str = 'test/test.safetensors') -> requests.Response:
        """
            Uploads the model to the server
            @param model_path: path to the model
            
        """
        from scripts.api import get_sd_ckpt_dir
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        url = self.target_ap_address + 'upload_sd_model'
        real_model_path = join_path(get_sd_ckpt_dir(), model_path)
        with open(real_model_path, 'rb') as f:
            response = self.send_data(f, 'sd_path', model_target_dir, url, file_basename=os.path.basename(real_model_path))
        return response
        
    @decorate_check_connection
    def upload_vae_model(self, model_path: str = 'test/test.safetensors') -> requests.Response:
        """
            Uploads the model to the server
        """
        from scripts.api import get_vae_ckpt_dir
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        url = self.target_ap_address + 'upload_vae_model'
        real_model_path = join_path(get_vae_ckpt_dir(), model_path)
        with open(real_model_path, 'rb') as f:
            response = self.send_data(f, 'vae_path', model_target_dir, url, file_basename=os.path.basename(real_model_path))
        return response
    
    @decorate_check_connection
    def upload_lora_model(self, model_path: str = 'test/test.safetensors') -> requests.Response:
        """
            Uploads the model to the server
        """
        from scripts.api import get_lora_ckpt_dir
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        url = self.target_ap_address + 'upload_lora_model'
        real_model_path = join_path(get_lora_ckpt_dir(), model_path)
        with open(real_model_path, 'rb') as f:
            response = self.send_data(f, 'lora_path', model_target_dir, url, file_basename=os.path.basename(real_model_path))
        return response
    
    @decorate_check_connection
    def upload_textual_inversion_model(self, model_path: str = 'test/test.pt') -> requests.Response:
        """
            Uploads the model to the server
        """
        from scripts.api import get_textual_inversion_dir
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        url = self.target_ap_address + 'upload_textual_inversion_model'
        real_model_path = join_path(get_textual_inversion_dir(), model_path)
        with open(real_model_path, 'rb') as f:
            response = self.send_data(f, 'textual_inversion_path', model_target_dir, url, file_basename=os.path.basename(real_model_path))
        return response
    
    @standalone
    @decorate_check_connection
    def sync_all_sd_models(self) -> None:
        """
            Syncs all models with the server
        """
        from scripts.api import get_sd_ckpt_dir
        for model_path in glob.glob(get_sd_ckpt_dir() + '/**/*.safetensors', recursive=True):
            self.sync_sd_model(model_path)
            
    @standalone
    @decorate_check_connection
    def sync_all_vae_models(self) -> None:
        """
            Syncs all models with the server
        """
        from scripts.api import get_vae_ckpt_dir
        for model_path in glob.glob(get_vae_ckpt_dir() + '/**/*.safetensors', recursive=True):
            self.sync_vae_model(model_path)
            
    @standalone
    @decorate_check_connection
    def sync_all_lora_models(self) -> None:
        """
            Syncs all models with the server
        """
        from scripts.api import get_lora_ckpt_dir
        for model_path in glob.glob(get_lora_ckpt_dir() + '/**/*.safetensors', recursive=True):
            self.sync_lora_model(model_path)
            
    @standalone
    @decorate_check_connection
    def sync_all_textual_inversion_models(self) -> None:
        """
            Syncs all models with the server
        """
        from scripts.api import get_textual_inversion_dir
        for model_path in glob.glob(get_textual_inversion_dir() + '/**/*.pt', recursive=True):
            self.sync_textual_inversion_model(model_path)
            
    @standalone
    @decorate_check_connection
    def sync_everything(self) -> None:
        """
            Syncs all models with the server
        """
        self.sync_all_sd_models()
        self.sync_all_vae_models()
        self.sync_all_lora_models()
        self.sync_all_textual_inversion_models()
        
    @standalone
    @decorate_check_connection
    def sync_sd_model(self, model_path: str = 'test/test.safetensors') -> requests.Response:
        """
            Syncs the model with the server
        """
        model_target_dirs = model_path.split('/')
        model_path = '/'.join(model_target_dirs)
        # query hash to self and server
        self_hash_response = self.create_self_request('models/query_hash_sd', data={'path': model_path})
        # {'hash': '1234567890'}
        self_response_json = self_hash_response.json()
        self_hash = self_response_json['hash']
        if not self_response_json['success']:
            raise Exception('Server does not have requested model')
        # server
        server_target_access = self.target_ap_address + 'models/query_hash_sd'
        server_hash_response = self.session.post(server_target_access, data={'path': model_path})
        if server_hash_response.status_code == 200:
            response_json = server_hash_response.json()
            server_hash = response_json['hash']
            success = response_json['success']
            if server_hash != self_hash or not success:
                # sync
                return self.upload_sd_model(model_path)
            return {"message": "Ther file hash matched with request", 'success': True}
        else:
            raise Exception('Server does not support Model Syncing')
            
    @standalone
    @decorate_check_connection
    def sync_vae_model(self, model_path: str = 'test/test.safetensors') -> requests.Response:
        """
            Syncs the model with the server
        """
        model_target_dirs = model_path.split('/')
        model_path = '/'.join(model_target_dirs)
        # query hash to self and server
        self_hash_response = self.create_self_request('models/query_hash_vae', data={'path': model_path})
        # {'hash': '1234567890'}
        self_response_json = self_hash_response.json()
        self_hash = self_response_json['hash']
        if not self_response_json['success']:
            raise Exception('Server does not have requested model')
        # server
        server_target_access = self.target_ap_address + 'models/query_hash_vae'
        server_hash_response = self.session.post(server_target_access, data={'path': model_path})
        if server_hash_response.status_code == 200:
            response_json = server_hash_response.json()
            server_hash = response_json['hash']
            success = response_json['success']
            if server_hash != self_hash or not success:
                # sync
                return self.upload_vae_model(model_path)
            return {"message": "Ther file hash matched with request", 'success': True}
        else:
            raise Exception('Server does not support Model Syncing')
        
    @standalone
    @decorate_check_connection
    def sync_lora_model(self, model_path: str = 'test/test.safetensors') -> requests.Response:
        """
            Syncs the model with the server
        """
        model_target_dirs = model_path.split('/')
        model_path = '/'.join(model_target_dirs)
        # query hash to self and server
        self_hash_response = self.create_self_request('models/query_hash_lora', data={'path': model_path})
        # {'hash': '1234567890'}
        self_response_json = self_hash_response.json()
        self_hash = self_response_json['hash']
        if not self_response_json['success']:
            raise Exception('Server does not have requested model')
        # server
        server_target_access = self.target_ap_address + 'models/query_hash_lora'
        server_hash_response = self.session.post(server_target_access, data={'path': model_path})
        if server_hash_response.status_code == 200:
            response_json = server_hash_response.json()
            server_hash = response_json['hash']
            success = response_json['success']
            if server_hash != self_hash or not success:
                # sync
                return self.upload_lora_model(model_path)
            return {"message": "Ther file hash matched with request", 'success': True}
        else:
            raise Exception('Server does not support Model Syncing')
    
    @standalone
    @decorate_check_connection
    def sync_textual_inversion_model(self, model_path:str = 'test/test.pt'):
        """
            Syncs the model with the server
        """
        
        model_target_dirs = model_path.split('/')
        model_path = '/'.join(model_target_dirs)
        # query hash to self and server
        self_hash_response = self.create_self_request('models/query_hash_textual_inversion', data={'path': model_path})
        # {'hash': '1234567890'}
        self_response_json = self_hash_response.json()
        self_hash = self_response_json['hash']
        if not self_response_json['success']:
            raise Exception('Server does not have requested model')
        # server
        server_target_access = self.target_ap_address + 'models/query_hash_textual_inversion'
        server_hash_response = self.session.post(server_target_access, data={'path': model_path})
        if server_hash_response.status_code == 200:
            response_json = server_hash_response.json()
            server_hash = response_json['hash']
            success = response_json['success']
            if server_hash != self_hash or not success:
                # sync
                return self.upload_textual_inversion_model(model_path)
            return {"message": "Ther file hash matched with request", 'success': True}
        else:
            raise Exception('Server does not support Model Syncing')