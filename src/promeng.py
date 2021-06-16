from typing import List, Union, Optional, Set, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
from itertools import zip_longest


@dataclass
class StockKeepingUnit:
    id_: str
    price: float


class PromotionInterface(ABC):
    """Interface class for various types of promotions."""

    @abstractmethod
    def apply(self, skus: List[StockKeepingUnit]) -> float:
        """Return the total price of SKUs after they received a promotion."""
        pass

    @abstractmethod
    def filter(self, skus: List[StockKeepingUnit]) -> Tuple[StockKeepingUnit]:
        """Return the SKUs that are part of the promotion and not, respectively."""
        pass


@dataclass
class PromotionByQuantity(PromotionInterface):
    sku: StockKeepingUnit
    quantity: int
    price: float

    def filter(self, skus: List[StockKeepingUnit]) -> Tuple[StockKeepingUnit]:
        """Return the SKUs that are part of the promotion and not, respectively."""
        # Get the count of the SKUs mathching the ID of this promotion
        ids = [sku.id_ for sku in skus]
        id_count = ids.count(self.sku.id_)

        # Extract all SKUs that can be part of the promotion
        promotion_skus, non_promotion_skus = [], []
        no_of_discount_ids = id_count - (id_count % self.quantity)
        count = 0
        for sku in skus:
            if sku.id_ == self.sku.id_ and count < no_of_discount_ids:
                # ID fits and there is still room in the promotion
                promotion_skus.append(sku)
                count += 1
            else:
                non_promotion_skus.append(sku)

        return promotion_skus, non_promotion_skus

    def apply(self, skus: List[StockKeepingUnit]) -> float:
        # We can assume that all "skus" are valid and a multiplum of self.quantity
        return len(skus) / self.quantity * self.price


@dataclass
class PromotionByVariety(PromotionInterface):
    promo_ids: Set[str]
    price: float

    def filter(self, skus: List[StockKeepingUnit]) -> Tuple[StockKeepingUnit]:
        """Return the SKUs that are part of the promotion and not, respectively."""

        # If an ID is not among the promo IDs, regular price applies
        non_promotion_skus = [sku for sku in skus if sku.id_ not in self.promo_ids]

        # If an ID is among the promo IDs, it must be tested if it can be paired w/
        # all IDs that are part of the promotion
        promos = {}
        for promo_id in self.promo_ids:
            promos[promo_id] = [sku for sku in skus if sku.id_ == promo_id]

        promotion_skus = []
        for tup in zip_longest(*promos.values()):
            if None in tup:
                # Some id(s) are missing for a valid promotion, thus no discount for
                # any of the SKUs
                for sku in tup:
                    if sku is not None:
                        non_promotion_skus.append(sku)
            else:
                # All ids are present for the promotion, apply the discounted price
                for sku in tup:
                    promotion_skus.append(sku)

        return promotion_skus, non_promotion_skus

    def apply(self, skus: List[StockKeepingUnit]) -> float:
        # We can assume that all items in "skus" are valid promotion pairs
        return self.price * len(skus) / len(self.promo_ids)


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
