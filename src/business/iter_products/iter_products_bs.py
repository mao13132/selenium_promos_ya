from src.business.analyser_click_product.analyser_click_product_ import analyser_click_product
from src.business.tasks.promo_work.page_work_promo.extract_info_by_product.extract_info_by_product_bs import \
    extract_info_list_by_html
from src.business.action_go.action_go_ import action_go
from src.business.iter_products.activate_element_ import activate_element
from src.utils.utils_decorators import catch_and_report


class IterProductsBS:
    def __init__(self, settings):
        self.settings = settings
        self.driver = settings["driver"]
        self.task = settings["task"]
        self.id_client = settings["id_client"]
        self.promos = settings["promos"]
        self.data_promo = settings["data_promo"]
        self.cabinet = settings["cabinet"]
        self.percent_list = settings["percent_list"]

    @catch_and_report('Парсинг html')
    async def start_work(self, html, rows):
        products_history = []
        is_change = False
        changes_count = 0

        products_data = extract_info_list_by_html(html)
        to_click = []

        for data_product in products_data:
            need_click = await analyser_click_product(
                {"data_product": data_product, "percent_list": self.percent_list}
            )
            products_history.append(data_product)
            if not need_click:
                continue
            action = need_click["action"]
            idx = data_product["count_product"]
            to_click.append({"idx": idx, "action": action, "data_product": data_product})

        for item in to_click:
            idx = item["idx"]
            try:
                product = rows[idx]
            except:
                continue
            activate_element(self.driver, product)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
            item["data_product"]["action"] = item["action"]
            res_action_work = await action_go(
                {
                    "driver": self.driver,
                    "product": product,
                    "action": item["action"],
                    "data_product": item["data_product"],
                }
            )
            if res_action_work:
                is_change = True
                changes_count += 1

        return {
            "is_change": is_change,
            "products_history": products_history,
            "changes_count": changes_count,
        }
