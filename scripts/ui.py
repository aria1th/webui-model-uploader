import gradio as gr
from scripts.download_models import all_models, download_model_by_name
from scripts.paths import get_controlnet_dir
from modules import shared
from modules import script_callbacks

def download_models_each(models_selected):
    """
    Download models one by one
    """
    for model in models_selected:
        download_model_by_name(get_controlnet_dir(), model)

def create_uploader_tab():
    """
    Create the UI for the uploader tab.
    """
    with gr.Blocks() as uploader_tab:
        with gr.Tab("ControlNet Model Download"):
            # dropdown all_models
            models_selected = gr.Dropdown(
                choices=all_models,
                label="Select model(s)",
                multiselect=True,
                default=None
            )
            # button download
            download_button = gr.Button(
                text="Download",
            )
            download_button.click(
                download_models_each,
                inputs=[models_selected],
                outputs=[]
            )
    return (uploader_tab, 'Auxilary-API', 'script-auxilary-api'),

script_callbacks.on_ui_tabs(create_uploader_tab)