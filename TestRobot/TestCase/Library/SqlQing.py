import pymysql

from Config.project import dbHost, dbPort, dbName, dbUsername, dbPassword, dbCharset


class SqlQing(object):

    def __init__(self):
        pass

    @staticmethod
    def execute_sql(sql):  # 获取数据库的数据
        conn = pymysql.connect(host=dbHost, port=dbPort, db=dbName, user=dbUsername, passwd=dbPassword,
                               charset=dbCharset)
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()  # 搜取所有结果
        cur.close()
        conn.close()
        return results

    def getExamtypeIdFromExamtype(self, examtype):
        u'''
        根据考试类型中文名称获取数据库对应的id
        :param examtype: 自考,公共课（本）
        :return:
        '''
        examtype_list = str(examtype).split(',')
        parent = examtype_list[0]
        exam = examtype_list[1]

        sql = "SELECT id FROM `exam_type` WHERE primary_categories='" + parent + "'"
        query = self.execute_sql(sql)
        parentId = query[0][0]

        sql = "SELECT id FROM `exam_type` WHERE parent_id=" + str(parentId) + " and primary_categories='" + exam + "'"
        query = self.execute_sql(sql)
        examtypeId = query[0][0]

        return (parentId, examtypeId)

    def getSubjectIdFromSubjecttype(self, subjecttype):
        u'''
        根据科目类型中文名称获取数据库对应的id
        :param subjecttype: 自考,公共课（本）,中国近现代史纲要
        :return:
        '''
        subjecttype_list = str(subjecttype).split(',')
        parent = subjecttype_list[0]
        exam = subjecttype_list[1]
        subject = subjecttype_list[2]

        parentId, examtypeId = self.getExamtypeIdFromExamtype(parent + "," + exam)

        sql = "SELECT id FROM `subject` WHERE exam_type_id=" + str(examtypeId) + " and subject_name='" + subject + "'"
        query = self.execute_sql(sql)
        subjectId = query[0][0]

        return (parentId, examtypeId, subjectId)


if __name__ == '__main__':
    print(SqlQing().getSubjectIdFromSubjecttype('自考,公共课（本）,中国近现代史纲要'))
