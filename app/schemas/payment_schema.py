import strawberry
from typing import Optional, List
from app.services.payment_service import MercadoPagoService

mp_service = MercadoPagoService()


# -----------------------------
# 📌 Tipos
# -----------------------------
@strawberry.type
class ItemType:
    title: str
    quantity: int
    unit_price: float
    currency_id: Optional[str]


@strawberry.type
class PayerType:
    email: Optional[str] = None
    name: Optional[str] = None


@strawberry.type
class Payment:
    id: str
    init_point: Optional[str]
    sandbox_init_point: Optional[str]
    external_reference: Optional[str]
    items: Optional[List[ItemType]]
    payer: Optional[PayerType]
    date_created: Optional[str]


# -----------------------------
# 📌 Inputs
# -----------------------------
@strawberry.input
class ItemInput:
    title: str
    quantity: int
    unit_price: float
    currency_id: Optional[str] = "ARS"


@strawberry.input
class PreferenceInput:
    items: List[ItemInput]
    external_reference: Optional[str] = None


# -----------------------------
# 📌 Mutations
# -----------------------------
@strawberry.type
class PaymentMutation:
    @strawberry.mutation
    def create_preference(self, input: PreferenceInput) -> Payment:
        pref_data = {
            "items": [item.__dict__ for item in input.items],
            "external_reference": input.external_reference,
            "auto_return": "approved",
            "back_urls": {
                "success": "https://miapp.com/success",
                "failure": "https://miapp.com/failure",
                "pending": "https://miapp.com/pending",
            }
        }

        resp = mp_service.create_preference(pref_data)
        pref = resp["response"]

        return Payment(
            id=pref["id"],
            init_point=pref.get("init_point"),
            sandbox_init_point=pref.get("sandbox_init_point"),
            external_reference=pref.get("external_reference"),
            items=[
                ItemType(
                    title=i["title"],
                    quantity=i["quantity"],
                    unit_price=i["unit_price"],
                    currency_id=i.get("currency_id")
                )
                for i in pref.get("items", [])
            ],
            payer=PayerType(
                email=pref.get("payer", {}).get("email"),
                name=pref.get("payer", {}).get("name")
            ) if pref.get("payer") else None,
            date_created=pref.get("date_created"),
        )
