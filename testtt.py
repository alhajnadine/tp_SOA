import logging
logging.basicConfig(level=logging.DEBUG)
import sys 
from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from spyne.util.wsgi_wrapper import run_twisted
from zeep.client import Client

class FileWatcherService(ServiceBase):
    @rpc(Unicode, _returns=Integer)
    def notify_file_created(ctx, file_path):
        return 0
 

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Cette méthode est appelée lorsque qu'un fichier est créé dans le répertoire surveillé
        print("Un fichier a été ajouté : " + event.src_path)
        # Invoquez l'opération SOAP pour notifier la création du fichier

def start_file_watcher():
    print("Écoute en cours...")
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path="C:\\Users\\alhaj\\Desktop\\Master2\\Web services\\Projet\\soa", recursive=False)
    observer.start()

    observer.join()

if __name__ == "__main__":
    application = Application([FileWatcherService],
                              tns='votre_namespace',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())
    wsgi_app = WsgiApplication(application)
    start_file_watcher()
    wsgi_app.run()
    twisted_apps = [
        (wsgi_app, b'votrenom'),
    ]

sys.exit(run_twisted(twisted_apps, 8001))