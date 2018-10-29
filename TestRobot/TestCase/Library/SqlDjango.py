import pymysql

from Config.django import dbhost, dbport, dbname, dbusername, dbpassword, dbcharset


class SqlDjango(object):

    def __init__(self):
        pass

    @staticmethod
    def execute_sql(sql):  # 获取数据库的数据
        conn = pymysql.connect(host=dbhost, port=dbport, db=dbname, user=dbusername, passwd=dbpassword,
                               charset=dbcharset)
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()  # 搜取所有结果
        cur.close()
        conn.close()
        return results

    def getParams(self, caseid, businessname):
        sql = 'SELECT id FROM `business` WHERE del_flag=0 AND `name`="' + businessname + '"'
        query = self.execute_sql(sql)
        businessid = query[0][0]

        sql = 'SELECT id,user_id FROM `case_business` WHERE del_flag=0 AND case_id=' + str(
            caseid) + ' AND bus_id=' + str(businessid)
        query = self.execute_sql(sql)
        user_id = query[0][1]
        casebddtobusiness_id = query[0][0]

        sql = 'SELECT b.`name`,a.`value` FROM `data` a INNER JOIN `variable` b WHERE a.variable_id=b.id AND a.id = (SELECT data_id  FROM`case_business_param`  WHERE casebddtobusiness_id=' + str(
            casebddtobusiness_id) + ')'
        query = self.execute_sql(sql)
        param_dict = {}
        for p in query:
            param_dict.update({p[0]: p[1]})

        sql = 'SELECT `name` FROM `variable` WHERE id in (SELECT var_id FROM `business_variable` WHERE bus_id=' + str(
            businessid) + ' ORDER BY sort)'
        query = self.execute_sql(sql)

        variables = [v[0] for v in query]
        param = [user_id]
        for var in variables:
            param.append(param_dict.get(var, 'error'))

        return set(param)


if __name__ == '__main__':
    print(SqlDjango().getParams(1, 'ChangeType'))
