from src.business.pagination_work.start_pagination_work import next_page_btn
from src.business.save_changes.start_save_changes import save_changes
from src.business.tasks.promo_work.change_count_for_page.change_count_for_page_ import change_count_for_page
from src.business.tasks.promo_work.page_work_promo.get_all_products_rows.get_all_products_rows_ import \
    get_all_products_rows
from src.business.iter_products.iter_products_bs import IterProductsBS
from src.utils.utils_decorators import catch_and_report


class StartPageWorkPromoBS:
    def __init__(self, settings):
        self.settings = settings
        self.driver = settings["driver"]
        self.task = settings["task"]
        self.id_client = settings["id_client"]
        self.promos = settings["promos"]
        self.data_promo = settings["data_promo"]
        self.cabinet = settings["cabinet"]

    @catch_and_report('Start Work BS')
    async def start_work(self):
        all_product_history = []
        count_page = 1
        total_changes_count = 0

        while True:
            await change_count_for_page({"driver": self.driver})
            rows = await get_all_products_rows(self.settings)
            html = self.driver.page_source

            work_from_products = await IterProductsBS(self.settings).start_work(html, rows)
            products_history = work_from_products.get("products_history", [])
            all_product_history.extend(products_history)
            is_change = work_from_products.get("is_change", False)
            changes_count = work_from_products.get("changes_count", 0)
            total_changes_count += changes_count

            if is_change:
                await save_changes(self.settings)

            next_page = await next_page_btn(self.settings)
            if not next_page:
                return {
                    "products_history": all_product_history,
                    "changes_count": total_changes_count,
                }
            count_page += 1
            continue

        return {
            "products_history": all_product_history,
            "changes_count": total_changes_count,
        }
