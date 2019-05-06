import nanome
from nanome.util import Logs

class SpamPlugin(nanome.PluginInstance):
    def __init__(self):
        pass

    # When user clicks on "Activate"
    def start(self):
        Logs.debug("Connected to a new session!")
    
    # When user clicks on "Run"
    def on_run(self):
        pass
        # while(True):
            # self.request_workspace(self.on_workspace_received) # Request the entire workspace, in "deep" mode

     # When we receive the entire workspace from Nanome
    def on_workspace_received(self, workspace):
        print("received")
        # self.request_workspace(self.on_workspace_received) # Request the entire workspace, in "deep" mode
        
if __name__ == "__main__":
    # Creates the server, register RemoveHydrogens as the class to instantiate, and start listening for connections
    plugin = nanome.Plugin("Remove Hydrogens", "Remove hydrogens in all selected atoms", "Simple Actions", False)
    plugin.set_plugin_class(SpamPlugin)
    plugin.run('127.0.0.1', 8888)