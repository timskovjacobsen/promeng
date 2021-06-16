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


def test_PromotionsByQuantity_apply_method():
    # ---- Setup ----
    A = StockKeepingUnit(id_="A", price=50)
    B = StockKeepingUnit(id_="B", price=50)

    # ---- Execute -----
    promotion = PromotionByQuantity(sku=A, quantity=3, price=130)

    # ---- Verify -----
    actual = promotion.apply(skus=[A, A, B, B, A, A, A, B, B, A, A])
    expected = 2 * 130 + 1 * 50

    assert actual == expected


def test_PromotionByVariety_apply_method():
    # ---- Setup ----
    A = StockKeepingUnit(id_="A", price=50)
    C = StockKeepingUnit(id_="C", price=20)
    D = StockKeepingUnit(id_="D", price=15)

    # ---- Execute -----
    promotion = PromotionByVariety(promo_ids={"C", "D"}, price=30)

    # ---- Verify -----
    actual = promotion.apply(skus=[A, C, D, A, C, D, D])
    expected = 50 + 0 + 30 + 50 + 0 + 30 + 15

    assert actual == expected
