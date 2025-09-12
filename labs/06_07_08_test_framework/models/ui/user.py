# View where an user (non admin) can Choose
# produts from the Product Catalog and/or
# remove it


class UserPage:
    def __init__(self, page):
        self.page = page
        self.logout_button = page.get_by_role("button").and_(page.get_by_text("Logout"))
        # page_(element-type)_(descriptive-name)
        # complete code

    def get_user_products(self):  # denna kan jag göra.
        # complete code
        pass

    def add_product_to_user(self, product_name):
        # complete code
        pass

    def remove_product_from_user(self, product_name):
        # complete code
        pass

    def logout(self):
        self.logout_button.click()
