import re

def is_variable(term):
    return term.islower() and len(term) == 1

def parse_predicate(sentence):
    predicate, args = re.match(r'(\w+)\((.*)\)', sentence).groups()
    args = args.split(', ')
    return predicate, args

def unify(sentence1, sentence2):
    predicate1, args1 = parse_predicate(sentence1)
    predicate2, args2 = parse_predicate(sentence2)

    if predicate1 != predicate2 or len(args1) != len(args2):
        return {}

    substitutions = {}
    for arg1, arg2 in zip(args1, args2):
        if is_variable(arg1) and not is_variable(arg2):
            substitutions[arg1] = arg2
        elif is_variable(arg2) and not is_variable(arg1):
            substitutions[arg2] = arg1
        elif arg1 != arg2:
            return {}

    return substitutions

def negate(clause):
    return ['¬' + literal[1:] if literal.startswith('¬') else '¬' + literal for literal in clause]

def resolve(clause1, clause2):
    resolved_clause = set()
    for literal1 in clause1:
        for literal2 in clause2:
            if literal1 == '¬' + literal2 or '¬' + literal1 == literal2:
                if unify(literal1, literal2):
                    new_clause = (set(clause1) | set(clause2)) - {literal1, literal2}
                    resolved_clause |= new_clause
    return list(resolved_clause)

def inference_by_resolution(kb, query):
    negated_query = negate(query)
    clauses = kb + [negated_query]

    new = set()
    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        for (ci, cj) in pairs:
            resolvent = resolve(ci, cj)
            if not resolvent:
                return True  # Query is true
            new.add(frozenset(resolvent))
        if new.issubset(set(map(frozenset, clauses))):
            return False  # Query is false
        for clause in new:
            if clause not in clauses:
                clauses.append(list(clause))

# Testing
print(unify('Parent(x, y)', 'Parent(John, Mary)'))  # Should output {'x': 'John', 'y': 'Mary'}
print(unify('Loves(father(x), x)', 'Loves(father(John), John)'))  # Should output {'x': 'John'}
print(unify('Parent(x, x)', 'Parent(John, Mary)'))  # Should output {}

# Knowledge base and query for inference test
kb = [
    ['¬King(x)', '¬Greedy(x)', 'Evil(x)'],
    ['King(John)'],
    ['Greedy(x)']
]
query = ['Evil(John)']
print(inference_by_resolution(kb, query))  # Should output True
