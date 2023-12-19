from utils.singleton import singleton
import logging
import os
import json

@singleton
class KubectlService(object): 

    def exec(self, command = None, outputAsJson = False):
        """
        Execute kubectl with its options
        """
        _cmd = None
        if outputAsJson:
            _cmd = "kubectl {} -o json".format(command)
        else:
            _cmd = "kubectl {}".format(command)
        logging.info(_cmd)
        cmd = os.popen(_cmd)
        result = cmd.read()
        cmd.close()
        if outputAsJson:
            return json.loads(result)
        return result

    def get(self, klass):
        return self.exec(command = "get {}".format(klass), outputAsJson = True)

    def getWithName(self, klass, name):
        return self.exec(command = "get {} {}".format(klass, name), outputAsJson = True)

    def getWithNamespace(self, klass, namespace):
        return self.exec(command = "get {} -n {}".format(klass, namespace), outputAsJson = True)

    def getWithNameInNamespace(self, klass, name, namespace):
        return self.exec(command = "get {} {} -n {}".format(klass, name, namespace), outputAsJson = True)
