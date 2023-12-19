id_offset = 1000


def apply_id_offset(api):
    new_api = {}
    for node_id in api:
        node = api[node_id]
        inputs = node['inputs']
        for pin in inputs:
            if isinstance(inputs[pin], list):
                pin_data = inputs[pin]
                pin_data[0] = str(int(pin_data[0]) + id_offset)
        new_node_id = str(int(node_id) + id_offset)
        new_api[new_node_id] = node

    return new_api


def apply_rule(api, rule):
    refactor_map = {}
    for node_id in api:
        node = api[node_id]
        if node['class_type'] in rule:
            rule_item = rule[node['class_type']]

            inputs = node['inputs']

            for pin in inputs:
                if pin in rule_item:
                    pin_data = inputs[pin]
                    if pin_data in rule_item[pin]:
                        refactor_map[node_id] = str(rule_item[pin][pin_data])

    new_api = {}
    for node_id in api:
        node = api[node_id]
        inputs = node['inputs']
        for pin in inputs:
            if isinstance(inputs[pin], list):
                pin_data = inputs[pin]
                if pin_data[0] in refactor_map:
                    pin_data[0] = refactor_map[pin_data[0]]
        if node_id in refactor_map:
            new_api[refactor_map[node_id]] = node
        else:
            new_api[node_id] = node
    return new_api

# api_fp = open("api.json")
# api_json = json.load(api_fp)
# api_fp.close()
# rule_fp = open("rule.json")
# rule_json = json.load(rule_fp)
# rule_fp.close()

# api_json = apply_id_offset(api_json)
# api_json = apply_rule(api_json, rule_json)

# with open("converted.json","w") as f:
#     json.dump(api_json, f, indent=2)
