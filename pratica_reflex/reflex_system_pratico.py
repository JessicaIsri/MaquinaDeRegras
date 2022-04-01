from inference_engine import Inference, Rule
import pymongo
'''
Exemplo para detectar se é soja
{rules: [
            {relation:">=", percept_ref: "0.6", percept_name:"amplitude", action:"True"},
            {relation:">=", percept_ref: "90", percept_name:"duration", action:"True"}
        ],
operators: ["and"],
action: ["soy"]
}
{rules: [
            {relation:">=", percept_ref: "0.6", percept_name:"amplitude", action:"True"},
            {relation:"<", percept_ref: "90", percept_name:"duration", action:"True"}
        ],
operators: ["and"],
action: ["cover_plating"]
}
{rules: [
            {relation:">=", percept_ref: "90", percept_name:"duration", action:"True"},
            {relation:"<", percept_ref: "0.6", percept_name:"amplitude", action:"True"}
        ],
operators: ["and"],
action: ["straw"]
}
'''

application_client = pymongo.MongoClient("mongodb://localhost:27017/")
application_db = application_client["reflex_pratice"]
application_collection = application_db["rule_collection"]


# composite_rule = {'rules': [
#             {'relation':">=", 'percept_ref': "0.6", 'percept_name':"amplitude", 'action':"True"},
#             {'relation':"<", 'percept_ref': "90", 'percept_name':"duration", 'action':"True"}],
#     'operators': ["and"],
#     'action': ["straw"]
# }
# x = application_collection.insert_one(composite_rule)

composite_rules = application_collection.find()
inferences = []
for composite_rule in composite_rules:
    rules = []
    for rule in composite_rule['rules']:
        r = Rule(rule['relation'], rule['percept_ref'], rule['percept_name'], rule['action'])
        rules.append(r)
    inferences.append(Inference(rules, composite_rule['operators'], composite_rule['action']))

print("Inferences: ")
print(inferences)


percepts = [
    {'amplitude': '0.7', 'duration': '100'},
    {'amplitude': '0.6', 'duration': '50'},
    {'amplitude': '0.3', 'duration': '100'},
]

count = 1


for inference in inferences:
    print("Analysing inference rule # " + str(count))
    for percept in percepts:
        print(inference.infer(percept))
    count += 1