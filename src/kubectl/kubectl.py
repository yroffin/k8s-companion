
from common.singleton import Singleton
import os, logging
import json

class KubeCtl(Singleton):
    def __init__(self) -> None:
        None

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

    def listNamespaces(self):
        """
        List all namespace
        """
        result = self.exec(command = "get namespaces", outputAsJson = True)
        for namespace in result['items']:
            print(namespace['metadata']['name'])

    def scan(self):
        """
        Scan cluster
        """
        namespaces = self.exec(command = "get namespaces", outputAsJson = True)
        for namespace in namespaces['items']:
            print(namespace['metadata']['name'])
            deployments = self.exec(command = "get -n {} deployment".format(namespace['metadata']['name']), outputAsJson = True)
            for deployment in deployments['items']:
                print("deployment: {}".format(deployment['metadata']['name']))
            pods = self.exec(command = "get -n {} pod".format(namespace['metadata']['name']), outputAsJson = True)
            for pod in pods['items']:
                print("pod: {}".format(pod['metadata']['name']))

