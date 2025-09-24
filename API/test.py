import json
with open("API\capabilityMappingv2.json") as f:
    capDict = json.load(f)

print(capDict)