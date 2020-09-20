from flask import Flask, render_template

app = Flask(__name__, template_folder='public')

@app.route('/')
@app.route('/<page>')
def index(page='index.html'):
    return render_template(f'{page}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)