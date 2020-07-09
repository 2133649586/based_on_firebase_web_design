from flask import Flask,render_template
import requests
import json
from flask import redirect, url_for,request
app= Flask(__name__)

@app.route("/")
def index():
    return(render_template("551.html"))






#########sakila table
@app.route("/sakila")
# def sakila():
#     return(render_template("sakila.html"))
def sakila():
   url_address = "https://final-project-52053.firebaseio.com/sakila/address.json"
   address = requests.get(url_address)
   address=address.json()

   url_customer = "https://final-project-52053.firebaseio.com/sakila/customer.json"
   customer = requests.get(url_customer)
   customer=customer.json()

   url_payment = "https://final-project-52053.firebaseio.com/sakila/payment.json"
   payment= requests.get(url_payment)
   payment=payment.json()
   return(render_template("sakila.html",address=address[:5],customer=customer[:5],payment=payment[:5]))

#    return(render_template("sakila.html"))
@app.route("/addresssakila")
def addresssakila():
   url_address = "https://final-project-52053.firebaseio.com/sakila/address.json"
   address = requests.get(url_address)
   customer = [{"address_id":"...",
              "customer_id":"...",
              "email":"...",
              "first_name":"...",
              "last_name":"..."
            }]
   payment = [{"amount":"...",
                      "customer_id":"...",
                      "payment_date":"...",
                      "payment_id":"..."
                    }]
   address=address.json()
   return (render_template("sakila.html", address=address, customer=customer, payment=payment))

@app.route("/customersakila")
def customersakila():
   url_customer = "https://final-project-52053.firebaseio.com/sakila/customer.json"
   customer = requests.get(url_customer)
   address = [{   "address":"...",
              "address_id":"...",
              "district":"...",
              "postal_code":"..."
            }]
   customer=customer.json()
   payment = [{"amount":"...",
                      "customer_id":"...",
                      "payment_date":"...",
                      "payment_id":"..."
                    }]
   return (render_template("sakila.html", address=address, customer=customer, payment=payment))

@app.route("/paymentsakila")
def paymentsakila():
   url_payment = "https://final-project-52053.firebaseio.com/sakila/payment.json"
   payment = requests.get(url_payment)
   address = [{   "address":"...",
              "address_id":"...",
              "district":"...",
              "postal_code":"..."
            }]
   customer = [{"address_id":"...",
              "customer_id":"...",
              "email":"...",
              "first_name":"...",
              "last_name":"..."
            }]
   payment=payment.json()
   return (render_template("sakila.html", address=address, customer=customer, payment=payment))




#########sakila search
@app.route('/api/start1', methods=['POST'], strict_slashes=False)
def api_predict1():
    index = request.form['file_path']
    index = str(index).lower()
    total = index.split(" ")
    address = []
    customer = []
    payment = []
    new_address = []
    new_customer = []
    new_payment = []

    if len(total) <= 1:
        url = f"https://final-project-52053.firebaseio.com/sakila/index/{index}.json"
        word = requests.get(url)
        word = word.json()
        for i in word:
            if ("address" in i) and ("address_id" in i) and ("district" in i) and ("postal_code" in i):
                address.append(i)
            if ("address_id" in i) and ("customer_id" in i) and ("email" in i) and ("first_name" in i) and (
                    "last_name" in i):
                customer.append(i)
            if ("amount" in i) and ("customer_id" in i) and ("payment_date" in i) and ("payment_id" in i):
                payment.append(i)
        if len(address) < 1:
            address = [{"address": "...",
                        "address_id": "...",
                        "district": "...",
                        "postal_code": "..."
                        }]
        if len(customer) < 1:
            customer = [{"address_id": "...",
                         "customer_id": "...",
                         "email": "...",
                         "first_name": "...",
                         "last_name": "..."
                         }]
        if len(payment) < 1:
            payment = [{"amount": "...",
                        "customer_id": "...",
                        "payment_date": "...",
                        "payment_id": "..."
                        }]
        new_address = address
        new_customer = customer
        new_payment = payment

    if len(total)>1:
        for single_index in total:
            url = f"https://final-project-52053.firebaseio.com/sakila/index/{single_index}.json"
            word = requests.get(url)
            word = word.json()
            print(word)
            for i in word:
                if ("address" in i)and("address_id" in i)and("district" in i)and("postal_code" in i):
                    address.append(i)
                if ("address_id" in i)and("customer_id" in i)and("email" in i)and("first_name" in i)and("last_name" in i):
                    customer.append(i)
                if ("amount" in i)and("customer_id" in i)and("payment_date" in i)and("payment_id" in i):
                    payment.append(i)

        if len(address)<1:
            address = [{   "address":"...",
                "address_id":"...",
                "district":"...",
                "postal_code":"..."
            }]
        if len(customer)<1:
            customer = [{"address_id":"...",
                "customer_id":"...",
                "email":"...",
                "first_name":"...",
                "last_name":"..."
            }]
        if len(payment)<1:
            payment = [{"amount":"...",
                        "customer_id":"...",
                        "payment_date":"...",
                        "payment_id":"..."
                    }]


    # according to appear times to give order
        address_dict = {}
        index_address_dict = {}
        for i in range(0, len(address)):
            if i == 0:
                address_dict[f"{i}"] = address[i]
                index_address_dict[f"{i}"] = 1
            else:
                ensure = 0
                for j in address_dict:
                    target = address_dict[j]
                    if target["address"] == address[i]["address"] and target["address_id"] == address[i]["address_id"] and \
                            target["district"] == address[i]["district"] and target["postal_code"] == address[i][
                        "postal_code"]:
                        ensure = j
                if ensure == 0:
                    address_dict[f"{i}"] = address[i]
                    index_address_dict[f"{i}"] = 1
                else:
                    index_address_dict[f"{ensure}"] = index_address_dict[f"{ensure}"] + 1

        for i in range(0,len(index_address_dict)):
            current = max(index_address_dict, key=index_address_dict.get)
            new_address.append(address_dict[current])
            index_address_dict.pop(current)



        customer_dict = {}
        index_customer_dict = {}
        for i in range(0, len(customer)):
            if i == 0:
                customer_dict[f"{i}"] = customer[i]
                index_customer_dict[f"{i}"] = 1
            else:
                ensure = 0
                for j in customer_dict:
                    target = customer_dict[j]
                    if target["address_id"] == customer[i]["address_id"] and target["customer_id"] == customer[i]["customer_id"] and \
                            target["email"] == customer[i]["email"] and target["first_name"] == customer[i]["first_name"] and\
                            target["last_name"] == customer[i]["last_name"]:
                        ensure = j
                if ensure == 0:
                    customer_dict[f"{i}"] = customer[i]
                    index_customer_dict[f"{i}"] = 1
                else:
                    index_customer_dict[f"{ensure}"] = index_customer_dict[f"{ensure}"] + 1

        for i in range(0,len(index_customer_dict)):
            current = max(index_customer_dict, key=index_customer_dict.get)
            new_customer.append(customer_dict[current])
            index_customer_dict.pop(current)



        payment_dict = {}
        index_payment_dict = {}
        for i in range(0, len(payment)):
            if i == 0:
                payment_dict[f"{i}"] = payment[i]
                index_payment_dict[f"{i}"] = 1
            else:
                ensure = 0
                for j in payment_dict:
                    target = payment_dict[j]
                    if target["amount"] == payment[i]["amount"] and target["customer_id"] == payment[i]["customer_id"] \
                            and target["payment_date"] == payment[i]["payment_date"] and\
                            target["payment_id"] == payment[i]["payment_id"]:
                        ensure = j
                if ensure == 0:
                    payment_dict[f"{i}"] = payment[i]
                    index_payment_dict[f"{i}"] = 1
                else:
                    index_payment_dict[f"{ensure}"] = index_payment_dict[f"{ensure}"] + 1

        for i in range(0,len(index_payment_dict)):
            current = max(index_payment_dict, key=index_payment_dict.get)
            new_payment.append(payment_dict[current])
            print(index_payment_dict[current])
            index_payment_dict.pop(current)




    return (render_template("sakila.html", address=new_address, customer=new_customer, payment=new_payment))

# sakila search reference
@app.route('/sakila_address_ref/<word>')
def sakila_address_ref(word:str):
    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/sakila/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    address = []
    customer = []
    payment = []
    for i in word:
        if ("address" in i)and("address_id" in i)and("district" in i)and("postal_code" in i):
            address.append(i)
        if ("address_id" in i)and("customer_id" in i)and("email" in i)and("first_name" in i)and("last_name" in i)and(i["address_id"]==index):
            customer.append(i)
        if ("amount" in i)and("customer_id" in i)and("payment_date" in i)and("payment_id" in i):
            payment.append(i)
    print(customer)
    address = [{   "address":"...",
        "address_id":"...",
        "district":"...",
        "postal_code":"..."
    }]
    if len(customer)<1:
        customer = [{"address_id":"...",
            "customer_id":"...",
            "email":"...",
            "first_name":"...",
            "last_name":"..."
        }]
   
    payment = [{"amount":"...",
                "customer_id":"...",
                "payment_date":"...",
                "payment_id":"..."
            }]
    return (render_template("sakila.html", address=address, customer=customer, payment=payment))
  

@app.route('/sakila_customer_ref/<word>')
def sakila_customer_ref(word:str):
    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/sakila/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    print(word)
    address = []
    customer = []
    payment = []
    for i in word:
        if ("address" in i)and("address_id" in i)and("district" in i)and("postal_code" in i):
            address.append(i)
        if ("address_id" in i)and("customer_id" in i)and("email" in i)and("first_name" in i)and("last_name" in i):
            customer.append(i)
        if ("amount" in i)and("customer_id" in i)and("payment_date" in i)and("payment_id" in i):
            payment.append(i)
    if len(address)<1:
        address = [{   "address":"...",
            "address_id":"...",
            "district":"...",
            "postal_code":"..."
        }]

    customer = [{"address_id":"...",
        "customer_id":"...",
        "email":"...",
        "first_name":"...",
        "last_name":"..."
    }]
   
    payment = [{"amount":"...",
                "customer_id":"...",
                "payment_date":"...",
                "payment_id":"..."
            }]
    return (render_template("sakila.html", address=address, customer=customer, payment=payment))    


  
  
@app.route('/sakila_payment_ref/<word>')
def sakila_payment_ref(word:str):

    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/sakila/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    print(word)
    address = []
    customer = []
    payment = []
    for i in word:
        if ("address" in i)and("address_id" in i)and("district" in i)and("postal_code" in i):
            address.append(i)
        if ("address_id" in i)and("customer_id" in i)and("email" in i)and("first_name" in i)and("last_name" in i):
            customer.append(i)
        if ("amount" in i)and("customer_id" in i)and("payment_date" in i)and("payment_id" in i):
            payment.append(i)

    address = [{   "address":"...",
        "address_id":"...",
        "district":"...",
        "postal_code":"..."
    }]
    if len(customer)<1:
        customer = [{"address_id":"...",
            "customer_id":"...",
            "email":"...",
            "first_name":"...",
            "last_name":"..."
        }]
    payment = [{"amount":"...",
                "customer_id":"...",
                "payment_date":"...",
                "payment_id":"..."
            }]
    return (render_template("sakila.html", address=address, customer=customer, payment=payment))    
# ############
@app.route('/sakila_customer1_ref/<word>')
def sakila_customer1_ref(word:str):
    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/sakila/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    address = []
    customer = []
    payment = []
    for i in word:
        if ("address" in i)and("address_id" in i)and("district" in i)and("postal_code" in i):
            address.append(i)
        if ("address_id" in i)and("customer_id" in i)and("email" in i)and("first_name" in i)and("last_name" in i):
            customer.append(i)
        if ("amount" in i)and("customer_id" in i)and("payment_date" in i)and("payment_id" in i)and(i["customer_id"]==index):
            payment.append(i)

    address = [{   "address":"...",
        "address_id":"...",
        "district":"...",
        "postal_code":"..."
    }]

    customer = [{"address_id":"...",
        "customer_id":"...",
        "email":"...",
        "first_name":"...",
        "last_name":"..."
    }]
    if len(payment)<1:
        payment = [{"amount":"...",
                    "customer_id":"...",
                    "payment_date":"...",
                    "payment_id":"..."
                }]
    return (render_template("sakila.html", address=address, customer=customer, payment=payment))    














########classic table
@app.route("/classic")
def classic():
   url_orders = "https://final-project-52053.firebaseio.com/classicmodels/orders.json"
   orders = requests.get(url_orders)
   orders=orders.json()

   url_payments = "https://final-project-52053.firebaseio.com/classicmodels/payments.json"
   payments = requests.get(url_payments)
   payments=payments.json()

   url_customers= "https://final-project-52053.firebaseio.com/classicmodels/customers.json"
   customers = requests.get(url_customers)
   customers=customers.json()
   return(render_template("classic.html",orders=orders[:5],payments=payments[:5],customers=customers[:5]))
@app.route("/ordersclassic")
def ordersclassic():
   url_orders = "https://final-project-52053.firebaseio.com/classicmodels/orders.json"
   orders = requests.get(url_orders)
   payments = [{"amount":"...",
              "checkNumber":"...",
              "customerNumber":"...",
              "paymentDate":"..."
            }]
   customers = [{"city":"...",
                 "customerName":"...",
                 "customerNumber":"..."
                    }]
   orders=orders.json()
   return(render_template("classic.html",orders=orders,payments=payments,customers=customers))

@app.route("/paymentsclassic")
def paymentsclassic():
   url_payments = "https://final-project-52053.firebaseio.com/classicmodels/payments.json"
   payments = requests.get(url_payments)
   orders = [{   "comments":"...",
              "customerNumber":"...",
              "orderNumber":"...",
              "status":"...",
            }]
   payments=payments.json()
   customers = [{"city":"...",
                 "customerName":"...",
                 "customerNumber":"..."
                    }]
   return(render_template("classic.html",orders=orders,payments=payments,customers=customers))

@app.route("/customersclassic")
def customersclassic():
   url_customers = "https://final-project-52053.firebaseio.com/classicmodels/customers.json"
   customers = requests.get(url_customers)
   orders = [{   "comments":"...",
              "customerNumber":"...",
              "orderNumber":"...",
              "status":"...",
            }]
   payments = [{"amount":"...",
              "checkNumber":"...",
              "customerNumber":"...",
              "paymentDate":"..."
            }]
   customers=customers.json()
   return(render_template("classic.html",orders=orders,payments=payments, customers=customers))


#######classic_search
@app.route('/api/start2', methods=['POST'], strict_slashes=False)
def api_predict2():
    index = request.form['file_path']
    index = str(index).lower()
    total = index.split(" ")
    orders = []
    payments = []
    customers = []
    new_orders = []
    new_payments = []
    new_customers = []

    if len(total) <= 1:
        url = f"https://final-project-52053.firebaseio.com/classicmodels/index/{index}.json"
        word = requests.get(url)
        word = word.json()
        print(word)
        for i in word:
            if ("comments" in i)and("customerNumber" in i)and("orderNumber" in i)and("status" in i):
                orders.append(i)
            if ("amount" in i)and("checkNumber" in i)and("customerNumber" in i)and("paymentDate" in i):
                payments.append(i)
            if ("city" in i)and("customerName" in i)and("customerNumber" in i):
                customers.append(i)
        if len(orders)<1:
            orders = [{   "comments":"...",
                "customerNumber":"...",
                "orderNumber":"...",
                "status":"...",
            }]
        if len(payments)<1:
            payments = [{"amount":"...",
                        "checkNumber":"...",
                        "customerNumber":"...",
                        "paymentDate":"..."
                    }]
        if len(customers)<1:
            customers = [{"city":"...",
                    "customerName":"...",
                    "customerNumber":"..."
                    }]
        new_orders = orders
        new_payments = payments
        new_customers = customers

    if len(total) > 1:
        for single_index in total:
            url = f"https://final-project-52053.firebaseio.com/classicmodels/index/{single_index}.json"
            word = requests.get(url)
            word = word.json()
            for i in word:
                if ("comments" in i)and("customerNumber" in i)and("orderNumber" in i)and("status" in i):
                    orders.append(i)
                if ("amount" in i)and("checkNumber" in i)and("customerNumber" in i)and("paymentDate" in i):
                    payments.append(i)
                if ("city" in i)and("customerName" in i)and("customerNumber" in i):
                    customers.append(i)
        if len(orders)<1:
            orders = [{   "comments":"...",
                "customerNumber":"...",
                "orderNumber":"...",
                "status":"...",
            }]
        if len(payments)<1:
            payments = [{"amount":"...",
                        "checkNumber":"...",
                        "customerNumber":"...",
                        "paymentDate":"..."
                    }]
        if len(customers)<1:
            customers = [{"city":"...",
                    "customerName":"...",
                    "customerNumber":"..."
                    }]

        # according to appear times to give order
        orders_dict = {}
        index_orders_dict = {}
        for i in range(0, len(orders)):
            if i == 0:
                orders_dict[f"{i}"] = orders[i]
                index_orders_dict[f"{i}"] = 1
            else:
                ensure = 0
                for j in orders_dict:
                    target = orders_dict[j]
                    if target["comments"] == orders[i]["comments"] and target["customerNumber"] == orders[i][
                        "customerNumber"] and \
                            target["orderNumber"] == orders[i]["orderNumber"] and target["status"] == orders[i][
                        "status"]:
                        ensure = j
                if ensure == 0:
                    orders_dict[f"{i}"] = orders[i]
                    index_orders_dict[f"{i}"] = 1
                else:
                    index_orders_dict[f"{ensure}"] = index_orders_dict[f"{ensure}"] + 1

        for i in range(0, len(index_orders_dict)):
            current = max(index_orders_dict, key=index_orders_dict.get)
            new_orders.append(orders_dict[current])
            index_orders_dict.pop(current)


        payments_dict = {}
        index_payments_dict = {}
        for i in range(0, len(payments)):
            if i == 0:
                payments_dict[f"{i}"] = payments[i]
                index_payments_dict[f"{i}"] = 1
            else:
                ensure = 0
                for j in payments_dict:
                    target = payments_dict[j]
                    if target["amount"] == payments[i]["amount"] and target["checkNumber"] == payments[i][
                        "checkNumber"] and target["customerNumber"] == payments[i]["customerNumber"] and target["paymentDate"] == payments[i]["paymentDate"]:
                        ensure = j
                if ensure == 0:
                    payments_dict[f"{i}"] = payments[i]
                    index_payments_dict[f"{i}"] = 1
                else:
                    index_payments_dict[f"{ensure}"] = index_payments_dict[f"{ensure}"] + 1

        for i in range(0, len(index_payments_dict)):
            current = max(index_payments_dict, key=index_payments_dict.get)
            new_payments.append(payments_dict[current])
            index_payments_dict.pop(current)


        customers_dict = {}
        index_customers_dict = {}
        for i in range(0, len(customers)):
            if i == 0:
                customers_dict[f"{i}"] = customers[i]
                index_customers_dict[f"{i}"] = 1
            else:
                ensure = 0
                for j in customers_dict:
                    target = customers_dict[j]
                    if target["city"] == customers[i]["city"] and target["customerName"] == customers[i][
                        "customerName"] and \
                            target["customerNumber"] == customers[i]["customerNumber"]:
                        ensure = j
                if ensure == 0:
                    customers_dict[f"{i}"] = customers[i]
                    index_customers_dict[f"{i}"] = 1
                else:
                    index_customers_dict[f"{ensure}"] = index_customers_dict[f"{ensure}"] + 1

        for i in range(0, len(index_customers_dict)):
            current = max(index_customers_dict, key=index_customers_dict.get)
            new_customers.append(customers_dict[current])
            index_customers_dict.pop(current)

    return(render_template("classic.html",orders=new_orders,payments=new_payments, customers=new_customers))



# classic search reference
@app.route('/classic_orders_ref/<word>')
def classic_orders_ref(word:str):
    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/classicmodels/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    print(word)
    orders = []
    payments = []
    customers = []
    for i in word:
        if ("comments" in i)and("customerNumber" in i)and("orderNumber" in i)and("status" in i):
            orders.append(i)
        if ("amount" in i)and("checkNumber" in i)and("customerNumber" in i)and("paymentDate" in i):
            payments.append(i)
        if ("city" in i)and("customerName" in i)and("customerNumber" in i):
            customers.append(i)
            

    orders = [{   "comments":"...",
        "customerNumber":"...",
        "orderNumber":"...",
        "status":"...",
    }]
    payments = [{"amount":"...",
                "checkNumber":"...",
                "customerNumber":"...",
                "paymentDate":"..."
            }]
    if len(customers)<1:
        customers = [{"city":"...",
                "customerName":"...",
                "customerNumber":"..."
                }]
    return(render_template("classic.html",orders=orders,payments=payments, customers=customers))

@app.route('/classic_payments_ref/<word>')
def classic_payments_ref(word:str):
    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/classicmodels/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    print(word)
    orders = []
    payments = []
    customers = []
    for i in word:
        if ("comments" in i)and("customerNumber" in i)and("orderNumber" in i)and("status" in i):
            orders.append(i)
        if ("amount" in i)and("checkNumber" in i)and("customerNumber" in i)and("paymentDate" in i):
            payments.append(i)
        if ("city" in i)and("customerName" in i)and("customerNumber" in i):
            customers.append(i)
            

    orders = [{   "comments":"...",
        "customerNumber":"...",
        "orderNumber":"...",
        "status":"...",
    }]
    payments = [{"amount":"...",
                "checkNumber":"...",
                "customerNumber":"...",
                "paymentDate":"..."
            }]
    if len(customers)<1:
        customers = [{"city":"...",
                "customerName":"...",
                "customerNumber":"..."
                }]
    return(render_template("classic.html",orders=orders,payments=payments, customers=customers))

@app.route('/classic_customers_ref/<word>')
def classic_customers_ref(word:str):
    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/classicmodels/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    print(word)
    orders = []
    payments = []
    customers = []
    for i in word:
        if ("comments" in i)and("customerNumber" in i)and("orderNumber" in i)and("status" in i):
            orders.append(i)
        if ("amount" in i)and("checkNumber" in i)and("customerNumber" in i)and("paymentDate" in i):
            payments.append(i)
        if ("city" in i)and("customerName" in i)and("customerNumber" in i):
            customers.append(i)
            
    if len(orders)<1:
        orders = [{   "comments":"...",
            "customerNumber":"...",
            "orderNumber":"...",
            "status":"...",
    }]
    if len(payments)<1:
        payments = [{"amount":"...",
                    "checkNumber":"...",
                    "customerNumber":"...",
                    "paymentDate":"..."
                }]

    customers = [{"city":"...",
            "customerName":"...",
            "customerNumber":"..."
            }]
    return(render_template("classic.html",orders=orders,payments=payments, customers=customers))
























###########
# world table
@app.route("/world")
def world():
   url_city = "https://final-project-52053.firebaseio.com/world/city.json"
   city = requests.get(url_city)
   city=city.json()

   url_country = "https://final-project-52053.firebaseio.com/world/country.json"
   country = requests.get(url_country)
   country=country.json()

   url_countrylanguage = "https://final-project-52053.firebaseio.com/world/countrylanguage.json"
   countrylanguage = requests.get(url_countrylanguage)
   countrylanguage=countrylanguage.json()
   return(render_template("world.html",city=city[:5],country=country[:5],countrylanguage=countrylanguage[:5]))

@app.route("/cityworld")
def cityworld():
   url_city = "https://final-project-52053.firebaseio.com/world/city.json"
   city = requests.get(url_city)
   country = [{"Code":"...",
              "Continent":"...",
              "Name":"...",
              "Region":"..."
            }]
   countrylanguage = [{"CountryCode":"...",
                      "IsOfficial":"...",
                      "Language":"...",
                      "Percentage":"..."
                    }]
   city=city.json()
   return (render_template("world.html", city=city, country=country, countrylanguage=countrylanguage))

@app.route("/countryworld")
def countryworld():
   url_country = "https://final-project-52053.firebaseio.com/world/country.json"
   country = requests.get(url_country)
   city = [{   "ID":"...",
              "District":"...",
              "Name":"...",
              "CountryCode":"...",
              "Population":"..."
            }]
   country=country.json()
   countrylanguage = [{"CountryCode":"...",
                      "IsOfficial":"...",
                      "Language":"...",
                      "Percentage":"..."
                    }]
   return (render_template("world.html", city=city, country=country, countrylanguage=countrylanguage))

@app.route("/countrylanguageworld")
def countrylanguageworld():
   url_countrylanguage = "https://final-project-52053.firebaseio.com/world/countrylanguage.json"
   countrylanguage = requests.get(url_countrylanguage)
   city = [{   "ID":"...",
              "District":"...",
              "Name":"...",
              "CountryCode":"...",
              "Population":"..."
            }]
   country = [{"Code":"...",
              "Continent":"...",
              "Name":"...",
              "Region":"..."
   }]
   countrylanguage=countrylanguage.json()
   return(render_template("world.html",city=city, country=country, countrylanguage=countrylanguage))



# world_search
@app.route('/api/start', methods=['POST'], strict_slashes=False)
def api_predict():
    index = request.form['file_path']
    index = str(index).lower()
    total = index.split(" ")
    city = []
    country = []
    countrylanguage = []
    new_city = []
    new_country = []
    new_countrylanguage = []

    if len(total) <= 1:
        url = f"https://final-project-52053.firebaseio.com/world/index/{index}.json"
        word = requests.get(url)
        word = word.json()
        print(word)

        for i in word:
            if ("ID" in i)and("District" in i)and("Name" in i)and("CountryCode" in i)and("Population" in i):
                city.append(i)
            if ("Code" in i)and("Continent" in i)and("Name" in i)and("Region" in i):
                country.append(i)
            if ("CountryCode" in i)and("IsOfficial" in i)and("Language" in i)and("Percentage" in i):
                countrylanguage.append(i)
        if len(city)<1:
            city = [{"ID": "...",
                     "District": "...",
                     "Name": "...",
                     "CountryCode": "...",
                     "Population": "..."
                     }]
        if len(country)<1:
            country = [{"Code": "...",
                        "Continent": "...",
                        "Name": "...",
                        "Region": "..."
                        }]
        if len(countrylanguage)<1:
            countrylanguage = [{"CountryCode": "...",
                                "IsOfficial": "...",
                                "Language": "...",
                                "Percentage": "..."
                                }]
        new_city = city
        new_country =country
        new_countrylanguage = countrylanguage

    if len(total)>1:
        for single_index in total:
            print(single_index)
            url = f"https://final-project-52053.firebaseio.com/world/index/{single_index}.json"
            word = requests.get(url)
            word = word.json()
            print(word)

            for i in word:
                if ("ID" in i) and ("District" in i) and ("Name" in i) and ("CountryCode" in i) and ("Population" in i):
                    city.append(i)
                if ("Code" in i) and ("Continent" in i) and ("Name" in i) and ("Region" in i):
                    country.append(i)
                if ("CountryCode" in i) and ("IsOfficial" in i) and ("Language" in i) and ("Percentage" in i):
                    countrylanguage.append(i)
        if len(city) < 1:
            city = [{"ID": "...",
                     "District": "...",
                     "Name": "...",
                     "CountryCode": "...",
                     "Population": "..."
                     }]
        if len(country) < 1:
            country = [{"Code": "...",
                        "Continent": "...",
                        "Name": "...",
                        "Region": "..."
                        }]
        if len(countrylanguage) < 1:
            countrylanguage = [{"CountryCode": "...",
                                "IsOfficial": "...",
                                "Language": "...",
                                "Percentage": "..."
                                }]

    # according to appear times to give order
        city_dict = {}
        index_city_dict = {}
        for i in range(0, len(city)):
            if i == 0:
                city_dict[f"{i}"] = city[i]
                index_city_dict[f"{i}"] = 1
            else:
                ensure = 0
                for j in city_dict:
                    target = city_dict[j]
                    if target["ID"] == city[i]["ID"] and target["District"] == city[i][
                        "District"] and \
                            target["Name"] == city[i]["Name"] and target["CountryCode"] == city[i][
                        "CountryCode"] and target["Population"] == city[i]["Population"]:
                        ensure = j
                if ensure == 0:
                    city_dict[f"{i}"] = city[i]
                    index_city_dict[f"{i}"] = 1
                else:
                    index_city_dict[f"{ensure}"] = index_city_dict[f"{ensure}"] + 1

        for i in range(0, len(index_city_dict)):
            current = max(index_city_dict, key=index_city_dict.get)
            new_city.append(city_dict[current])
            index_city_dict.pop(current)


        country_dict = {}
        index_country_dict = {}
        for i in range(0, len(country)):
            if i == 0:
                country_dict[f"{i}"] = country[i]
                index_country_dict[f"{i}"] = 1
            else:
                ensure = 0
                for j in country_dict:
                    target = country_dict[j]
                    if target["Code"] == country[i]["Code"] and target["Continent"] == country[i][
                        "Continent"] and \
                            target["Name"] == country[i]["Name"] and target["Region"] == country[i][
                        "Region"]:
                        ensure = j
                if ensure == 0:
                    country_dict[f"{i}"] = country[i]
                    index_country_dict[f"{i}"] = 1
                else:
                    index_country_dict[f"{ensure}"] = index_country_dict[f"{ensure}"] + 1

        for i in range(0, len(index_country_dict)):
            print(index_country_dict)
            current = max(index_country_dict, key=index_country_dict.get)
            new_country.append(country_dict[current])
            index_country_dict.pop(current)



        countrylanguage_dict = {}
        index_countrylanguage_dict = {}
        for i in range(0, len(countrylanguage)):
            if i == 0:
                countrylanguage_dict[f"{i}"] = countrylanguage[i]
                index_countrylanguage_dict[f"{i}"] = 1
            else:
                ensure = 0
                for j in countrylanguage_dict:
                    target = countrylanguage_dict[j]
                    if target["CountryCode"] == countrylanguage[i]["CountryCode"] and target["IsOfficial"] == countrylanguage[i][
                        "IsOfficial"] and \
                            target["Language"] == countrylanguage[i]["Language"] and target["Percentage"] == countrylanguage[i][
                        "Percentage"]:
                        ensure = j
                if ensure == 0:
                    countrylanguage_dict[f"{i}"] = countrylanguage[i]
                    index_countrylanguage_dict[f"{i}"] = 1
                else:
                    index_countrylanguage_dict[f"{ensure}"] = index_countrylanguage_dict[f"{ensure}"] + 1

        for i in range(0, len(index_countrylanguage_dict)):
            current = max(index_countrylanguage_dict, key=index_countrylanguage_dict.get)
            new_countrylanguage.append(countrylanguage_dict[current])
            index_countrylanguage_dict.pop(current)

    return(render_template("world.html",city=new_city, country=new_country, countrylanguage=new_countrylanguage))

# world search reference
@app.route('/world_city_ref/<word>')
def world_city_ref(word:str):
    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/world/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    print(word)
    city = []
    country = []
    countrylanguage = []
    for i in word:
        if ("ID" in i)and("District" in i)and("Name" in i)and("CountryCode" in i)and("Population" in i):
            city.append(i)
        if ("Code" in i)and("Continent" in i)and("Name" in i)and("Region" in i):
            country.append(i)
        if ("CountryCode" in i)and("IsOfficial" in i)and("Language" in i)and("Percentage" in i):
            countrylanguage.append(i)
    if len(city)<1:
        city = [{"ID": "...",
                 "District": "...",
                 "Name": "...",
                 "CountryCode": "...",
                 "Population": "..."
                 }]
    if len(country)<1:
        country = [{"Code": "...",
                    "Continent": "...",
                    "Name": "...",
                    "Region": "..."
                    }]
    if len(countrylanguage)<1:
        countrylanguage = [{"CountryCode": "...",
                            "IsOfficial": "...",
                            "Language": "...",
                            "Percentage": "..."
                            }]
    return(render_template("world.html",city=city, country=country, countrylanguage=countrylanguage))


@app.route('/world_country_ref/<word>')
def world_country_ref(word:str):
    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/world/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    print(word)
    city = []
    country = []
    countrylanguage = []
    for i in word:
        if ("ID" in i)and("District" in i)and("Name" in i)and("CountryCode" in i)and("Population" in i):
            city.append(i)
        if ("Code" in i)and("Continent" in i)and("Name" in i)and("Region" in i):
            country.append(i)
        if ("CountryCode" in i)and("IsOfficial" in i)and("Language" in i)and("Percentage" in i):
            countrylanguage.append(i)

    city = [{"ID": "...",
             "District": "...",
             "Name": "...",
             "CountryCode": "...",
             "Population": "..."
             }]

    country = [{"Code": "...",
                "Continent": "...",
                "Name": "...",
                "Region": "..."
                }]
    if len(countrylanguage)<1:
        countrylanguage = [{"CountryCode": "...",
                            "IsOfficial": "...",
                            "Language": "...",
                            "Percentage": "..."
                            }]
    return(render_template("world.html",city=city, country=country, countrylanguage=countrylanguage))

@app.route('/world_countrylanguage_ref/<word>')
def world_countrylanguage_ref(word:str):
    index = str(word).lower()
    url = f"https://final-project-52053.firebaseio.com/world/index/{index}.json"
    word = requests.get(url)
    word = word.json()
    print(word)
    city = []
    country = []
    countrylanguage = []
    for i in word:
        if ("ID" in i)and("District" in i)and("Name" in i)and("CountryCode" in i)and("Population" in i):
            city.append(i)
        if ("Code" in i)and("Continent" in i)and("Name" in i)and("Region" in i):
            country.append(i)
        if ("CountryCode" in i)and("IsOfficial" in i)and("Language" in i)and("Percentage" in i):
            countrylanguage.append(i)

    city = [{"ID": "...",
             "District": "...",
             "Name": "...",
             "CountryCode": "...",
             "Population": "..."
             }]
    if len(country)<1:
        country = [{"Code": "...",
                    "Continent": "...",
                    "Name": "...",
                    "Region": "..."
                    }]

    countrylanguage = [{"CountryCode": "...",
                        "IsOfficial": "...",
                        "Language": "...",
                        "Percentage": "..."
                        }]
    return(render_template("world.html",city=city, country=country, countrylanguage=countrylanguage))



if __name__=="__main__":
     app.run(debug=True)

