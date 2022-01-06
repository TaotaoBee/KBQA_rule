#!/usr/bin/env python3
# coding: utf-8
from py2neo import Graph

GRAPH = Graph("bolt://127.0.0.1:7687", user="neo4j", password="001231")


class AnswerSearcher:
    def __init__(self):
        self.graph = GRAPH
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.graph.run(query).data()
                answers += ress
            print(answers)
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        elif question_type == 'stockid_conceptget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.stock_name']
            final_answer = '{0} {1}的所属概念是：{2}'.format(subject1, subject2, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'stockname_conceptget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.stock_name']
            final_answer = '{0} {1}的所属概念是：{2}'.format(subject1, subject2, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'concept_stockget':
            desc = [i['m.stock_id'] + ' ' + i['m.stock_name'] for i in answers]
            length = len(answers[0])
            list_subject = []
            if length > 2:
                for i in range(2, length):
                    list_subject.append(answers[0]['n#i#.name'.replace('#i#', str(i-2))])
            subject = "、".join(list_subject)
            final_answer = '属于{0}概念的股票有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'stockid_controllerget':
            desc = [i['n.name'] + '(' + i['n.type'] + ')' for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.stock_name']
            final_answer = '{0} {1}的实际控制人是：{2}'.format(subject1, subject2, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'stockname_controllerget':
            desc = [i['n.name'] + '(' + i['n.type'] + ')' for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.stock_name']
            final_answer = '{0} {1}的实际控制人是：{2}'.format(subject1, subject2, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'controller_stockget':
            desc = [i['m.stock_id'] + ' ' + i['m.stock_name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}作为实际控股人有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'stockid_industryget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.stock_name']
            final_answer = '{0} {1}的所属行业是：{2}'.format(subject1, subject2, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'stockname_industryget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.stock_name']
            final_answer = '{0} {1}的所属行业是：{2}'.format(subject1, subject2, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'industry_stockget':
            desc = [i['m.stock_id'] + ' ' + i['m.stock_name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '属于{0}行业的股票有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'stockid_markettypeget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.stock_name']
            final_answer = '{0} {1}的市场类型是：{2}'.format(subject1, subject2, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'stockname_markettypeget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.stock_name']
            final_answer = '{0} {1}的市场类型是：{2}'.format(subject1, subject2, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'markettype_stockget':
            desc = [i['m.stock_id'] + ' ' + i['m.stock_name'] for i in answers]
            length = len(answers[0])
            list_subject = []
            if length > 2:
                for i in range(2, length):
                    list_subject.append(answers[0]['n#i#.name'.replace('#i#', str(i-2))])
            subject = "、".join(list_subject)
            final_answer = '属于{0}的股票有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
    query = "MATCH ()"
    ress = GRAPH.run(query).data()
    print(ress)