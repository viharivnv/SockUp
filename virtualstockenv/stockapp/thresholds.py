import smtplib
import ssl
import mysql.connector
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def notify_user(user_email, user_msg):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "stockupalerts@gmail.com"  # Enter your address
    receiver_email = user_email  # Enter receiver address
    password = "stockupteam"
    msg = MIMEMultipart()
    msg['Subject'] = "StockUp Price Change Alert"
    msg.attach(MIMEText(user_msg, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


def check_thresholds():
    stocks = ['AAPL', 'AMZN', 'FB', 'GOOGL', 'NFLX', 'TSLA', 'TWTR', 'YELP', 'VAC', 'TRIP']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Password1$",
        database='appdata',
        auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
    mycursor.execute("USE appdata;")
    mycursor.execute("set sql_safe_updates = 0;")
    price_details = dict()

    for stock in stocks:
        mycursor.execute("SELECT sid from stocks where ticker='" + stock + "';")
        result = mycursor.fetchall()
        sid = result[0][0]
        mycursor.execute("SELECT close_value from real_time where sid='" + str(sid) +
                         "' order by dat desc, tim desc limit 1;")
        result = mycursor.fetchall()
        price_details[stock] = float(result[0][0])

    mycursor.execute("SELECT * from thresholds where satisfied = 0")
    result = mycursor.fetchall()
    for row in result:
        stock = row[1]
        user = row[0]
        curr_price = price_details[stock]
        prev_price = float(row[2])
        threshold = float(row[3])
        percent_price = (threshold / 100.0) * prev_price
        min_price = prev_price - percent_price
        max_price = prev_price + percent_price
        if curr_price >= max_price:
            msg = "Hello " + user + ",\n\nHope you're having a great day!\n\nThis email is to inform you that the " \
                    "price for stock " + str(stock) + " has increased by more than " + str(threshold) + " percent. " \
                    "Please login to the application for more details so that you don't miss out on any trading " \
                    "opportunity.\n\nThank you,\nStockUp Team"
            mycursor.execute("update thresholds set satisfied = 1 where username = '" + str(user)
                             + "' and ticker = '" + str(stock) + "';")
            mydb.commit()
            mycursor.execute("SELECT email from auth_user where username='" + str(user) + "';")
            result = mycursor.fetchall()
            user_email = result[0][0]
            notify_user(user_email, msg)
        if curr_price <= min_price:
            msg = "Hello " + user + ",\n\nHope you're having a great day!\n\nThis email is to inform you that the " \
                    "price for stock " + str(stock) + " has decreased by more than " + str(threshold) + " percent. " \
                    "Please login to the application for more details so that you don't miss out on any trading " \
                  "opportunity.\n\nThank you,\nStockUp Team"
            mycursor.execute("update thresholds set satisfied = 1 where username = '" + str(user)
                             + "' and ticker = '" + str(stock) + "';")
            mydb.commit()
            mycursor.execute("SELECT email from auth_user where username='" + str(user) + "';")
            result = mycursor.fetchall()
            user_email = result[0][0]
            notify_user(user_email, msg)
