import json
from app.main import Rule, EarleyParser


def test_general():
    for id_ in range(1, 5):
        with open(f'tests/test{id_}.json') as input_file:
            dictionary = json.load(input_file)
            results = dictionary["answers"]
            words = dictionary["words"]
            rules = dictionary["rules"]
            for i in range(len(rules)):
                rules[i] = Rule(rules[i][0], rules[i][1])
            parser = EarleyParser(rules)
            for i in range(len(words)):
                assert (parser.check(words[i]) == results[i])
