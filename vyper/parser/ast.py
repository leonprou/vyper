from vyper.parser import parser
from astexport.export import export_dict, export_json
import json
import ast
import ntpath
from vyper.parser.global_context import GlobalContext

def parse_to_json(code, contract_filename, interface_codes):
    ast_code = parser.parse_to_ast(code)
    m = ast.Module(ast_code)
    contract_json  = export_dict(m)

    global_ctx = GlobalContext.get_global_context(ast_code, interface_codes=interface_codes)

    add_vyper_attributes(global_ctx, contract_json)

    contract_json['name'] = get_contract_name(contract_filename)
    contract_json['vyper_type'] = 'ContractDef'
    # print(_names_events)
    return json.dumps(contract_json, indent=4,
            sort_keys=True,
            separators=(",", ": "))

def get_contract_name(contract_filename):
    filename = ntpath.basename(contract_filename)
    if ('.' in filename):
        return filename.split('.')[0]
    else:
        return filename

def add_vyper_attributes(global_ctx, contract_json):
    add_event_attributes(global_ctx, contract_json)
    add_function_attibutes(global_ctx, contract_json)
    add_rest_attibutes(contract_json)

# FunctionDefinition
def add_event_attributes(global_ctx, contract_json):
    _names_events = {_event.target.id for _event in global_ctx._events}
    assignment_declarations = [
        top_declaration for top_declaration in contract_json['body']
        if top_declaration['ast_type'] == 'AnnAssign']

    for top_declaration in assignment_declarations:
        if ('target' in top_declaration and 'id' in top_declaration['target']):
            if top_declaration['target']['id'] in _names_events:
                 top_declaration['vyper_type'] = 'EventDef'
            else:
                 top_declaration['vyper_type'] = 'VariableDeclaration'

def add_function_attibutes(global_ctx, contract_json):
    func_declarations = [
        top_declaration for top_declaration in contract_json['body']
        if top_declaration['ast_type'] == 'FunctionDef']
    for top_declaration in func_declarations:
        top_declaration['vyper_type'] = 'FunctionDef'

def add_rest_attibutes(contract_json):
    top_declarations = [
        top_declaration for top_declaration in contract_json['body']
        if 'vyper_type' not in top_declaration]
    for top_declaration in top_declarations:
        top_declaration['vyper_type'] = top_declaration['ast_type']
