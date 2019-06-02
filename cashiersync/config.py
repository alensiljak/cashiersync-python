'''
Store configuration in YAML format,
in user's configuration directory.
'''


class Configuration:
    def __init__(self):
        self.configFileName = "config.yaml"
        self.appName = "cashiersync"
        self.createConfigFile()
        self.readConfig()

    def readConfig(self):
        ''' Read configuration file '''
        import yaml

        path = self.configPath
        with open(path, 'r') as stream:
            try:
                print(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)

    def createConfigFile(self):
        ''' create the config file if it does not exist '''
        import os
        # Create the config folder
        dir = self.configDir
        if not os.path.exists(dir) and not os.path.isdir(dir):
            os.makedirs(dir)
        # Create file
        path = self.configPath
        if os.path.exists(path):
            return

        with open(path, "w") as config_file:
            config_file.write("")

    @property
    def configDir(self):
        from xdg.BaseDirectory import xdg_config_home
        from os.path import sep

        return xdg_config_home + sep + self.appName

    @property
    def configPath(self):
        ''' assembles the path to the config file '''
        from os.path import sep

        return self.configDir + sep + self.configFileName
