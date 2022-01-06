#!/usr/bin/env python3
# coding: utf-8


class QuestionParser():
    def __init__(self, pDate):
        self.pDate = 'Stock' + pDate

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []

            if  question_type == 'stockid_conceptget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockid'))

            elif question_type == 'stockname_conceptget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockname'))

            elif question_type == 'concept_stockget':
                sql = self.sql_transfer(question_type, entity_dict.get('concept'))

            elif question_type == 'stockid_controllerget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockid'))

            elif question_type == 'stockname_controllerget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockname'))

            elif question_type == 'controller_stockget':
                sql = self.sql_transfer(question_type, entity_dict.get('controller'))

            elif question_type == 'stockid_industryget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockid'))

            elif question_type == 'stockname_industryget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockname'))

            elif question_type == 'industry_stockget':
                sql = self.sql_transfer(question_type, entity_dict.get('industry'))

            elif question_type == 'stockid_indextypeget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockid'))

            elif question_type == 'stockname_indextypeget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockname'))

            elif question_type == 'stockid_markettypeget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockid'))

            elif question_type == 'stockname_markettypeget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockname'))

            elif question_type == 'markettype_stockget':
                sql = self.sql_transfer(question_type, entity_dict.get('markettype'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''转换成Cypher语句'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            print('in not entities\n')
            return []

        print(entities)

        # 查询语句
        sql = []

        # 按股票代码查询所属概念
        if question_type == 'stockid_conceptget':
            sql = ["MATCH (m:{0})-[r:ConceptInvolved]->(n:Concept) where m.stock_code = '{1}' return m.stock_id, m.sotck_name, r.name, n.name".format(self.pDate, i) for i in entities]

        # 按股票名称查询所属概念
        elif question_type == 'stockname_conceptget':
            sql = ["MATCH (m:{0})-[r:ConceptInvolved]->(n:Concept) where m.stock_name = '{1}' return m.stock_id, m.stock_name, r.name, n.name".format(self.pDate, i) for i in entities]

        # 根据概念查股
        elif question_type == 'concept_stockget':
            length = len(entities)
            part1_list = []
            part2_list = []
            part3_list = []
            for i in range(length):
                part1_list.append("(m:{0})-[r#i#:ConceptInvolved]->(n#i#:Concept)".format(self.pDate).replace('#i#', str(i)))
                part2_list.append("n#i#.name = '{0}'".format(entities[i]).replace('#i#', str(i)))
                part3_list.append("n#i#.name".replace('#i#', str(i)))
            part1 = ",".join(part1_list)
            part2 = " and ".join(part2_list)
            part3 = ','.join(part3_list)
            sql = ["MATCH #part1# where #part2# return m.stock_id, m.stock_name, #part3#".replace('#part1#', part1).replace('#part2#', part2).replace('#part3#', part3)]
            #sql = ["MATCH (m:{0})-[r:ConceptInvolved]->(n:Concept) where n.name = '{1}' return m.stock_id, m.stock_name, n.name".format(self.pDate, i) for i in entities]

        # 按股票代码查询实际控制人
        elif question_type == 'stockid_controllerget':
            sql = ["MATCH (m:{0})-[r:IsControlledBy]->(n:Controller) where m.stock_id = '{1}' return m.stock_id, m.sotck_name, r.name, n.name, n.type".format(self.pDate, i) for i in entities]

        # 按股票名称查询实际控制人
        elif question_type == 'stockname_controllerget':
            sql = ["MATCH (m:{0})-[r:IsControlledBy]->(n:Controller) where m.stock_name = '{1}' return m.stock_id, m.stock_name, r.name, n.name, n.type".format(self.pDate, i) for i in entities]

        # 根据实际控制人查股
        elif question_type == 'controller_stockget':
            sql = ["MATCH (m:{0})-[r:IsControlledBy]->(n:Controller) where n.name = '{1}' return m.stock_id, m.stock_name, n.name".format(self.pDate, i) for i in entities]

        # 按股票代码查询所属行业
        elif question_type == 'stockid_industryget':
            sql = ["MATCH (m:{0})-[r:IndustryInvolved]->(n:Industry) where m.stock_id = '{1}' return m.stock_id, m.stock_name, r.name, n.name".format(self.pDate, i) for i in entities]

        # 按股票名称查询所属行业
        elif question_type == 'stockname_industryget':
            sql = ["MATCH (m:{0})-[r:IndustryInvolved]->(n:Industry) where m.stock_id = '{1}' return m.stock_id, m.stock_name, r.name, n.name".format(self.pDate, i) for i in entities]

        # 按行业查询股票
        elif question_type == 'industry_stockget':
            sql = ["MATCH (m:{0})-[r:IndustryInvolved]->(n:Industry) where n.name = '{1}' return m.stock_name, n.name".format(self.pDate, i) for i in entities]

        # 查市场类型
        elif question_type == 'stockid_markettypeget':
            sql = ["MATCH (m:{0})-[r:MarketTypeIs]->(n:MarketType) where m.stock_id = '{1}' return m.stock_id, " \
                   "m.stock_name, n.name".format(self.pDate, i) for i in entities]

        elif question_type == 'stockname_markettypeget':
            sql = ["MATCH (m:{0})-[r:MarketTypeIs]->(n:MarketType) where m.stock_name = '{1}' return m.stock_id, " \
                   "m.stock_name, n.name".format(self.pDate, i) for i in entities]

        elif question_type == 'markettype_stockget':
            length = len(entities)
            part1_list = []
            part2_list = []
            part3_list = []
            for i in range(length):
                part1_list.append("(m:{0})-[r#i#:MarketTypeIs]->(n#i#:MarketType)".format(self.pDate).replace('#i#', str(i)))
                part2_list.append("n#i#.name = '{0}'".format(entities[i]).replace('#i#', str(i)))
                part3_list.append("n#i#.name".replace('#i#', str(i)))
            part1 = ",".join(part1_list)
            part2 = " and ".join(part2_list)
            part3 = ','.join(part3_list)
            sql = ["MATCH #part1# where #part2# return m.stock_id, m.stock_name, #part3#".replace('#part1#', part1).replace('#part2#', part2).replace('#part3#', part3)]

        return sql

if __name__ == '__main__':
    handler = QuestionParser()
