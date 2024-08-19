documents = [
    "The quick brown fox jumped over the lazy dog.",
    "The lazy dog slept in the sun.",
    "This is the third, this is it now.",
]


def postfix(infix_expr):
    prec = {"(": 0, ")": 0, "OR": 1, "AND": 2, "NOT": 3}
    stack = []
    postfix_expr = ""

    for token in infix_expr.split():
        if token in prec:
            if token == "(":
                stack.append(token)
            elif token == ")":
                while stack and stack[-1] != "(":
                    postfix_expr += stack.pop() + " "
                stack.pop()
            else:
                while stack and prec[stack[-1]] >= prec[token]:
                    postfix_expr += stack.pop() + " "
                stack.append(token)
        else:
            postfix_expr += token + " "

    while stack:
        postfix_expr += stack.pop() + " "

    return postfix_expr


def process_query(postfix_expr, inverted_index, doc_count):
    stack = []
    postfix_expr = postfix(postfix_expr)
    print(postfix_expr)
    prec = {"(": 0, ")": 0, "OR": 1, "AND": 2, "NOT": 3}

    for token in postfix_expr.split():
        if token not in prec:
            documents = set(inverted_index[token])
            stack.append(documents)
        elif token == "NOT":
            op = stack.pop()
            all_docs = {str(i+1) for i in range(doc_count)}
            result = all_docs.difference(op)
            print(result)
            stack.append(result)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            if token == "AND":
                result = op1.intersection(op2)
            elif token == "OR":
                result = op1.union(op2)
            stack.append(result)

    return stack.pop()


# Convert each document to lowercase and split it into words
tokens = [doc.lower().split() for doc in documents]

# Combine the tokens into a list of unique terms
terms = list(set([word for doc in tokens for word in doc]))

# Create an empty dictionary to store the inverted index
inverted_index = {}

# For each term, find the documents that contain it
for term in terms:
    doc_list = []
    for i, doc_tokens in enumerate(tokens):
        if term in doc_tokens:
            doc_list.append(f"{i+1}")
    inverted_index[term] = doc_list


for term, doc_list in inverted_index.items():
    print(f"{term} -> {', '.join(doc_list)}")


doc_count = len(documents)
print(process_query("( ( the AND lazy ) OR ( this AND NOT over ) )", inverted_index, doc_count))
