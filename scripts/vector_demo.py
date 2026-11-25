from app.vector_store import add_texts, ensure_collection, search

FAQS = [
    "Refunds are processed back to the original payment method.",
    "A partial refund returns only part of the payment amount to the customer.",
    "Failed payments are usually reversed automatically by the bank.",
    "Settlements move collected payments into the merchant's bank account.",
    "You can view all transactions in the dashboard under Payments.",
    "API keys can be regenerated from the account settings page.",
    "Test mode lets you try payments without moving real money.",
    "Webhooks notify your server when a payment succeeds or fails.",
    "Customers can pay using UPI, cards, netbanking, or wallets.",
    "Disputes are raised when a customer questions a charge with their bank.",
]

ensure_collection()
add_texts(FAQS)
print(f"Indexed {len(FAQS)} texts. Ask a question, or press Enter to quit.\n")

while True:
    question = input("Question: ").strip()
    if not question:
        break
    for hit in search(question):
        print(f"  {hit['score']:.3f}  {hit['text']}")
    print()