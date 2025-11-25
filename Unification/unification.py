import re

# Check if a term is a variable
def is_variable(x):
    return isinstance(x, str) and x.islower() and x.isalpha()

# Parse a term into either string or (functor, args)
def parse_term(term):
    term = term.replace(" ", "")
    if "(" not in term:
        return term
    m = re.match(r'(\w+)\((.*)\)', term)
    functor = m.group(1)
    args = []
    arg_str = m.group(2)
    balance = 0
    start = 0
    for i, c in enumerate(arg_str):
        if c == ',' and balance == 0:
            args.append(parse_term(arg_str[start:i]))
            start = i + 1
        elif c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
    args.append(parse_term(arg_str[start:]))
    return (functor, args)

# Occurs check to prevent infinite substitution
def occurs_check(var, x, subst):
    if var == x:
        return True
    elif isinstance(x, tuple):
        return any(occurs_check(var, arg, subst) for arg in x[1])
    elif x in subst:
        return occurs_check(var, subst[x], subst)
    return False

# Unify two terms with existing substitutions
def unify(x, y, subst=None):
    if subst is None:
        subst = {}
    if x == y:
        return subst
    if is_variable(x):
        return unify_var(x, y, subst)
    if is_variable(y):
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

# Unify a variable with a term
def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    if occurs_check(var, x, subst):
        return None
    subst[var] = x
    return subst

# Example terms
t1 = "P(f(x), g(y), y)"
t2 = "P(f(a), g(b), b)"

parsed1 = parse_term(t1)
parsed2 = parse_term(t2)

result = unify(parsed1, parsed2, {})

if result:
    print("Unifier:", result)
else:
    print("Cannot unify")
