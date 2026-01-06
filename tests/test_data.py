# tests/test_data.py

test_data = {
    "empty":      [],
    "integers":   [ 1, 2, 3, 4, 5, 2, 3 ],
    "strings":    [ "apple", "banana", "avocado", "blueberry" ],
    "dictionary": [
        { "name": "MichaelP", "year": 43 },
        { "name": "GrahamC", "year": 41 },
        { "name": "TerryG", "year": 40 },
        { "name": "EricI", "year": 43 },
        { "name": "JohnC", "year": 39 },
        { "name": "TerryJ", "year": 42 },
    ],
    "nested_dict": [
        { "id": 1, "people": [ { "name": "Bob" }, { "name": "James" } ] },
        { "id": 2, "people": [ { "name": "Harry" }, { "name": "Mikey" } ] }
    ],
}

def get_integers_avg() -> float:
    items_sum = 0
    items_count = 0
    for i in test_data['integers']:
        items_sum += i
        items_count += 1
    if items_count == 0:
        raise ValueError("Test collection 'integers' has no elements!")
    return items_sum / items_count

def get_integers_avg_with_predicate(predicate) -> float:
    items_sum = 0
    items_count = 0
    for i in [x for x in test_data['integers'] if predicate(x)]:
        items_sum += i
        items_count += 1
    if items_count == 0:
        raise ValueError("Test collection 'integers' has no elements!")
    return items_sum / items_count

def get_strings_grouped_by(predicate):
    grouped = {}
    for string in test_data['strings']:
        key = predicate(string)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(string)
    return list(grouped.items())
