import psycopg2
from connection_pool import engine,Session
from models import *
from data.users_data import users
from data.auctions_data import auctions
from data.categories_data import categories
from data.buildings_data import buildings
from data.goods_category import goods_categories
from data.goods_data import goods
from data.orders import orders
from data.reviews_data import reviews
from data.participate_auction import participate_auction


with Session(engine) as session:
    # new_building = []
    # for building in buildings:
    #     new_building.append(Apartment_building(name=building['name'],address=building['address'],
    #                         zip_code=building['zip_code'],street_name=building['street_name']))
    # session.add_all(new_building)
    # session.commit()

    # new_users = []
    # for user in users:
    #     new_users.append(Users(username=user['username'], password=user['password'],
    #                           email=user['email'], telephone=user['telephone'], building_name=user['building_name']))
    # session.add_all(new_users)
    # session.commit()

    # new_goods = []
    # for good in goods:
    #     new_goods.append(Second_hand_goods(state=good['state'], price=good['price'],email=good['email'],
    #                             description=good['description'], image_url=good['image_url']))
    # session.add_all(new_goods)
    # session.commit()
    #
    # new_auctions = []
    # for auction in auctions:
    #     new_auctions.append(Auctions(good_id=auction['good_id'],count_down=auction['count_down'],
    #                         max_price=auction['max_price'],state=auction['state']))
    # session.add_all(new_auctions)
    # session.commit()
    #
    # new_participation_auction = []
    # for pa in participate_auction:
    #     new_participation_auction.append(Participate_Auction(email=pa['email'],good_id=pa['good_id'],
    #                         price=pa['price']))
    # session.add_all(new_participation_auction)
    # session.commit()
    #
    # new_category = []
    # for category in categories:
    #     new_category.append(Category(name = category['name']))
    # session.add_all(new_category)
    # session.commit()
    #
    # new_good_category = []
    # for good_category in goods_categories:
    #     new_good_category.append(Goods_Category(name=good_category['name'], good_id = good_category['good_id']))
    # session.add_all(new_good_category)
    # session.commit()
    #
    # new_order = []
    # for order in orders:
    #     new_order.append(Orders(total_price = order['total_price'], email = order['email'], good_id = order['good_id']))
    # session.add_all(new_order)
    # session.commit()
    #
    new_review = []
    for review in reviews:
        new_review.append(Reviews(content = review['content'], writer_email = review['writer_email'], receiver_email = review['receiver_email']))
    session.add_all(new_review)
    session.commit()

    result = session.execute("select * from users;").fetchall()

print(result)