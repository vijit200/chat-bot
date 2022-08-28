
from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    print(str(source_currency) + ' ' + str(amount) + ' ' + str(target_currency))


    
    cf=fetch_conversion_factor(source_currency,target_currency)
    final_ammount = amount * cf
    final_ammount = round(final_ammount,3)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_ammount,target_currency)
    }
    print(final_ammount)
    return jsonify(response)

def fetch_conversion_factor(source,target):
     url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=9aa0c54f5ad4c460c36d".format(source,target)

     response = requests.get(url)
     response = response.json()
     return response['{}_{}'.format(source,target)]

if __name__ == '__main__':
    app.run()