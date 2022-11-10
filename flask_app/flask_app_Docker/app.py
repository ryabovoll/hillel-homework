from flask import Flask
from flask import request
from datetime import datetime
from random import choices
from os import environ

app = Flask(__name__)


@app.route("/whoami")
def client_browser():
    return f"<p>Client browser = {request.user_agent}!</p>" \
           f"<p>IP = {request.remote_addr}</p>" \
           f"<p>Time now = {datetime.now().strftime('%H:%M:%S')}</p>"


@app.route("/source_code")
def source_code():
    with open(__file__, 'r') as f:
        return f"<plaintext>{f.read()}"


@app.route("/random")
def random_str():
    length = int(request.values.get('length', 0))
    specials = int(request.values.get('specials', 0))
    digits = int(request.values.get('digits', 0))
    result = ''
    if length not in range(1, 101) or specials not in (0, 1) or digits not in (0, 1):
        result += f"<p> length is not valid </p>" if length not in range(1, 101) else ""
        result += f"<p> specials is not valid </p>" if specials not in (0, 1) else ""
        result += f"<p> digits is not valid </p>" if digits not in (0, 1) else ""
    else:
        string = [chr(letter) for letter in list(range(65, 91)) + list(range(97, 123))]
        string += [chr(sign) for sign in list(range(48, 58))] if specials else ""
        string += [chr(number) for number in list(range(33, 48))] if digits else ""
        result = "".join(choices(string, k=length))
    return result


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(app.run(debug=True, host='0.0.0.0', port=port))
