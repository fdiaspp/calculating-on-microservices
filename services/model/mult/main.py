from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS


class Mult:

    def __init__(self, numa, numb):
        self.numa = numa
        self.numb = numb

    def execute(self):
        return self.numa * self.numb


class Principal(Resource):
    def get(self,numa, numb):
        
        op = Mult(numa, numb)
        result = op.execute()
        return {
            'status': 'success',
            'data': {
                'result': result
            }
        }

if __name__ == '__main__':

    app = Flask(__name__)
    api = Api(app)
    CORS(app)
    
    api.add_resource(Principal, '/<float:numa>/<float:numb>', '/<int:numa>/<int:numb>')    
    app.run(debug=True, host="0.0.0.0", port=80)
