import nanome
from timeit import default_timer as timer
import os
import sys, inspect
import test_plugins
import sys
import subprocess

def runplugin (plugin_class):
    plugin = nanome.Plugin("✏Testing Plugin", "Plugin is being run using the tester plugin.", "Test", True)
    plugin.set_plugin_class(plugin_class)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    class_name = str(sys.argv[1])
    pluginNum = int(sys.argv[2])
    if (pluginNum > 0):
        subprocess.Popen(["python", sys.argv[0], class_name, str(pluginNum-1)])
        del sys.argv[2]
        del sys.argv[1]
    else:
        exit()
    module_name = "test_plugins." + class_name
    if module_name not in sys.modules:
        raise Exception("No module: " + module_name)
    clsmembers = inspect.getmembers(sys.modules[module_name], inspect.isclass)
    plugin_class = None
    for clsmember in clsmembers:
        if (clsmember[0] == class_name):
            plugin_class = clsmember[1]
            break
    if plugin_class == None:
        raise "No class " + class_name + " in module " + module_name
    runplugin(plugin_class)