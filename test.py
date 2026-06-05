import json 
info= set()
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
for i in data:
    info.add(i["brand"])
print(info)
print(len(info))