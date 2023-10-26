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

        client= Client('http://localhost:8002/ExtractionInformationIE?wsdl')
        reponse= client.service.ExtractionInformationIE(event.src_path)
       

        RevenueMens=reponse.RevenueMens
        DepenseMens=reponse.DepenseMens
        client2= Client('http://localhost:8003/Solvabilite?wsdl')
        reponse2=client2.service.Solvabilite(RevenueMens,DepenseMens)
        print(reponse2)

        TypeBatiment= reponse.TypeBatiment
        NbrEtage=reponse.NbrEtage
        TypeQuartier =reponse.TypeQuartier
        client3= Client('http://localhost:8004/Prop?wsdl')
        reponse3=client3.service.Prop(TypeBatiment,NbrEtage,TypeQuartier)
        print(reponse3)

        client4= Client('http://localhost:8005/Decision?wsdl')
        reponse4= client4.service.Decision(reponse2,reponse3)
        print(reponse4)



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