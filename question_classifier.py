#!/usr/bin/env python3
# coding: utf-8

import os
import ahocorasick


class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])

        # 股票特征词路径
        self.stockid_path = os.path.join(cur_dir, 'my_stock_dict/stockid.txt')
        self.stockname_path = os.path.join(cur_dir, 'my_stock_dict/stockname.txt')
        self.concept_path = os.path.join(cur_dir, 'my_stock_dict/concept.txt')
        self.controller_path = os.path.join(cur_dir, 'my_stock_dict/controller.txt')
        self.industry_path = os.path.join(cur_dir, 'my_stock_dict/industry.txt')
        self.marketype_path = os.path.join(cur_dir, 'my_stock_dict/marketype.txt')
        self.nationality_path = os.path.join(cur_dir, 'my_stock_dict/nationality.txt')
        self.province_path = os.path.join(cur_dir, 'my_stock_dict/province.txt')
        self.city_path = os.path.join(cur_dir, 'my_stock_dict/city.txt')
        self.topmanager_path = os.path.join(cur_dir, 'my_stock_dict/topmanager.txt')

        # 加载特征词
        self.stockid_wds = [i.strip() for i in open(self.stockid_path, encoding='utf-8') if i.strip()]
        self.stockname_wds = [i.strip() for i in open(self.stockname_path, encoding='utf-8') if i.strip()]
        self.concept_wds = [i.strip() for i in open(self.concept_path, encoding='utf-8') if i.strip()]
        self.controller_wds = [i.strip() for i in open(self.controller_path, encoding='utf-8') if i.strip()]
        self.industry_wds = [i.strip() for i in open(self.industry_path, encoding='utf-8') if i.strip()]
        self.marketype_wds = [i.strip() for i in open(self.marketype_path, encoding='utf-8') if i.strip()]
        self.nationality_wds = [i.strip() for i in open(self.nationality_path, encoding='utf-8') if i.strip()]
        self.province_wds = [i.strip() for i in open(self.province_path, encoding='utf-8') if i.strip()]
        self.city_wds = [i.strip() for i in open(self.city_path, encoding='utf-8') if i.strip()]
        self.topmanager_wds = [i.strip() for i in open(self.topmanager_path, encoding='utf-8') if i.strip()]
        self.stock_region_words = set(self.stockid_wds + self.stockname_wds + self.concept_wds +
            self.controller_wds + self.industry_wds + self.marketype_wds + self.nationality_wds +
            self.province_wds + self.city_wds + self.topmanager_wds)

        # 构造领域actree
        self.stock_region_tree = self.build_actree(list(self.stock_region_words))
        # 构建词典
        self.stock_wdtype_dict = self.build_wdtype_my_stock_dict()
        # 问句疑问词
        #【0】概念
        self.concept_qwds = ['所属概念', '什么概念', '概念类别', '概念是什么', '啥概念', '概念是啥', '嘛概念', '神马概念', '概念']
        #【1】实际控股人
        self.controller_qwds = ['是谁', '控制', '大股东', '股东', '老板', '控股人']
        #【2】行业
        self.industry_qwds = ['所属行业', '什么行业', '行业是什么', '行业是啥', '啥行业', '嘛行业', '行业类别', '行业']
        #【3】市场类型
        self.marketype_qwds = ['市场类型', '股票市场'] #属于什么市场
        #【4】国籍
        self.nationality_qwds = ['国籍']
        #【5】高管
        self.topmanager_qwds = ['高管', '经理', 'CEO']

        self.stock_belong_qwds = ['属于', '所属', '拥有', '包含', '含有']
        self.performance_qwds = ['好不好', '好吗', '牛逼', '牛', '厉害', '蓝筹', '牛股', '怎样', '如何', '好么', '牛不', '屌']
        self.common_qwds = ['指标', '特性', '形态', '表现']

        print('model init finished ......')
        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        my_stock_dict = self.check_stock(question)
        if not my_stock_dict:
            return {}
        data['args'] = my_stock_dict
        #收集问句当中所涉及到的实体类型
        types = []

        for type_ in my_stock_dict.values():
            types += type_

        question_type = 'others'
        question_types = []

        # 股票查概念
        if self.check_words(self.concept_qwds, question) and 'stockid' in types:
            question_type = 'stockid_conceptget'
            question_types.append(question_type)

        if self.check_words(self.concept_qwds, question) and 'stockname' in types:
            question_type = 'stockname_conceptget'
            question_types.append(question_type)

        # 概念查股
        if self.check_words(self.concept_qwds, question) and 'concept' in types:
            question_type = 'concept_stockget'
            question_types.append(question_type)

        # 控制人查询
        if self.check_words(self.controller_qwds, question) and 'stockid' in types:
            question_type = 'stockid_controllerget'
            question_types.append(question_type)

        if self.check_words(self.controller_qwds, question) and 'stockname' in types:
            question_type = 'stockname_controllerget'
            question_types.append(question_type)

        # 根据控制人查股
        if self.check_words(self.controller_qwds, question) and 'controller' in types:
            question_type = 'controller_stockget'
            question_types.append(question_type)

        # 股票查行业
        if self.check_words(self.industry_qwds, question) and 'stockid' in types:
            question_type = 'stockid_industryget'
            question_types.append(question_type)

        if self.check_words(self.industry_qwds, question) and 'stockname' in types:
            question_type = 'stockname_industryget'
            question_types.append(question_type)

        # 行业查股
        if self.check_words(self.industry_qwds+self.stock_belong_qwds, question) and 'industry' in types:
            question_type = 'industry_stockget'
            question_types.append(question_type)

        # 查询市场类型
        if self.check_words(self.marketype_qwds, question) and 'stockid' in types:
            question_type = 'stockid_markettypeget'
            question_types.append(question_type)

        if self.check_words(self.marketype_qwds, question) and 'stockname' in types:
            question_type = 'stockname_markettypeget'
            question_types.append(question_type)

        # 根据市场类型查股
        if self.check_words(self.marketype_qwds + self.stock_belong_qwds, question) and 'markettype' in types:
            question_type = 'markettype_stockget'
            question_types.append(question_type)

        # 高管姓名查询
        if self.check_words(self.topmanager_wds, question) and 'stockid' in types:
            question_type = 'stockid_topmanagerget'
            question_types.append(question_type)

        if self.check_words(self.topmanager_wds, question) and 'stockname' in types:
            question_type = 'stockname_topmanagerget'
            question_types.append(question_type)

        if question_types == [] and 'sensitive' in types:
            question_types = ['sensitive']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''

    def build_wdtype_my_stock_dict(self):
        wd_dict = dict()
        for wd in self.stock_region_words:
            wd_dict[wd] = []
            if wd in self.stockid_wds:
                wd_dict[wd].append('stockid')
            if wd in self.stockname_wds:
                wd_dict[wd].append('stockname')
            if wd in self.concept_wds:
                wd_dict[wd].append('concept')
            if wd in self.controller_wds:
                wd_dict[wd].append('controller')
            if wd in self.industry_wds:
                wd_dict[wd].append('industry')
            if wd in self.marketype_wds:
                wd_dict[wd].append('marketype')
            if wd in self.nationality_wds:
                wd_dict[wd].append('nationality')
            if wd in self.city_wds:
                wd_dict[wd].append('city')
            if wd in self.province_wds:
                wd_dict[wd].append('province')
            if wd in self.topmanager_wds:
                wd_dict[wd].append('topmanager')

        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''股票问句过滤'''
    def check_stock(self, question):
        region_wds = []
        for i in self.stock_region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1) # 停用词
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.stock_wdtype_dict.get(i) for i in final_wds}
        print(final_dict)
        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)