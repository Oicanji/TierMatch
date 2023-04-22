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

    print(res)
    return HttpResponse(dumps(res), content_type='text/plain')

def format_values(args):
    params = {}
    for i in args['response']:
        params["name"] = i['name']
        params["description"] = i['description']
        params["create_id"] = i['create_by_id'].id
        params["create_name"] = i['create_by_id'].username
        params["create_at"] = i['create_at'].strftime("%d/%m/%Y %H:%M:%S")
        params["super_allow_allias"] = i['super_allow_allias']
        params["allow_allias"] = i['allow_allias']
        params["deny_allias"] = i['deny_allias']
        params["super_allow_color"] = i['super_allow_color']
        params["allow_color"] = i['allow_color']
        params["deny_color"] = i['deny_color']
        params["categories"] = i["categories"]  
        return params
