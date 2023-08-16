import launch
# launch is imported in context of webui
if not launch.is_installed("requests_toolbelt"):
    launch.run_pip("install requests_toolbelt", " requests_toolbelt for progress bar")

