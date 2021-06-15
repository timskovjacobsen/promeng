from typing import List
from dataclasses import dataclass


@dataclass
class StockKeepingUnit:
    id_: str
    price: float


@dataclass
class PromotionByQuantity:
    sku: StockKeepingUnit
    quantity: int
    price: float


class PromotionByVariety:
    skus: List[StockKeepingUnit]
    price: float

