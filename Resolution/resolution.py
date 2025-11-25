# ---------- INPUT ----------
KB = [
    "(A -> B)",
    "(B -> C)",
    "A"
]

QUERY = "C"


# ---------- TOKENIZER ----------
def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c in "()∧∨¬":
            tokens.append(c)
            i += 1
        elif c == '-' and i+1 < len(expr) and expr[i+1] == '>':
            tokens.append("->")
            i += 2
        elif c == '<' and expr[i:i+3] == "<->":
            tokens.append("<->")
            i += 3
        elif c.isalpha():
            j = i
            while j < len(expr) and expr[j].isalnum():
                j += 1
            tokens.append(expr[i:j])
            i = j
        else:
            i += 1
    return tokens


# ---------- PARSER (recursive descent) ----------
def parse(tokens):
    def parse_imp(i):
        node, i = parse_iff(i)
        while i < len(tokens) and tokens[i] == "->":
            right, i = parse_iff(i+1)
            node = ("->", node, right)
        return node, i

    def parse_iff(i):
        node, i = parse_or(i)
        while i < len(tokens) and tokens[i] == "<->":
            right, i = parse_or(i+1)
            node = ("<->", node, right)
        return node, i

    def parse_or(i):
        node, i = parse_and(i)
        while i < len(tokens) and tokens[i] == "∨":
            right, i = parse_and(i+1)
            node = ("∨", node, right)
        return node, i

    def parse_and(i):
        node, i = parse_not(i)
        while i < len(tokens) and tokens[i] == "∧":
            right, i = parse_not(i+1)
            node = ("∧", node, right)
        return node, i

    def parse_not(i):
        if i < len(tokens) and tokens[i] == "¬":
            n, j = parse_not(i+1)
            return ("¬", n), j
        return parse_atom(i)

    def parse_atom(i):
        if tokens[i] == "(":
            node, j = parse_imp(i+1)
            return node, j+1
        return tokens[i], i+1

    return parse_imp(0)[0]


# ---------- ELIMINATE → and ↔ ----------
def elim_imp(n):
    if isinstance(n, str):
        return n
    op = n[0]
    if op == "->":
        A = elim_imp(n[1])
        B = elim_imp(n[2])
        return ("∨", ("¬", A), B)
    if op == "<->":
        A = elim_imp(n[1])
        B = elim_imp(n[2])
        return ("∧", ("∨", ("¬", A), B), ("∨", ("¬", B), A))
    if op in ("∧", "∨"):
        return (op, elim_imp(n[1]), elim_imp(n[2]))
    if op == "¬":
        return ("¬", elim_imp(n[1]))
    return n


# ---------- PUSH ¬ INWARD (NNF) ----------
def nnf(n):
    if isinstance(n, str):
        return n
    op = n[0]
    if op == "¬":
        x = n[1]
        if isinstance(x, str):
            return ("¬", x)
        if isinstance(x, tuple) and x[0] == "¬":
            return nnf(x[1])
        if isinstance(x, tuple) and x[0] == "∧":
            return ("∨", nnf(("¬", x[1])), nnf(("¬", x[2])))
        if isinstance(x, tuple) and x[0] == "∨":
            return ("∧", nnf(("¬", x[1])), nnf(("¬", x[2])))
        return ("¬", nnf(x))
    if op in ("∧", "∨"):
        return (op, nnf(n[1]), nnf(n[2]))
    return n


# ---------- DISTRIBUTE ∨ OVER ∧ ----------
def dist(a, b):
    if isinstance(a, tuple) and a[0] == "∧":
        return ("∧", dist(a[1], b), dist(a[2], b))
    if isinstance(b, tuple) and b[0] == "∧":
        return ("∧", dist(a, b[1]), dist(a, b[2]))
    return ("∨", a, b)

def cnf(n):
    if isinstance(n, str):
        return n
    op = n[0]
    if op == "∧":
        return ("∧", cnf(n[1]), cnf(n[2]))
    if op == "∨":
        return dist(cnf(n[1]), cnf(n[2]))
    if op == "¬":
        return ("¬", cnf(n[1]))
    return n


# ---------- EXTRACT CLAUSES (produce literal strings) ----------
def flatten_or_to_literals(n):
    if isinstance(n, str):
        return {n}
    if isinstance(n, tuple) and n[0] == "∨":
        return flatten_or_to_literals(n[1]) | flatten_or_to_literals(n[2])
    if isinstance(n, tuple) and n[0] == "¬":
        inner = n[1]
        if isinstance(inner, str):
            return {"¬" + inner}
        # fallback
        return {"¬" + str(inner)}
    # fallback for unexpected node types
    return {str(n)}

def get_clauses(n):
    if isinstance(n, str):
        return [set([n])]
    if isinstance(n, tuple) and n[0] == "∧":
        return get_clauses(n[1]) + get_clauses(n[2])
    # otherwise it's a disjunction or negation (single clause)
    return [flatten_or_to_literals(n)]


# ---------- RESOLVE ----------
def resolve(C1, C2):
    resolvents = []
    for lit in C1:
        neg = ("¬" + lit) if not lit.startswith("¬") else lit[1:]
        if neg in C2:
            new = (C1 - {lit}) | (C2 - {neg})
            resolvents.append(new)
    return resolvents


# ---------- FULL RESOLUTION ----------
def resolution(KB, Q):
    clauses = []

    for s in KB:
        t = tokenize(s)
        p = parse(t)
        c = elim_imp(p)
        c = nnf(c)
        c = cnf(c)
        clauses += get_clauses(c)

    nq = ("¬", Q)
    t = tokenize("(" + "¬" + Q + ")")  
    clauses.append({ "¬" + Q })

    # normalize to frozensets
    clauses = [frozenset(c) for c in clauses]

    while True:
        new = set()
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                r = resolve(set(clauses[i]), set(clauses[j]))
                for c in r:
                    if len(c) == 0:
                        return True
                    new.add(frozenset(c))
        if new.issubset(set(clauses)):
            return False
        for f in new:
            if f not in clauses:
                clauses.append(f)


# ---------- RUN ----------
print(resolution(KB, QUERY))
