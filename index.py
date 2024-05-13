from flask import Flask,request
import json
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#Creamos una instancia de Flask
app = Flask(__name__)

#Cargamos la informacion de nuestro archivo config.json
f = open('config.json', 'r')
env = json.loads(f.read())

#Creamos nuestro primer servicio web
@app.route('/test', methods=['GET'])
def test():
    return 'Hello World!'

#Creamos nuestro segundo servicio web,enviamos un SMS(API Twilio)
@app.route('/send_sms', methods=['POST'])
def send_sms():
    try:
        account_sid = env['TWILIO_ACCOUNT_SID']
        auth_token = env['TWILIO_AUTH_TOKEN']
        origen = env['TWILIO_PHONE_NUMBER']
        client = Client(account_sid, auth_token)
        data = request.json
        contenido = data["contenido"]
        destino = data["destino"]
       
        message = client.messages.create(
                            body=contenido,
                            from_=origen,
                            to='+57' + destino
                        )
        print(message)
        return "send success"
    except Exception as e:
        print(e)
        return "error"
    
#Creamos nuestro tercer servicio web,enviamos un correo(API SendGrid)
@app.route('/send_email', methods=['POST'])
def send_email():
    #Capturar la informacion de la solicitud
    data = request.json
    contenido = data["contenido"]
    destino = data["destino"]
    asunto = data["asunto"]
    print(contenido,destino,asunto)
    #Creo el mensaje de correo
    message = Mail(
        from_email=env['SENGRIDEMAIL'],
        to_emails=destino,
        subject=asunto,
        html_content=contenido
    )
    try:
        sg = SendGridAPIClient(env['SENGRIDKEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "send success"
    except Exception as e:
        print(e)
        return "error"



#Ejecutamos el servidor
if __name__ == '__main__':
    app.run()
    
    