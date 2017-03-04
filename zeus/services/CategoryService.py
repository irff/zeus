from zeus.models import Category


class CategoryService:

    def get_categories(self):
        categories = Category.objects().only('name').all()
        return categories
