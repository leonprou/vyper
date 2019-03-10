from vyper.parser import parser
from astexport.export import export_dict, export_json
import json
import ast
#
# def parse_to_json(code, contract_name, interface_codes):
#     trees = parser.parse_to_ast(code)
#     json_file = []
#     for tree in trees:
#         json_file.append(export_dict(tree))
#
#     return json.dumps(json_file, indent=4,
#         sort_keys=True,
#         separators=(",", ": "))

def parse_to_json(code, contract_name, interface_codes):
    trees = parser.parse_to_ast(code)
    m = ast.Module(trees)
    contract_json  = export_dict(m)
    contract_json['name'] = contract_name
    return json.dumps(contract_json, indent=4,
            sort_keys=True,
            separators=(",", ": "))
