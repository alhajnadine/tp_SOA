import logging
logging.basicConfig(level=logging.DEBUG)
import sys 
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted

class Solvabilite(ServiceBase):
    @rpc(Unicode, Unicode, _returns=float)
    def Solvabilite(ctx, RevenueMens,DepenseMens):
            debit = 2000
            retard = 1
            faillite = 1
            score = 1000 - debit * 0.1 - retard * 50
            
            if RevenueMens < DepenseMens :
                score = score - 200

            if faillite != 0 :
                score = score - (250*faillite)
            return score

application = Application([Solvabilite],
                          tns='spyne.examples.hello',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )

if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    twisted_apps = [
        (wsgi_app, b'Solvabilite'),
    ]
    
    sys.exit(run_twisted(twisted_apps, 8003))