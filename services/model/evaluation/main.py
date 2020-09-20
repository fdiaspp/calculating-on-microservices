from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import json


class Expression:

    def __init__(self, expression):
        self.expression = expression
        self.character = 0
        self.state = 0

    def analex(self):
        
        value = ''
        matrix = []

        while True:

            char = self.expression[self.character]

            if self.state == 0:
                if char.isdigit():
                    value += char

                elif char in ['.', ','] :
                    value += '.'
                    self.state = 1
                    
                else:
                    matrix.append(['NUMBER', value])
                    value = ''
                    self.character -= 1
                    self.state = 2

                if len(self.expression) <= self.character + 1:
                    matrix.append(['NUMBER', value])
                    break
            
            elif self.state == 1:
                
                if char.isdigit():
                    value += char

                else:
                    matrix.append(['NUMBER', value])
                    value = ''
                    self.character -= 1
                    self.state = 2                    

                if len(self.expression) <= self.character + 1:
                    matrix.append(['NUMBER', value])
                    break

            elif self.state == 2:                
                
                if char == '+':
                    matrix.append(['OP_SUM', ''])

                elif char == '-':
                    matrix.append(['OP_SUB', ''])                

                elif char in ['/', 'd']:
                    matrix.append(['OP_DIV', ''])

                elif char == '*':
                    matrix.append(['OP_MULT', ''])

                else:
                    self.character -= 1
                
                self.state = 0                    

            if len(self.expression) <= self.character + 1:
                break
            else:
                self.character += 1 

        return matrix

    def requisition(self, url):
        try:
            r = requests.get(url)
            d = json.loads(r.content)
            if d['status'] == 'success':
                return d['data']['result']
            else:
                print("Error on requisition.", url, d)
                return 0                
        except Exception as e:
            print("Error on requisition.", url, e)
            return 0

    def execute(self):
        num_stack = []
        num_side_stack = []
        op_stack = []
        op_side_stack = []
        lemmas = self.analex()


        for l in lemmas:               

            if l[0] == 'NUMBER':
                num_stack.append(float(l[1]))
            else:
                op_stack.append(l[0])


        for _ in range(len(op_stack)):
            op = op_stack.pop()
            b = num_stack.pop()
            a = num_stack.pop()

            if op in ['OP_SUM', 'OP_SUB']:
                num_stack.append(a)
                num_side_stack.append(b)
                op_side_stack.append(op)

            if op == 'OP_MULT':
                print('*', a,b)
                num_stack.append(
                    self.requisition(f'http://operation-mult/{a}/{b}')
                )

            if op == 'OP_DIV':
                print('/',a,b)
                num_stack.append(
                    self.requisition(f'http://operation-div/{a}/{b}')
                )                

        for _ in range(len(op_side_stack)):
            op = op_side_stack.pop()
            a = num_stack.pop()

            try:
                b = num_side_stack.pop()
            except:
                b = num_stack.pop()

            if op == 'OP_SUM':
                print('+',a,b)
                num_stack.append(
                    self.requisition(f'http://operation-sum/{a}/{b}')
                )                

            if op == 'OP_SUB':
                print('-',a,b)
                num_stack.append(
                    self.requisition(f'http://operation-sub/{a}/{b}')
                )                            
           
        return num_stack.pop()


class Principal(Resource):
    def get(self, text):
        
        op = Expression(text)
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
    
    api.add_resource(Principal, '/<string:text>')    
    app.run(debug=True, host="0.0.0.0", port=80)
