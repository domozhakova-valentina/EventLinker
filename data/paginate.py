class Pagination:
    def __init__(self, query, page, per_page=20):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.previous_page_number = page - 1
        self.next_page_number = page + 1
        total_count = self.query.order_by(None).count()
        self.num_pages = total_count // self.per_page + (total_count % self.per_page > 0)
        self.pages_range = range(1, self.num_pages + 1)  # диапазон кол-во страниц

    def items(self):
        """Информация страницы"""
        return self.query.limit(self.per_page).offset((self.page - 1) * self.per_page).all()

    def has_previous(self):
        """Проверка: есть ли перед страницей ещё страница"""
        return self.page > 1

    def has_next(self):
        """Проверка: есть ли после странице ещё страница"""
        total_count = self.query.order_by(None).count()
        return self.page < (total_count // self.per_page + (total_count % self.per_page > 0))