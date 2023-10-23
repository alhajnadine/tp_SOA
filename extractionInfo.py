import logging
logging.basicConfig(level=logging.DEBUG)
import sys 
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
from spyne import ComplexModel
import csv

class reponse(ComplexModel):
    Nom = Unicode
    Adresse = Unicode
    Telephone = Unicode
    MontantPret = Unicode
    DureePret = Unicode
    TypeBatiment = Unicode
    NbrEtage = Unicode
    TypeQuartier = Unicode
    RevenueMens = Unicode
    DepenseMens = Unicode

class ExtractionInformationIE(ServiceBase):
    @rpc(Unicode, _returns=reponse)
    def ExtractionInformationIE(ctx, chemin):
        with open(chemin,'r')as file:
            reader = csv.reader(file)
            next (reader)
            reader2= next(reader)
            if reader2: 
                Nom =reader2[0]
                Adresse=reader2[1]
                Telephone=reader2[2]
                MontantPret=reader2[3]
                DureePret=reader2[4]
                TypeBatiment=reader2[5]
                NbrEtage=reader2[6]
                TypeQuartier=reader2[7]
                RevenueMens=reader2[8]
                DepenseMens=reader2[9]
                response = reponse(Nom=Nom, Adresse=Adresse, Telephone=Telephone, MontantPret=MontantPret,
                                DureePret=DureePret, TypeBatiment=TypeBatiment,NbrEtage=NbrEtage, TypeQuartier=TypeQuartier, RevenueMens=RevenueMens,
                                DepenseMens=DepenseMens)
        return response



application = Application([ExtractionInformationIE],
                          tns='spyne.examples.hello',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )

if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    twisted_apps = [
        (wsgi_app, b'ExtractionInformationIE'),
    ]
    
    sys.exit(run_twisted(twisted_apps, 8002))