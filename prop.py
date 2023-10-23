import logging
logging.basicConfig(level=logging.DEBUG)
import sys
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted


class Prop(ServiceBase):
    @rpc(Unicode, Unicode,Unicode, _returns=Unicode)
    def Prop(ctx, TypeBatiment,NbrEtage,TypeQuartier):
            TypeQuartier = 0
            TypeBatiment= 0

            if TypeQuartier == 'Calme' :
                TypeQuartier = TypeQuartier + 3 #3
            elif TypeQuartier == 'Moyen' : 
                TypeQuartier = TypeQuartier + 2
            else :
                TypeQuartier = TypeQuartier + 1

            if TypeBatiment == 'Maison' :
                TypeBatiment = TypeBatiment + 3
            elif TypeBatiment == 'Pavillon': 
                TypeBatiment = TypeBatiment + 2
            else : 
                TypeBatiment = TypeBatiment + 1 #1
            
            prop = TypeBatiment + TypeQuartier + int(NbrEtage)*2 

            if prop >= 8 : 
                 classification = 'Cher'
            elif prop == 6 :
                 classification = 'Moyen'
            else :
                 classification = 'Pas Cher'
            return classification

application = Application([Prop],
                          tns='spyne.examples.hello',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )

if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    twisted_apps = [
        (wsgi_app, b'Prop'),
    ]
    
    sys.exit(run_twisted(twisted_apps, 8004))