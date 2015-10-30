#   LISTA DEI PLUGIN
from plugins import plug1
from plugins import plug2
from plugins import plug1
plugin_module_list = [plug1,plug2,plug3]


def start():
    plugins={plug.setup():plug for plug in plugin_module_list}

def stop():
    for plug in plugins.values():
        plug.cleanup()
    plugins={}
    

def dispatch(plugin_name,data):
    if plugin_name in plugins:
        return plugins[plugin_name].handle(data)
    else:
        return plugin_not_found(plugin_name)
    
    
