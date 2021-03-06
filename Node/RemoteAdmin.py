
import requests, xml.etree.ElementTree as ET
import xmlrpclib

class RemoteAdmin:
    _server = None
    _sessionID = ""
    connected = False
    message = ""

    def __init__(self, address, port, token):
        url = 'http://%s:%s/xmlrpc/RemoteAdmin/' % (address, port);
        self._server = xmlrpclib.ServerProxy(url) #verbose=True

        result =  self._server.session.login_with_token(token)
        if result['Status'] == 'Failure':
            self.message = result['ErrorDescription']
            return

        self.connected = True
        self._sessionID = result['Value']

    def close(self):
        if not self.connected:
            return (False, "Not Connected")
        self._server.session.logout()
        return (True, "")

    def shutdown(self, regionID, delay):
        if not self.connected:
            return (False, "Not Connected")
        self._server.Region.Shutdown(self._sessionID, regionID, delay)
        return (True, "")

    def backup(self, regionName, oarFile, saveAssets):
        if not self.connected:
            return (False, "Not Connected")
        result = self._server.Region.Backup(self._sessionID, regionName, oarFile, saveAssets)
        if result['Status'] == 'Success':
            return (True, "")
        return (False, result["ErrorDescription"])

    def restore(self, regionName, oarFile, reassignUsers, skipErrors):
        if not self.connected:
            return (False, "Not Connected")
        result = self._server.Region.Restore(self._sessionID, regionName, oarFile, reassignUsers, skipErrors)
        if result['Status'] == 'Success':
            return (True, "")
        return (False, result["ErrorDescription"])

    def command(self, regionName, command):
        if not self.connected:
            return (False, "Not Connected")
        result = self._server.Console.Command(self._sessionID, command)
        if result['Status'] == 'Success':
            return (True, "")
        return (False, result["ErrorDescription"])
