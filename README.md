# 4111_project

1. PostgreSQL account name:
yx2622

2. URL:
http://34.138.157.148:8080/

3. ALL of features mentioned in Part1 have been implemented.
    - Login and register functions.
    - Edit user profile including telephone number and building name that user lives in
    - Search keywords, choose categories and choose whether 'goods in your building' 
    or not to filter the goods in the index page.
    - Post new second-hand-goods to sell or auction.
    - Cancel posted goods or auctions and make them off shelf.
    - Buy others' second-hand-goods at fixed price or join auctions.
    - Write reviews to sellers after making an order.
    
4. Webpages:
  - Index page: In the index pages, the main page displaying all the second-hand goods on sale or on auction. When entering the webpage, 'SELECT' is used to get all the entities from 'Second_hand_good' table with 'state' of the good being '1'(on sale) or '2'(on auction). Also, there are multiple choices for users to get the goods they want to see:
    * Category menu bar: Allow user to search goods with certain category selection by connecting tables Goods_Category and Second_hand_good to find the good according to the good_id and category.
    * Search box: Allow user to search key words of the goods by using the 'LIKE' to find the key words in the 'description' of the good.
    * Price range selection: Allow user to find goods with price less than $20 or greater than $20 by using the 'price' attribute in the TABLE Second_hand_good.
    * Same apartment button: It allows users to find sellers who live in the same building as you. It connect TABLE User and Second_hand_good to find the sellers whose apartment is the same with the user's.

  - Posting good page: In this page, a user can post a good for sale or auction. The inputs on this page including price, category,image and description of the good. If the user choose to create an auction, the inputs will also include auction time and start price. The server use these inputs to insert an entity into table Second_hand_good, with ```state``` set to 1 (on sale) or 2 (on auction). The product image file will be first saved in server and its file path will then be inserted in database. If this new good is for auction, server will also insert a new weak entity into table Auctions whose attributes include current max price, auction start time, last hours and state. Before each request, if the server finds any auctions in database whose start time plus last hours is less than the current time, server will set these auction state to 3(auction done) and create orders for the users who offer the max price.  
  We find this page interesting because it uploads image files to the server and the server needs to interact with database in different ways for creating sale and auction.

5. AJAX calls:
    - POST ```/register```: It is called in the register page to create a new user in database.
    - POST ```/login```: It is called in the login page to pass input email and password to the server.
    - GET ```/good```: It is triggered in the index page and good page. The server return the information of filtered goods.
    - POST ```/buy```: It is triggered in good page when a user click the 'Buy now' button. The server creates an order for this user and then update the state of this product as 'Sold out'.
    - POST ```/sell```: It is triggered in the page for posting a new good for sale or auction. It uploads information of good given by the seller including price, product image,description, auction time and so on.
    - POST ```/auction```: It is triggered in good page. It passes the price offered by a user for an auction.
    - DELETE ```/signout```: It is trigger by clicking the 'sign out' button and called to delete the cookie in the frontend and session in backend.
    - GET and POST ```/review```: GET is used to show all the reviews to a certain user. POST is used to post reviews to the sellers, whose good was bought by the user.
    - GET ```/order```: It is used to get the goods the user bought before.
    - GET and POST ```/user```: GET is used to show a certain user's information. POST is triggered when the user edits his info. POST passes the new user information to the server.
    - POST ```/offshelf```: It is used to offshelf the goods seller put on the market by shifting the 'state' of the goods.
    - GET ```/soldgoods```: It is used to get the goods sellers sold before.
    - GET ```/auctions```: It is trigger by clicking the 'My Auctions' button and called to view the auctions you are now participating in.

