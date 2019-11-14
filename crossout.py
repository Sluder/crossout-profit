import requests
from operator import getitem


class CrossoutApi:
    URL = "https://crossoutdb.com/api/v1"

    def get_items(self):
        return requests.get("{}/{}".format(self.URL, "items")).json()


if __name__ == "__main__":
    api = CrossoutApi()
    interests_craft = {}
    interests_buy = {}

    # Grab interesting parts
    for item in api.get_items():
        if (item['craftVsBuy'] == 'Craft') and item['faction'] is not None:
            sell = float(item['formatBuyPrice']) - (float(item['formatBuyPrice']) * 0.1)

            interests_craft[item['name']] = {
                'craft_in': "{} ({})".format(item['faction'], item['rarityName']),
                'sell_for': round(sell, 2),
                'craft_sell': float(item['formatCraftingBuySum']),
                'profit': round(sell - float(item['formatCraftingBuySum']), 2)
            }
        if item['rarityName'] is not None and (float(item['formatSellPrice']) != 0.0) and (float(item['formatBuyPrice']) > float(item['formatSellPrice'])):
            interests_buy[item['name']] = {
                'rarity': item['rarityName'],
                'buy_for': float(item['formatSellPrice']),
                'sell_for': float(item['formatBuyPrice']),
                'profit': round(float(item['formatBuyPrice']) - float(item['formatSellPrice']), 2)
            }

    # Output results
    print("-" * 104)
    print("Craft - Sell")
    print("{:<25} {:>30} {:>15} {:>15} {:>15}".format("Item Name", "Faction", "Part Price", "Sell Price", "Profit"))
    print("-" * 104)

    if bool(interests_craft):
        for name, item in sorted(interests_craft.items(), key=lambda x: getitem(x[1], 'profit'), reverse=True):
            print("{:<25} {:>30} {:>15} {:>15} {:>15}".format(name, item['craft_in'], item['craft_sell'], item['sell_for'], item['profit']))
    else:
        print('No items for crafting & selling')

    print("\n" + ("-" * 104))
    print("Buy - Sell")
    print("{:<25} {:>15} {:>15} {:>15} {:>15}".format("Item Name", "Rarity", "Buy For", "Sell For", "Profit"))
    print("-" * 104)

    if bool(interests_buy):
        for name, item in sorted(interests_buy.items(), key=lambda x: getitem(x[1], 'profit'), reverse=True):
            print("{:<25} {:>15} {:>15} {:>15} {:>15}".format(name, item['rarity'], item['buy_for'], item['sell_for'], item['profit']))
    else:
        print('No items for flipping')
