from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def proxy():
    if request.method == 'POST':
        try:
            target_url = request.form.get('url')
            lang = request.form.get('lang')
            headers = {'Accept-Language': lang}

            # Remove the port 443 from the target_url
            target_url = target_url.replace(':443', '')

            response = requests.get(target_url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return render_template('proxy.html', url=target_url, response=response.text)
        except requests.exceptions.RequestException as e:
            return render_template('error.html', error=str(e))

    return render_template('proxy.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
