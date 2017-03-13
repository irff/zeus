from zeus.models import Category


class CategoryService:

    def get_categories(self):
        categories = Category.objects().only('name').all()
        list_category = []

        for category in categories:
            list_category.append(category.name)
        return list_category

    def get_or_create(self, name):
        category = Category.objects(name=name).first()
        if category is None:
            category = Category(name=name)
            category.save()
        return category