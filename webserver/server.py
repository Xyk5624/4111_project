
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
import re
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, flash, session, make_response
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
CORS(app, supports_credentials=True)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@xxx.xxx.xxx.xxx/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@xxx.xxx.xxx.xxx/proj1part2"
#
DATABASEURI = ""


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


def handle_auction():
  ids = g.conn.execute("""
    UPDATE auctions SET state = 3 
    where Start_Time + (''||count_down||' hours')::interval  < current_timestamp 
    and state = 1 returning auction_id,good_id,max_price""").fetchall()
  for auction_id,good_id,max_price in ids:
    email = g.conn.execute("""
      SELECT email
      FROM participate_auction
      WHERE price = %s AND good_id = %s""",max_price,good_id).fetchall()
    if len(email) == 0:
      g.conn.execute("""
        UPDATE second_hand_goods
        SET state = 4
        WHERE good_id = %s""",good_id)
    else:
      g.conn.execute("""
        UPDATE second_hand_goods
        SET state = 3
        WHERE good_id = %s""",good_id)
      g.conn.execute("""
        INSERT INTO orders
        (total_price,email,good_id)
        VALUES (%s,%s,%s)
        """,max_price,email[0][0],good_id)
      
  
@app.before_request
def before_request():
#   """
#   This function is run at the beginning of every web request 
#   (every time you enter an address in the web browser).
#   We use it to setup a database connection that can be used throughout the request.

#   The variable g is globally accessible.
#   """
  try:
    g.conn = engine.connect()
    g.conn.execute("SET TIME ZONE 'posix/America/Montreal'")
    handle_auction()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/', methods=["GET"])
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

  """

  # DEBUG: this is debugging code to see what request looks like
  print("request.args: ", request.args)


  #
  # example of a database query
  #
  # cursor = g.conn.execute("SELECT name FROM test")
  # names = []
  # for result in cursor:
  #   names.append(result['name'])  # can also be accessed using result[0]
  # cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  # context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def post():
  return render_template("another.html")


# Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
#   name = request.form['name']
#   g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
#   return redirect('/')
@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    telephone = int(request.form['telephone'])
    apartment = request.form['apartment']
    error = None
    
    if not username:
      error = "Please enter a username"
    elif not password:
      error = "Please enter a password"
    elif not email:
      error = "Please enter a email"
    elif not telephone:
      error = "Please enter a telephone"
    elif not apartment:
      error = "Please select a apartment" 

    if error is not None:
      resp = make_response(error, 401)
      return resp
          
    a = g.conn.execute("SELECT COUNT(*) FROM Users WHERE Email=(%s)", email)
    res = a.fetchall()[0][0]
    if res > 0:
      error = "The email has been registered."
      resp = make_response(error, 401)
      return resp
      
    if error is None:
      g.conn.execute('INSERT INTO Users (Username, Password_Encrypted, Email, Telephone, Building_name) VALUES (%s, %s, %s, %s, %s)', username, generate_password_hash(password), email, telephone, apartment)

      resp = make_response("success", 200)
      return resp
      
    resp = make_response(error, 401)
    return resp


@app.route('/good', methods=["GET"])
def good():
  category = request.args.get('category')
  search = request.args.get('search')
  good_id = request.args.get('good_id')
  building = request.args.get('building')
  price = request.args.get('price')
  from_sql = ""
  where_clau = " WHERE "
  where_cond = " WHERE (G.state = 1 OR G.state = 2) "
  state_sql = " AND (G.state = 1 OR G.state = 2)"
  error = None

  sql_query = "SELECT G.image_url, G.description, G.good_id FROM Second_hand_Goods G"

  if good_id is not None:
    good_info = g.conn.execute('SELECT state, price, description, email, image_url FROM Second_hand_Goods WHERE good_id = (%s)', good_id).fetchall()
    dic = {"state": good_info[0][0], "price": good_info[0][1], "description": good_info[0][2], "selleremail": good_info[0][3],"image_url": good_info[0][4]}   

    resp = make_response({"status":"success","message":error,"data":dic}, 200)
    return resp

  if category is not None and category != 'All':
    from_sql += ", Goods_Category C"
    where_cond += ' AND C.good_id = G.good_id AND C.name = \'' + category + '\''
  if search is not None:
    where_cond += " AND G.description LIKE \'%%"+  search + "%%\'"
  if price is not None and price != '0':
    if price == '1':
      where_cond += " AND G.price <= 20"
    elif price == '2':
      where_cond += " AND G.price > 20"
  if building is not None:
    from_sql += ", Users U"
    where_cond += " AND G.email = U.email AND U.building_name =\'" + building + "\'"

  sql_query += from_sql + where_cond

  try:
    good_info = g.conn.execute(sql_query).fetchall()
    dic = []
    for i in range(len(good_info)):
      dic.append({"imgurl": good_info[i][0], "description": good_info[i][1], "good_id": good_info[i][2]})

    resp = make_response({"status":"success","message":error,"data":dic}, 200)
    return resp
  except:
    resp = make_response({"status":"fail","message":error}, 401)
    return resp

@app.route('/buy', methods=["POST"])
def buy():
  error = ""
  email = request.cookies.get('user_email')
  good_id = int(request.form['good_id'])
  price = int(request.form['price'])

  res = g.conn.execute("""
  UPDATE Second_hand_Goods SET state = 3 
  WHERE good_id = %s and state = 1 returning good_id
  """,good_id).fetchone()
  if res == None:
    error = "Someone else has already bought this good..."
    resp = make_response({"status":"fail","message":error}, 401)
    return resp
  
  res = g.conn.execute("""
  INSERT INTO orders
  (total_price,email,good_id)
  VALUES (%s,%s,%s)
  """,price,email,good_id)
  resp = make_response({"status":"success","message":error}, 200)
  return resp

@app.route('/sell', methods=['POST'])
def sell():
  error = None
  if request.method == 'POST':
    email = request.form['email']
    sell_or_auction = request.form['state']
    price = int(request.form['price'])
    category = request.form['category']
    state = 1
    if sell_or_auction == "Auction":
      state = 2
      count_down = request.form['count_down']
    description = request.form['description']
    file = request.files['file']  
    type = file.filename.split('.')[1]
    
    try:
      ret = g.conn.execute("INSERT INTO Second_hand_Goods (state, price, description, email, image_url) VALUEs (%s, %s, %s, %s, %s)RETURNING good_id", state, price, description, email, "temporay").fetchone()

      good_id = ret[0]
      file.filename = good_id
      filepath = "./static/" + str(good_id) + "." + type
      file.save(filepath)
      imgurl = "/static/" + str(good_id) + "." + type

      g.conn.execute("UPDATE Second_hand_Goods SET image_url = %s WHERE good_id = %s", imgurl, good_id)

      if sell_or_auction == "Auction":
        g.conn.execute("INSERT INTO Auctions (count_down, good_id, max_price, state) VALUEs (%s, %s, %s, 1)", count_down, good_id, price)

      g.conn.execute("INSERT INTO goods_category (name, good_id) VALUES (%s, %s)", category, good_id)

      resp = make_response({"status":"success","message":error}, 200)
      return resp
    except:
      error = "Failure in insert data into database"
      resp = make_response({"status":"fail","message":error}, 401)
      return resp
  
  resp = make_response({"status":"success","message":error}, 200)
  return resp


@app.route('/soldgoods', methods=['GET'])
def soldgoods():
  if request.method == 'GET':
    email=request.cookies.get('user_email')
    error = "None"

    try:
      good_info = g.conn.execute("SELECT state, price, description, image_url, good_id FROM Second_hand_Goods WHERE email = %s", email).fetchall()
      dic = []
      for good in good_info:
        dic.append({"state": good[0], "price": good[1], "description": good[2], "image_url": good[3], "good_id": good[4]})

      resp = make_response({"status":"success","message":error,"data":dic}, 200)
      return resp
      
    except:
      error = "Failure in find goods"
      resp = make_response({"status":"fail","message":error}, 401)
      return resp


@app.route('/offshelf', methods=['POST'])
def offshelf():
  if request.method == 'POST':
    state = request.form['state']
    good_id = request.form['good_id']
    error = None

    try:
      g.conn.execute("UPDATE Second_hand_Goods SET state = '4' WHERE good_id = %s", good_id)
      
      if state == '2':
        g.conn.execute("UPDATE Auctions SET state = '2' WHERE good_id = %s", good_id)

      resp = make_response({"status":"success","message":error,}, 200)
      return resp
    except:
      error = "Failure in delete goods"
      resp = make_response({"status":"fail","message":error}, 401)
      return resp



@app.route('/auctions', methods=['GET'])
def auctions():
  if request.method == 'GET':
    email=request.cookies.get('user_email')
    error = "None"

    try:
      good_info = g.conn.execute("SELECT A.max_price, P.price, G.description, G.image_url, A.start_time, A.Start_Time + (''||A.count_down||' hours')::interval, G.good_id  FROM participate_auction P, Second_hand_Goods G, Auctions A WHERE P.email = (%s) AND G.state = 2 AND G.good_id = P.good_id AND A.good_id = P.good_id", email).fetchall()
      dic = []
      for good in good_info:
        dic.append({"maxprice": good[0], "offer_price": good[1],"description": good[2], "image_url": good[3], "start_time": good[4], "count_down": good[5], "good_id": good[6]})

      resp = make_response({"status":"success","message":error,"data":dic}, 200)
      return resp
      
    except:
      error = "Failure in find auctions"
      resp = make_response({"status":"fail","message":error}, 401)
      return resp

@app.route('/auction', methods=['GET', 'POST'])
def auction():
  if request.method == 'GET':
    good_id=int(request.args.get('good_id'))
    error = "None"

    try:
      res = g.conn.execute("""
      SELECT max_price, start_time, Start_Time + (''||count_down||' hours')::interval 
      FROM Auctions 
      WHERE good_id = %s""",good_id).fetchone()

      resp = make_response({"status":"success","message":error,"data":list(res)}, 200)
      return resp
      
    except:
      error = "Failure in find auction"
      resp = make_response({"status":"fail","message":error}, 401)
      return resp
  elif request.method == 'POST':
    email=request.cookies.get('user_email')
    good_id = request.form['good_id']
    offerprice = request.form['offerprice']
    try:
      res = g.conn.execute("SELECT 1 FROM Auctions WHERE good_id = %s AND state = 1", good_id).fetchone()
      if not res:
        error = "The auction is closed"
        resp = make_response({"status":"fail","message":error}, 401)
        return resp

      g.conn.execute("UPDATE Auctions SET max_price = %s WHERE good_id = %s", offerprice, good_id)
      g.conn.execute("UPDATE Second_hand_Goods SET price = %s WHERE good_id = %s", offerprice, good_id)

      partipate = g.conn.execute("SELECT email FROM participate_auction WHERE good_id = %s AND email = %s", good_id, email).fetchone()

      if not partipate:
        g.conn.execute("INSERT INTO participate_auction (email, good_id, price) VALUES (%s, %s, %s)", email, good_id, offerprice)
      else:
        g.conn.execute("UPDATE participate_auction SET price = %s WHERE good_id = %s AND email = %s", offerprice, good_id, email)
    except:
      error = "Failure in participate auction"
      resp = make_response({"status":"fail","message":error}, 401)
      return resp
    
    resp = make_response({"status":"success","message":""}, 200)
    return resp

      


@app.route('/login', methods=["GET", "POST"])
def login():
  if request.method == 'POST':
    password = request.form['password']
    email = request.form['email']
    error = None

    a = g.conn.execute("SELECT COUNT(*) FROM Users WHERE Email=(%s)", email)
    res = a.fetchall()[0][0]
    if res == 0:
      error = "No email"
      resp = make_response({"status":"fail","message":error}, 401)
      return resp


    user_info = g.conn.execute("SELECT * FROM Users WHERE Email=(%s)", email).fetchone()
    passwd = user_info[1]
    username = user_info[0]
    building = user_info[4]

    if not email:
      error = "Incorrect email"
    elif not check_password_hash(passwd, password):
      error = "Incorrect password"

    if error is None:
      session[email] = email

      resp = make_response({"status":"success","message":error,"data":{"username":username,"building":building}}, 200)
      resp.set_cookie("user_email", email)
      return resp

    resp = make_response({"status":"fail","message":error}, 401)
  return resp


@app.route('/signout', methods=["DELETE"])
def signout():
  email=request.cookies.get('user_email')
  if email in session:
    session.pop(email)
  error = None

  resp = make_response({"status":"success","message":error}, 200)
  resp.delete_cookie("user_email")
  return resp


@app.route('/user', methods=["GET", "POST"])
def user():
  if request.method == 'GET':
    email = request.args.get('email')
    error = None

    res = g.conn.execute("""
      SELECT U.username,U.email,U.telephone,U.building_name,A.address,A.zip_code FROM Users U,Apartment_Building A 
      WHERE U.Email=(%s) and U.building_name = A.name
    """, email).fetchall()
    if len(res) == 0:
      error = "No such a user"
      resp = make_response({"status":"fail","message":error}, 404)
      return resp

    resp = make_response({"status":"success","message":error,"data":list(res[0])}, 200)
    return resp

  if request.method == 'POST':
    error = None
    email=request.cookies.get('user_email')
    if email not in session:
      resp = make_response({"status":"fail","message":error}, 403)
      return resp
    telephone = int(request.form['telephone'])
    building_name = request.form['building_name']

    try:
      g.conn.execute("""
        UPDATE Users SET telephone = %s, building_name = %s
        WHERE Email=(%s)
      """, telephone,building_name,email)
      res = g.conn.execute("""
      SELECT address,zip_code FROM Apartment_Building
      WHERE name = %s
    """, building_name).fetchone()
    except:
      resp = make_response({"status":"fail","message":error}, 500)
      return resp

    resp = make_response({"status":"success","message":error,"data":{"address":res[0],"zip_code":res[1]}}, 200)
    return resp


@app.route('/order', methods=["GET", "POST"])
def order():
  if request.method == 'GET':
    error = None
    email=request.cookies.get('user_email')
    # if email not in session:
    #   resp = make_response({"status":"fail","message":error}, 403)
    #   return resp

    res = g.conn.execute("""
      SELECT O.good_id,O.total_price,O.time,G.image_url,G.description 
      FROM orders O, Second_hand_Goods G
      WHERE O.email=(%s) and O.good_id = G.good_id
      ORDER BY O.time DESC
    """, email).fetchall()

    resp = make_response({"status":"success","message":error,"data":list(map(list,res))}, 200)
    return resp


@app.route('/review', methods=["GET", "POST"])
def review():
  if request.method == 'GET':
    receiver = request.args.get('receiver')
    error = None

    res = g.conn.execute("""
      SELECT R.content,R.time,R.writer_email,U.username FROM Reviews R, Users U
      WHERE R.Receiver_Email=(%s) and R.Writer_Email = U.email
      ORDER BY R.time DESC
    """, receiver).fetchall()

    resp = make_response({"status":"success","message":error,"data":list(map(list,res))}, 200)
    return resp
  
  if request.method == 'POST':
    email=request.cookies.get('user_email')
    good_id = int(request.form['good_id'])
    content = request.form['content']
    error = None

    g.conn.execute("""
      INSERT INTO reviews 
      (content,writer_email,receiver_email) 
      VALUES (%s,%s,(select email from second_hand_goods where Good_ID = %s))
    """, content,email,good_id)

    resp = make_response({"status":"success","message":error}, 200)
    return resp


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.config['SECRET_KEY']=os.urandom(24)
    app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7)

    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
