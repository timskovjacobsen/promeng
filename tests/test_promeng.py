from src.promeng import (
    Cart,
    Checkout,
    PromotionByQuantity,
    PromotionByVariety,
    CurrentPromotions,
    StockKeepingUnit,
    CartItem,
)


def test_scanrioA():
    # ---- Setup ----
    products = {"A": 50, "B": 30, "C": 20, "D": 15}

    skus = [StockKeepingUnit(id_=i, price=p) for i, p in products.items()]

    # ---- Execute -----
    promotion1 = PromotionByQuantity(sku=skus[0], quantity=3, price=130)
    promotion2 = PromotionByVariety(skus=[skus[2], skus[3]], price=130)

    current_promotions = CurrentPromotions([promotion1, promotion2])

    cart_items = [
        CartItem(skus[0], quantity=1),
        CartItem(skus[1], quantity=1),
        CartItem(skus[2], quantity=1),
    ]
    cart = Cart(items=cart_items)
    checkout = Checkout(cart, current_promotions)

    # ---- Verify -----
    actual = checkout.total_order_price()
    expected = 100

    assert actual == expected
