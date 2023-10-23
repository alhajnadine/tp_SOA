import logging
logging.basicConfig(level=logging.DEBUG)
import sys 
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted


class Decision(ServiceBase):
    @rpc(float, Unicode, _returns=Unicode)
    def Decision(ctx, reponse2,reponse3):
        if ( 500 < reponse2 and reponse2 <= 700 ) and reponse3 != 'Cher' :
            PretRes = 'Prêt accordé' 
        elif 700 < reponse2 : 
            PretRes = 'Prêt accordé'
        elif ( 400 < reponse2 and reponse2 <= 500 ) and reponse3 == 'Pas Cher' :
            PretRes = 'Prêt accordé'
        else : 
            PretRes = 'Prêt refusé'
        return PretRes



application = Application([Decision],
                          tns='spyne.examples.hello',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )

if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    twisted_apps = [
        (wsgi_app, b'Decision'),
    ]
    
    sys.exit(run_twisted(twisted_apps, 8005))