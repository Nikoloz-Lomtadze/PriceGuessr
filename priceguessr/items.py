from priceguessr.models import Items

class EbayItemProvider:
    def __init__(self,ebay_api):
        self.ebay_api = ebay_api
    def get_two_items(self,category=None):
        raw_items = self.ebay_api.search_items(category,10)
        if len(raw_items)<2:
            raise ValueError("there are less then 2 items that we get")
        first_raw_item = raw_items[0]
        second_raw_item = raw_items[1]
        
        first_item = self.convert_to_item(first_raw_item)
        second_item = self.convert_to_item(second_raw_item)
        return first_item,second_item

    def convert_to_item(self,raw_item):
        price_info = raw_item.get("price", {})
        image_info = raw_item.get("image", {})

        return Items(
            raw_item.get("itemId"),
            raw_item.get("title"),
            float(price_info.get("value", 0)),
            raw_item.get("categoryPath", "unknown"),
            image_info.get("imageUrl", "")
        )