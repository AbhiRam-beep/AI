facts = [
    ("Parent", ["John", "Mary"]),
    ("Parent", ["Mary", "Alice"])
]

rules = [
    ([("Parent", ["x", "y"]), ("Parent", ["y", "z"])],
     ("Grandparent", ["x", "z"]))
]

def unify(x, y, subst):
    if subst is None:
        return None
    if x == y:
        return subst
    if isinstance(x, str) and x.islower():
        return unify_var(x, y, subst)
    if isinstance(y, str) and y.islower():
        return unify_var(y, x, subst)
    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x[1]) != len(y[1]):
            return None
        for a, b in zip(x[1], y[1]):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    return None

def unify_var(var, val, subst):
    if var in subst:
        return unify(subst[var], val, subst)
    if val in subst and val.islower():
        return unify(var, subst[val], subst)
    subst[var] = val
    return subst

def substitute(term, subst):
    if isinstance(term, str):
        return subst.get(term, term)
    return (term[0], [substitute(a, subst) for a in term[1]])

def forward_chain(facts, rules, query):
    new_facts = facts[:]
    added = True
    while added:
        added = False
        for premises, conclusion in rules:
            for fact1 in new_facts:
                for fact2 in new_facts:
                    if fact1 == fact2 and len(premises) > 1:
                        continue
                    subst = {}
                    subst = unify(premises[0], fact1, subst)
                    if subst is None:
                        continue
                    if len(premises) > 1:
                        subst = unify(premises[1], fact2, subst)
                    if subst is not None:
                        inferred = substitute(conclusion, subst)
                        if inferred not in new_facts:
                            new_facts.append(inferred)
                            added = True
    return query in new_facts

query = ("Grandparent", ["John", "Alice"])
print(forward_chain(facts, rules, query))
