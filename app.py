from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route('/qrcode', methods=['GET'])
def get_qrcode():
    return send_from_directory('qrcode', 'qrcode.png', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)