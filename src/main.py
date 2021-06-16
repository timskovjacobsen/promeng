if __name__ == "__main__":

    from promeng import StockKeepingUnit, ProductCatalog, CartItem, PromotionByVariety

    # import promeng

    A = StockKeepingUnit(id_="A", price=50)
    B = StockKeepingUnit(id_="B", price=30)
    catalog = ProductCatalog(skus=[A, B])
    cartitem = CartItem(sku=A, quantity=3)

    promotion2 = PromotionByVariety(skus=[A, B], price=130)

    print(A)
    print(catalog)
    print(cartitem)
