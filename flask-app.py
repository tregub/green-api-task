from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)


def mainFunc(apiMethod, method, payload):
    apiUrl = "https://7103.api.greenapi.com"
    idInstance = request.form.get('idInstance')
    apiTokenInstance = request.form.get('apiTokenInstance')
    apiUrl = f"{apiUrl}/waInstance{idInstance}/{apiMethod}/{apiTokenInstance}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request(method, apiUrl, data=payload, headers=headers)
    if response.status_code not in range(200, 299):
        return f"error: {response.status_code}, {response.content}"
    return json.dumps(response.json(), sort_keys=False, indent=2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getSettings():
    method = "GET"
    payload = {}
    apiMethod = request.form.get('action')
    if apiMethod in ['sendMessage', 'sendFileByUrl']:
        method = "POST"
        phoneNumber = request.form.get('phoneNumber')
        message = request.form.get('message')
        payload = {
            "chatId": f"{phoneNumber}@c.us",
            "message": f"{message}"
            }
        if apiMethod == "sendFileByUrl":
            phoneNumber = request.form.get('phoneNumberForURL')
            urlFile = request.form.get('urlFile')
            fileName = urlFile.split('/')[-1]
            payload = {
                "chatId": f"{phoneNumber}@c.us",
                "urlFile": urlFile,
                "fileName": fileName
            }
    response = mainFunc(apiMethod, method, json.dumps(payload))
    return render_template('index.html', response=response)


if __name__ == '__main__':
    app.run(debug=True)
