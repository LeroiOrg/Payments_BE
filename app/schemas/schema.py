import strawberry
from .payment_schema import PaymentMutation
from .transaction_schema import TransactionMutation


# -----------------------------
# 📌 Query base
# -----------------------------
@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"


# -----------------------------
# 📌 Mutations raíz
# -----------------------------
@strawberry.type
class Mutation(PaymentMutation, TransactionMutation):
    pass


# -----------------------------
# 📌 Schema principal
# -----------------------------
schema = strawberry.Schema(query=Query, mutation=Mutation)