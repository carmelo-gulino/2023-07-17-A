from database.DB_connect import DBConnect
from model.product import Product


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_colors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct gp.Product_color color from go_products gp order by gp.Product_color """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['color'])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_nodes(color):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from go_products gp where gp.Product_color = %s"""
        cursor.execute(query, (color, ))
        result = []
        for row in cursor:
            result.append(Product(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_n_sales(year, p1_number, p2_number):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select count(distinct gds2.`Date`) peso
                    from go_daily_sales gds , go_daily_sales gds2 
                    where gds2.Retailer_code = gds.Retailer_code
                    and gds2.`Date` = gds.`Date` and year(gds2.`Date`) = %s
                    and gds.Product_number = %s and gds2.Product_number = %s"""
        cursor.execute(query, (year, p1_number, p2_number))
        result = None
        for row in cursor:
            result = row['peso']
        cursor.close()
        cnx.close()
        return result
