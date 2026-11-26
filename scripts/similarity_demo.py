import numpy as np

from app.embeddings import embed_documents, embed_query

query = "How do I get my money back?"

documents = [
    "Refunds are sent to the customer's original payment method.",
    "You can cancel an order before it is shipped.",
    "To reset your password, click Forgot Password on the login page.",
    "Settlements are transferred to your bank account on a schedule.",
    "Our office has a cafeteria on the third floor.",
]

q = np.array(embed_query(query))
docs = np.array(embed_documents(documents))

print(f"One embedding has {len(q)} numbers. First five: {q[:5]}\n")


scores = docs @ q

print(scores)

for score, text in sorted(zip(scores, documents), reverse=True):
    print(f"{score:.3f}  {text}")