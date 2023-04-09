import json

with open('blog_scrapping.json', 'r') as f:
    data = json.load(f)

with open('agg_data.json', 'r') as f:
    old_data = json.load(f)

new_data = []
for obj in data["sample"]:
    new_data.append({
        "prompt": obj,
        "category": "blog"
    })

old_data.extend(new_data)
with open('agg_data.json', 'w') as f:
    json.dump(old_data, f, indent=4)