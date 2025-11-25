import itertools

def parse_expr(expr, values):
    s = expr
    for var, val in values.items():
        s = s.replace(var, str(val))
    
    # Replace operators with Python equivalents
    s = s.replace('^', ' and ')
    s = s.replace('v', ' or ')
    s = s.replace('!', ' not ')
    
    # Replace implication a->b with (not a or b)
    while '->' in s:
        i = s.find('->')
        # Find left operand
        l = i-1
        while l >=0 and s[l] not in ' ()':
            l -= 1
        left = s[l+1:i].strip()
        # Find right operand
        r = i+2
        while r < len(s) and s[r] not in ' ()':
            r += 1
        right = s[i+2:r].strip()
        s = s[:l+1] + f'((not {left}) or {right})' + s[r:]
    
    # Replace biconditional a<->b with (a and b) or (!a and !b)
    while '<->' in s:
        i = s.find('<->')
        l = i-1
        while l >=0 and s[l] not in ' ()':
            l -= 1
        left = s[l+1:i].strip()
        r = i+3
        while r < len(s) and s[r] not in ' ()':
            r += 1
        right = s[i+3:r].strip()
        s = s[:l+1] + f'(({left} and {right}) or (not {left} and not {right}))' + s[r:]
    
    return eval(s)

def entails(kb, query):
    vars_set = set([c for c in kb + query if c.isalpha()])
    vars_list = sorted(vars_set)

    for vals in itertools.product([False, True], repeat=len(vars_list)):
        assignment = dict(zip(vars_list, vals))
        kb_val = parse_expr(kb, assignment)
        query_val = parse_expr(query, assignment)
        if kb_val and not query_val:
            return False
    return True

# Input example
kb = input("Enter KB: ")        # e.g., (a->b)^(b->c)
query = input("Enter Query: ")  # e.g., a->c

if entails(kb, query):
    print("Query is entailed by KB")
else:
    print("Query is NOT entailed by KB")
