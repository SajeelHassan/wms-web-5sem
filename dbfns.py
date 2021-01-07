import pymysql
import datetime


class DBFns:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    # add the product

    def addProduct(self, title, sku, cost, price, stock, low):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "INSERT INTO products (title,sku,cost,price,stock,low,curr_status,created_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            currstatus = self.setStatus(stock, low)
            createdOn = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            args = (title, sku, cost, price, stock,
                    low, currstatus, createdOn)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status
    # update the product

    def setStatus(self, stock, low):
        if stock >= low:
            return 'In Stock'
        elif stock == 0:
            return 'Out of Stock'
        elif stock < 15:
            return 'Soon out of Stock'
        elif stock < low:
            return 'Low Stock'

    def updateProduct(self, title, sku, cost, price, stock, low, prodid):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "UPDATE products SET title=%s,sku=%s,cost=%s,price=%s,stock=%s,low=%s,curr_status=%s,last_updated=%s WHERE prod_id=%s"
            currstatus = self.setStatus(stock, low)
            lUpdated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            args = (title, sku, cost, price, stock,
                    low, currstatus, lUpdated, prodid)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status
    # // get single product using prod id and its sku

    def isSkuExists(self, sku):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "Select * from products WHERE sku =%s"
            mydbCursor.execute(sql, sku)
            myresult = mydbCursor.fetchone()
            if myresult != None:
                if myresult[2] == sku:
                    status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def getProduct(self, prodid):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "Select * from products WHERE prod_id =%s"
            args = (prodid)
            mydbCursor.execute(sql, args)
            myresult = mydbCursor.fetchone()
            if myresult != None:
                if myresult[0] == prodid:
                    # print(myresult[8].strftime("%c"))
                    status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            if status == True:
                return myresult
            else:
                return status

    def getAllProducts(self):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "Select * from products ORDER BY created_on DESC"
            mydbCursor.execute(sql)
            myresult = mydbCursor.fetchall()
            if myresult != None:
                # print(myresult[8].strftime("%c"))
                status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            if status == True:
                return myresult
            else:
                return status

    def deleteProduct(self, prodid, sku):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "Delete FROM products WHERE prod_id=%s AND sku=%s"
            # lUpdated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            args = (prodid, sku)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def addProdToReceipt(self, prod_id, sr_no, qty, total_price):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "INSERT INTO receiptproducts (prod_id,sr_no, qty, total_price) VALUES (%s,%s,%s,%s)"
            args = (prod_id, sr_no, qty, total_price)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
            # self.updateStock(prod_id,qty)
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def getStock(self, prod_id):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "Select prod_id,stock from products WHERE prod_id =%s"
            args = (prod_id)
            mydbCursor.execute(sql, args)
            myresult = mydbCursor.fetchone()
            # print(myresult)
            if myresult != None:
                if myresult[0] == prod_id:
                    # print(myresult[8].strftime("%c"))
                    # print(myresult[1])
                    status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            if status == True:
                return myresult[1]
            else:
                return status

    def updateStock(self, prod_id, qty):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "UPDATE products SET stock=stock-%s WHERE prod_id=%s"
            args = (qty, prod_id)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def newReceipt(self, total_prod, total_rcpt_price, sold_by, cust_name, pay_status):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "INSERT INTO receipt (total_prod,total_rcpt_price,sold_by,cust_name,pay_status,date_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            createdOn = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            args = (total_prod, total_rcpt_price, sold_by,
                    cust_name, pay_status, createdOn)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def deleteReceipt(self, ordid):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "Delete FROM receipt WHERE rcpt_id=%s"
            args = (ordid)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def addEmployee(self, firstname, lastname, email, phone):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "INSERT INTO employee (firstname, lastname, joined_on, email, phone) VALUES (%s,%s,%s,%s,%s)"
            joinedOn = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            args = (firstname, lastname, joinedOn, email, phone)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def removeEmployee(self, empid):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "Delete FROM employee WHERE emp_id=%s"
            args = (empid)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def updateEmployee(self, firstname, lastname,  email, phone, empid):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "UPDATE products SET firstname=%s,lastname=%s,email=%s,phone=%s WHERE emp_id=%s"

            args = (firstname, lastname,  email, phone, empid)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def addCustomer(self, firstname, lastname, email, phone):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "INSERT INTO customer (firstname, lastname, created_on, email, phone) VALUES (%s,%s,%s,%s,%s)"
            createdOn = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            args = (firstname, lastname, createdOn, email, phone)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def removeCustomer(self, cust_id):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "Delete FROM customer WHERE cust_id=%s"
            args = (cust_id)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status

    def updateCustomer(self, firstname, lastname,  email, phone, custid):
        mydb = None
        status = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "UPDATE customer SET firstname=%s,lastname=%s,email=%s,phone=%s WHERE cust_id=%s"
            args = (firstname, lastname,  email, phone, custid)
            mydbCursor.execute(sql, args)
            mydb.commit()
            status = True
        except Exception as e:
            print(str(e))
        finally:
            if mydb != None:
                mydb.close()
            return status


if __name__ == "__main__":
    obj = DBFns('localhost', 'root', 's@ajeel', 'wms')
    result = obj
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.addProduct('finalizinfggg', '098098',
    #                         222, 333, 900, 300, 'new status')
    # result = obj.updateProduct(
    #     'finalizinfggg', '098098', 222, 333, 299, 300, 'Low stock', 22)
    # result = obj.getProduct(22, '098098')
    # result = obj.getAllProducts()
    # result = obj.deleteProduct(22, '098098')
    # result = obj.getStock(12)
    # result = obj.updateStock(12, 100)
    # print('Stock update: ', result)
    # result = obj.deleteProduct(12, '78B90')

    # result = obj.deleteProduct(19, '098098')
    # result = obj.deleteProduct(20, '098098')
    # result = obj.deleteProduct(21, '098098')
    # result = obj.getStock(12)
    # print(result)
