from bs4 import BeautifulSoup


def _has_class_contains(tag, needle):
    classes = tag.get("class", [])
    if isinstance(classes, str):
        classes = [classes]
    return any(needle in c for c in classes)


def _get_name(tr):
    el = tr.find(lambda t: t.name and _has_class_contains(t, "nameCategoryCol"))

    name = el.get_text(strip=True) if el else ""

    return name


def _get_stocks(tr):
    el = tr.select_one("[data-e2e*='stock-total-count']")
    if not el:
        el = tr.find(
            lambda t: t.has_attr("data-e2e")
            and "stock" in str(t["data-e2e"]).lower()
            and "empty" in str(t["data-e2e"]).lower()
        )
    if not el:
        return 0
    text = el.get_text(strip=True)
    if "нет на складе" in text.lower():
        return 0
    try:
        return int(text)
    except:
        return 0


def _get_price_by_catalog(tr):
    el = tr.select_one("[data-zone-name*='merchPrice']")

    price = el.get_text(strip=True) if el else 0

    return price


def _get_price_sale(tr):
    inp = tr.select_one("[data-e2e*='price-text'] input") or tr.select_one("input[data-e2e*='price-text']")
    if not inp:
        container = tr.find(
            lambda t: t.has_attr("data-e2e")
            and "price-text" in str(t.get("data-e2e")).lower()
        )
        if not container:
            container = tr.find(
                lambda t: any(
                    isinstance(k, str)
                    and k.lower().startswith("data-e2e")
                    and (
                        ("price-text" in str(v).lower())
                        if not isinstance(v, (list, tuple))
                        else any("price-text" in str(x).lower() for x in v)
                    )
                    for k, v in (t.attrs or {}).items()
                )
            )
        if not container:
            container = tr.find(
                lambda t: t.has_attr("data-zone-name")
                and "merchprice" in str(t.get("data-zone-name")).lower()
            )
        if container:
            inp = container.find("input") or container.select_one("input[type='text'], input[type='number']")
    if not inp:
        return 0
    price = inp.get("value") or inp.get("aria-valuenow") or 0
    return price


def _get_old_price(tr):
    inp = tr.select_one("[data-e2e*='old-price-text'] input") or tr.select_one("input[data-e2e*='old-price-text']")
    if not inp:
        container = tr.find(
            lambda t: t.has_attr("data-e2e")
            and "old-price-text" in str(t.get("data-e2e")).lower()
        )
        if not container:
            container = tr.find(
                lambda t: any(
                    isinstance(k, str)
                    and k.lower().startswith("data-e2e")
                    and (
                        ("old-price-text" in str(v).lower())
                        if not isinstance(v, (list, tuple))
                        else any("old-price-text" in str(x).lower() for x in v)
                    )
                    for k, v in (t.attrs or {}).items()
                )
            )
        if not container:
            container = tr.find(
                lambda t: t.has_attr("data-zone-name")
                and "oldprice" in str(t.get("data-zone-name")).lower()
            )
        if container:
            inp = container.find("input") or container.select_one("input[type='text'], input[type='number']")
    if not inp:
        return 0
    old_price = inp.get("value") or inp.get("aria-valuenow") or 0
    return old_price


def _get_percent(tr):
    el = tr.select_one("[data-e2e*='promo-discount']")
    if not el:
        return 0
    text = el.get_text(strip=True)
    try:
        percent = int(text.rstrip("%"))
    except:
        return 0

    return percent


def _get_select(tr):
    inputs = tr.select("td input[type='checkbox']")
    if not inputs:
        inp = tr.find("input", attrs={"type": "checkbox"})
        if not inp:
            return False
        inputs = [inp]
    for inp in inputs:
        if "checked" in inp.attrs:
            return True
        val = str(inp.get("checked", "")).lower()
        aria = str(inp.get("aria-checked", "")).lower()
        if val in ("true", "checked") or aria == "true":
            return True
    return False


def extract_info_list_by_html(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table tbody tr")
    products = []
    for idx, tr in enumerate(rows):
        data = {
            "count_product": idx,
            "select": _get_select(tr),
            "name": _get_name(tr),
            "stocks": _get_stocks(tr),
            "catalog_price": _get_price_by_catalog(tr),
            "price_salle": _get_price_sale(tr),
            "percent": _get_percent(tr),
            "old_price": _get_old_price(tr),
            "action": "",
        }
        products.append(data)
    return products
