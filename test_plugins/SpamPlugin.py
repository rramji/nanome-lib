import nanome
from nanome.util import Logs

class SpamPlugin(nanome.PluginInstance):
    def __init__(self):
        pass
    def start(self):
        pass
    def on_workspace_received(self, workspace):
        print ("received")
    def on_run(self):
        self.request_workspace(self.on_workspace_received)
        raise Exception("nub")
    def on_advanced_settings(self):
        pass
if __name__ == "__main__":
    # Creates the server, register RemoveHydrogens as the class to instantiate, and start listening for connections
    plugin = nanome.Plugin("Remove Hydrogens", "Remove hydrogens in all selected atoms", "Simple Actions", False)
    plugin.set_plugin_class(SpamPlugin)
    plugin.run('127.0.0.1', 8888)