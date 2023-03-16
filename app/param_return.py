import json
from flask import jsonify

class paramReturm:
    codes = {
        200: "Sucesso",
        400: "Requisição inválida",
        401: "Não autorizado",
        403: "Proibido",
        404: "Não encontrado",
        405: "Método não permitido",
        500: "Erro interno do servidor",
        503: "Serviço indisponível",
    }
    def __init__(self):
        self.code = ''
        self.message = ''
        self.data = False

    def __str__(self):
        return "Code: " + str(self.code) + " Message: " + self.message + " Data: " + str(self.data)

    def format(self):
        value = {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }
        #limpa os todos os valores
        self.code = ''
        self.message = ''
        self.data = False

        return value
    
    #recebe o codigo e se tiver parametros adicionais, adiciona no data
    def parse(self, code, data = False):
        self.code = code
        self.message = self.codes[code]
        self.data = jsonify(data)

        #retorna em json
        return jsonify(self.format())