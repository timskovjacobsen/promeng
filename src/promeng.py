from typing import List, Union, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class StockKeepingUnit:
    id_: str
    price: float


class PromotionInterface(ABC):
    """Interface class for various types of promotions."""

    @abstractmethod
    def apply(self, skus: List[StockKeepingUnit]) -> float:
        """Apply a promotion."""
        pass


@dataclass
class PromotionByQuantity(PromotionInterface):
    sku: StockKeepingUnit
    quantity: int
    price: float

    def apply(self, skus: List[StockKeepingUnit]) -> float:
        pass


class PromotionByVariety:

@dataclass
class PromotionByVariety(PromotionInterface):
    skus: List[StockKeepingUnit]
    price: float

    def apply(self, skus: List[StockKeepingUnit]) -> float:
        pass


@dataclass
class CartItem:
    sku: StockKeepingUnit
    quantity: int

    @property
    def id_(self):
        return self.sku.id_


class Cart:
    def __init__(self, items: List[CartItem] = None):
        if not items:
            self.items = []
        else:
            self.items = items

        # Create a dictionary for easy accessing via SKU ID
        self._items_dict = {cartitem.id_: cartitem for cartitem in self.items}

    def __getitem__(self, id_: str) -> CartItem:
        return self._items_dict[id_]


@dataclass
class CurrentPromotions:
    promotions: List[Union[PromotionByQuantity, PromotionByVariety]]


@dataclass
class Checkout:
    cart: Cart
    current_promotions: Optional[CurrentPromotions] = None
