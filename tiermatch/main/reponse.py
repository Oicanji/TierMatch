from django.http import HttpResponse
from json import dumps

code = {
    200: 'A requisição [:method][:suffix]foi realizada com sucesso',
    400: 'A requisição [:method][:suffix]não foi realizada devido a um erro na requisição',
    403: 'A requisição [:method][:suffix]não foi realizada devido a uma ação inválida',
    404: 'A requisição [:method][:suffix]não foi realizada devido a um recurso não encontrado',
    500: 'A requisição [:method][:suffix]não foi realizada devido a um erro interno',
}
"""
    @param code: int
    @param params: dict
"""
def response(code_int, params = {}):
    data = ''
    method = ''
    suffix = ''
    if 'response' in params and isinstance(params['response'], dict):
        data = dumps(params['response'])
    elif 'response' in params:
        data = params['response']
        
    if 'method' in params:
        method = 'ao ' +params['method']+ ' '
    
    if 'suffix' in params:
        suffix = 'uma ' +params['suffix']+ ' '

    res_text = code[code_int].replace('[:method]', method).replace('[:suffix]', suffix)
    res = {
        'code': code_int,
        'message': res_text,
    }
    if data != '':
        res['data'] = data

    if 'route' in params:
        res['route'] = params['route']
    return HttpResponse(dumps(res), content_type='text/plain')
