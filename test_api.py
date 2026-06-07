from Config import EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_ENVIRONMENT
from priceguessr.ebay_api import EbayApi
from priceguessr.items import EbayItemProvider


api = EbayApi(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_ENVIRONMENT)
provider = EbayItemProvider(api)

left_item, right_item = provider.get_two_items("keyboard")

print("LEFT ITEM")
print(left_item.id)
print(left_item.name)
print(left_item.price)
print(left_item.category)
print(left_item.image_url)

print()

print("RIGHT ITEM")
print(right_item.id)
print(right_item.name)
print(right_item.price)
print(right_item.category)
print(right_item.image_url)