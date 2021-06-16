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
    promotion2 = PromotionByQuantity(sku=skus[1], quantity=2, price=45)
    promotion3 = PromotionByVariety(promo_ids={"C", "D"}, price=130)

    current_promotions = CurrentPromotions([promotion1, promotion2, promotion3])

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


def test_PromotionByQuantity_apply_method():
    # ---- Setup ----
    A = StockKeepingUnit(id_="A", price=50)
    B = StockKeepingUnit(id_="B", price=30)

    # ---- Execute -----
    promotion = PromotionByQuantity(sku=A, quantity=3, price=130)

    promo_skus, _ = promotion.filter([A, A, B, B, A, A, A, B, B, A, A])

    # ---- Verify -----
    actual = promotion.apply(skus=promo_skus)
    expected = 2 * 130

    assert actual == expected


def test_PromotionByQuantity_filter_method():
    # ---- Setup ----
    A = StockKeepingUnit(id_="A", price=50)
    C = StockKeepingUnit(id_="C", price=20)
    D = StockKeepingUnit(id_="D", price=15)

    promotion = PromotionByQuantity(sku=A, quantity=3, price=130)

    # ---- Execute -----
    actual_promos, actual_non_promos = promotion.filter(skus=[A, C, A, A, A, D, D])

    # ---- Verify -----
    expected_promos, expected_non_promos = [A, A, A], [C, A, D, D]

    assert actual_promos == expected_promos
    assert actual_non_promos == expected_non_promos


def test_PromotionByQuantity_filter_method2():
    # ---- Setup ----
    A = StockKeepingUnit(id_="A", price=50)
    B = StockKeepingUnit(id_="B", price=50)
    promotion = PromotionByQuantity(sku=A, quantity=3, price=130)

    # ---- Execute -----
    actual_promos, actual_non_promos = promotion.filter(
        skus=[A, A, B, B, A, A, A, B, B, A, A]
    )

    # ---- Verify -----
    expected_promos, expected_non_promos = [A, A, A, A, A, A], [B, B, B, B, A]

    assert actual_promos == expected_promos
    assert actual_non_promos == expected_non_promos


def test_PromotionByVariety_apply_method():
    # ---- Setup ----
    A = StockKeepingUnit(id_="A", price=50)
    C = StockKeepingUnit(id_="C", price=20)
    D = StockKeepingUnit(id_="D", price=15)

    # ---- Execute -----
    promotion = PromotionByVariety(promo_ids={"C", "D"}, price=30)

    promo_skus, _ = promotion.filter(skus=[A, C, D, A, C, D, D])

    print(promo_skus)

    # ---- Verify -----
    actual = promotion.apply(skus=promo_skus)
    expected = 0 + 30 + 0 + 30

    assert actual == expected
