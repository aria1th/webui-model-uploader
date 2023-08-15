import os
import shutil
import glob
from pathlib import Path
import requests
#Session = requests.Session()


filepath = Path(os.path.realpath(__file__))
# get parent of parent directory
basepath = filepath.parent.parent.parent.absolute() # base webui path

SD_MODEL_PATH = os.path.join(basepath, 'models', 'Stable-diffusion')
VAE_PATH = os.path.join(basepath, 'models', 'VAE')
LORA_PATH = os.path.join(basepath, 'models', 'Lora')

#curl -X POST -F "file=@C:\\Users\\UserName\\Downloads\\test.safetensors" -F "lora_path=test" http://127.0.0.1:7860/upload_lora_model

class Connection:
    master_ap_address = '127.0.0.1:7860/'
    """
        Connects and handles the communication with the server
    """
    def __init__(self, target_ap_address: str = '127.0.0.1:7860/') -> None:
        self.target_ap_address = target_ap_address
        # if not ends with /, add it
        if not self.target_ap_address.endswith('/'):
            self.target_ap_address += '/'
        self.session = requests.Session()
        
    def decorate_check_connection(func):
        def wrapper(self, *args, **kwargs):
            self.check_connection()
            return func(self, *args, **kwargs)
        return wrapper
        
    def check_connection(self) -> bool:
        """
        Send GET request to "/uploader/ping" to check if server is running
        """
        url = 'http://' + self.target_ap_address + 'uploader/ping'
        response = self.session.get(url)
        if response.status_code == 200:
            return True
        raise Exception('Server not running')
        
    @decorate_check_connection
    def upload_sd_model(self, model_path: str = 'test/test.safetensors') -> None:
        """
            Uploads the model to the server
        """
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        url = 'http://' + self.target_ap_address + 'upload_sd_model'
        files = {'file': open(model_path, 'rb')}
        response = self.session.post(url, files=files, data={'sd_path': model_target_dir})
        print(response.text)
        
    @decorate_check_connection
    def upload_vae_model(self, model_path: str = 'test/test.safetensors') -> None:
        """
            Uploads the model to the server
        """
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        url = 'http://' + self.target_ap_address + 'upload_vae_model'
        files = {'file': open(model_path, 'rb')}
        response = self.session.post(url, files=files, data={'vae_path': model_target_dir})
        print(response.text)
    
    @decorate_check_connection
    def upload_lora_model(self, model_path: str = 'test/test.safetensors') -> None:
        """
            Uploads the model to the server
        """
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        url = 'http://' + self.target_ap_address + 'upload_lora_model'
        files = {'file': open(model_path, 'rb')}
        response = self.session.post(url, files=files, data={'lora_path': model_target_dir})
        print(response.text)
        
    @decorate_check_connection
    def sync_sd_model(self, model_path: str = 'test/test.safetensors') -> None:
        """
            Syncs the model with the server
        """
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        # query hash to self and server
        self_target_access = self.master_ap_address + 'models/query_hash_sd'
        self_hash_response = self.session.post(self_target_access, data={'path': model_target_dir})
        # {'hash': '1234567890'}
        self_hash = self_hash_response.json()['hash']
        # server
        server_target_access = 'http://' + self.target_ap_address + 'models/query_hash_sd'
        server_hash_response = self.session.post(server_target_access, data={'path': model_target_dir})
        if server_hash_response.status_code == 200:
            server_hash = server_hash_response.json()['hash']
            if server_hash != self_hash:
                # sync
                self.upload_sd_model(model_path)
        else:
            # upload
            self.upload_sd_model(model_path)
            
    @decorate_check_connection
    def sync_vae_model(self, model_path: str = 'test/test.safetensors') -> None:
        """
            Syncs the model with the server
        """
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        # query hash to self and server
        self_target_access = self.master_ap_address + 'models/query_hash_vae'
        self_hash_response = self.session.post(self_target_access, data={'path': model_target_dir})
        # {'hash': '1234567890'}
        self_hash = self_hash_response.json()['hash']
        # server
        server_target_access = 'http://' + self.target_ap_address + 'models/query_hash_vae'
        server_hash_response = self.session.post(server_target_access, data={'path': model_target_dir})
        if server_hash_response.status_code == 200:
            server_hash = server_hash_response.json()['hash']
            if server_hash != self_hash:
                # sync
                self.upload_vae_model(model_path)
        else:
            # upload
            self.upload_vae_model(model_path)
    
    @decorate_check_connection
    def sync_lora_model(self, model_path: str = 'test/test.safetensors') -> None:
        """
            Syncs the model with the server
        """
        model_target_dirs = model_path.split('/')[:-1]
        model_target_dir = '/'.join(model_target_dirs)
        # query hash to self and server
        self_target_access = self.master_ap_address + 'models/query_hash_lora'
        self_hash_response = self.session.post(self_target_access, data={'path': model_target_dir})
        # {'hash': '1234567890'}
        self_hash = self_hash_response.json()['hash']
        # server
        server_target_access = 'http://' + self.target_ap_address + 'models/query_hash_lora'
        server_hash_response = self.session.post(server_target_access, data={'path': model_target_dir})
        if server_hash_response.status_code == 200:
            server_hash = server_hash_response.json()['hash']
            if server_hash != self_hash:
                # sync
                self.upload_lora_model(model_path)
        else:
            # upload
            self.upload_lora_model(model_path)
    
    