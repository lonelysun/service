# -*- coding: utf-8 -*-
##############################################################################
#  COMPANY: BORN
#  AUTHOR: LH
#  EMAIL: arborous@gmail.com
#  VERSION : 1.0   NEW  2014/07/21
#  UPDATE : NONE
#  Copyright (C) 2011-2014 www.wevip.com All Rights Reserved
##############################################################################

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
import openerp
import time,datetime
import logging
import json
from mako import exceptions
from mako.lookup import TemplateLookup
import base64
import os
import werkzeug.utils

_logger = logging.getLogger(__name__)

#MAKO
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#服务APP
SER_THEME="defaultApp/views"
ser_path = os.path.join(BASE_DIR, "static", SER_THEME)
ser_tmp_path = os.path.join(ser_path, "tmp")
ser_lookup = TemplateLookup(directories=[ser_path],output_encoding='utf-8',module_directory=ser_tmp_path)

#动态切换数据库
def ensure_db(db='MAST',redirect='/except'):
    if not db:
        db = request.params.get('db')
 
    if db and db not in http.db_filter([db]):
        db = None
     
    if not db and request.session.db and http.db_filter([request.session.db]):
        db = request.session.db
         
    if not db:
        werkzeug.exceptions.abort(werkzeug.utils.redirect(redirect, 303))
    request.session.db = db


#获取模版信息
def serve_template(templatename, **kwargs):
    try:
        template = ser_lookup.get_template(templatename)
        return template.render(**kwargs)
    except:
        return exceptions.html_error_template().render()


#服务
class born_service(http.Controller):
    
    @http.route('/except', type='http', auth="none",)
    def Exception(self, **post):
        return serve_template('except.html')
    
    @http.route('/bornservice', type='http', auth="none")
    def toIndex(self,  **post):
        
        #切换数据库
        db = request.params.get('db')
        if not db:
            db = 'MAST'
        ensure_db(db)

        born_uuid=post.get('born_uuid',False)
        if not born_uuid:
            _logger.info(request.session.company_id)
            werkzeug.exceptions.abort(werkzeug.utils.redirect('/except', 303))

        company_obj = request.registry.get('res.company')
        company_res = company_obj.search(request.cr, SUPERUSER_ID, [('born_uuid','=',born_uuid)],context=request.context)
        company_id = company_res and company_res[0] or False
        
        if not company_id:
            werkzeug.exceptions.abort(werkzeug.utils.redirect('/except', 303))
        
        request.session.company_id=company_id
        company=company_obj.browse(request.cr, SUPERUSER_ID, company_id)
        
        return serve_template('index.html',company=company)
    

    #获取服务信息
    @http.route('/api/services', type='http', auth="none",)
    def services(self, **post):

        page_index=post.get('index',0)

        data = []
        if not request.session.company_id:
            _logger.info(request.session.company_id)
            werkzeug.exceptions.abort(werkzeug.utils.redirect('/except', 303))

        service_obj = request.registry.get('born.service')
        domain=[('state','=','done')]
        service_ids = service_obj.search(request.cr, SUPERUSER_ID, domain,int(page_index),10,order="sequence desc, id desc", context=request.context)
        for service in service_obj.browse(request.cr, SUPERUSER_ID,service_ids, context=request.context):

            time_format = datetime.datetime.strptime(service.create_date, '%Y-%m-%d %H:%M:%S')
            time_format = time_format.strftime('%y/%m/%d')

            if len(service.introduction )>15:
                introduction=service.introduction [0:15]+' ...'
            else:
                introduction=service.introduction

            if len(service.name )>10:
                name=service.name [0:10]+' ...'
            else:
                name=service.name

            val={
                 'name' : name or '',
                 'introduction' : introduction or '',
                 'image': service.image_url or '',
                 'id': service.id,
                 'create_date' : time_format,
            }
            data.append(val)
        return json.dumps(data,sort_keys=True)


    #已注册服务列表
    @http.route('/api/orders', type='http', auth="none",)
    def orders(self, **post):

        if not request.session.company_id:
            _logger.info(request.session.company_id)
            werkzeug.exceptions.abort(werkzeug.utils.redirect('/except', 303))
        data=[]

        business_obj = request.registry['born.business.line']
        business_ids = business_obj.search(request.cr, SUPERUSER_ID, [('company_id','=',request.session.company_id)],context=request.context)

        for business in business_obj.browse(request.cr, SUPERUSER_ID,business_ids, context=request.context):
            if business.approved_date:
                time_format = datetime.datetime.strptime(business.approved_date, '%Y-%m-%d')
                time_format = time_format.strftime('%y/%m/%d')
            else:
                time_format=''

            if len(business.service_id.introduction )>15:
                introduction=business.service_id.introduction [0:15]+' ...'
            else:
                introduction=business.service_id.introduction

            if business.state == 'draft':
                state_display=u'待审核'
            elif business.state == 'done':
                state_display=u'待付款'
            elif business.state == 'in':
                state_display=u'已生效'
            elif business.state == 'failed':
                state_display=u'审核未通过'
            elif business.state == 'cancel':
                state_display=u'已取消'

            val={
                 'name': business.service_id.name,
                 'introduction': introduction,
                 'image': business.service_id.image_url or '',
                 'service_id': business.service_id.id,
                 'approved_date': time_format,
                 'id': business.id,
                 'state':business.state,
                 'state_display':state_display,

            }
            data.append(val)

        print(data)
        return json.dumps(data,sort_keys=True)


    #获取全部文章列表
    @http.route('/api/contents', type='http', auth="none")
    def contents(self, **post):

        page_index=post.get('index',0)

        data=[]
        content_obj = request.registry.get('born.content')
        domain=[('type','=','infomation')]
        content_ids = content_obj.search(request.cr, SUPERUSER_ID, domain,int(page_index),10,order="sequence desc, id desc", context=request.context)
        for content in content_obj.browse(request.cr, SUPERUSER_ID,content_ids,context=request.context):
            time_format = datetime.datetime.strptime(content.create_date, '%Y-%m-%d %H:%M:%S')
            time_format = time_format.strftime('%y/%m/%d')
            val = {
               'id': content.id,
               'name': content.name,
               'create_date': time_format,
               'image': content.image_url or '',
               'flow':content.flow,
            }
            data.append(val)
        return json.dumps(data,sort_keys=True)


    #获取服务详细信息
    @http.route('/api/services/<int:id>',type='http',auth="none")
    def service(self, id, **post):

        if not request.session.company_id or not id or id<=0:
            _logger.info(request.session.company_id)
            werkzeug.exceptions.abort(werkzeug.utils.redirect('/except', 303))

        #获取服务详细信息
        service_obj = request.registry.get('born.service')
        service=service_obj.browse(request.cr, SUPERUSER_ID,int(id),context=request.context)
        contents = []

        #遍历服务的文章列表
        for content in service.contents_ids:
            content_date = datetime.datetime.strptime(content.create_date, '%Y-%m-%d %H:%M:%S')
            content_date = content_date.strftime('%y/%m/%d')

            if len(content.name)>12:
                name=content.name[0:12]+' ...'
            else:
                name=content.name

            val = {
               'id': content.id,
               'name': name,
               'create_date' : content_date,
               'image': content.image_url or '',
            }
            contents.append(val)

        #获取服务信息
        service_date = datetime.datetime.strptime(service.create_date, '%Y-%m-%d %H:%M:%S')
        service_date = service_date.strftime('%y/%m/%d')

        #验证该商户是否已经注册了该服务
        already_register=False
        obj_business = request.registry['born.business.line']
        domain = [('state','in',('draft','done','in')),('service_id','=',int(id)),('company_id','=',int(request.session.company_id))]
        res=obj_business.search(request.cr, SUPERUSER_ID, domain, context=request.context)
        if res:
            already_register=True

        if not service.is_regiest:
            already_register=True

        data={
            'contents':contents,
            'name' : service.name or '',
            'introduction' :service.introduction or '',
            'describe' :service.describe or '',
            'image': service.image_url or '',
            'id': service.id,
            'create_date': service_date,
            'is_regiest': service.is_regiest,
            'price': service.price,
            'type': service.type,
            'num': service.num,
            'days': service.days,
            'already_register':already_register,
        }
        return json.dumps(data,sort_keys=True)
        

    #获取文章
    @http.route('/api/contents/<int:id>',type='http',auth="none")
    def content(self, id, **post):

        if not request.session.company_id or id<=0:
            _logger.info(request.session.company_id)
            werkzeug.exceptions.abort(werkzeug.utils.redirect('/except', 303))

        content_obj = request.registry.get('born.content')
        content = content_obj.browse(request.cr, SUPERUSER_ID,id,context=request.context)
        data = {
            'name': content.name,
            'create_date': content.create_date,
            'content': content.content,
            'flow':content.flow,
        }

        sql=u""" update  born_content set flow=flow+1 where id=%s """ % (id,)
        request.cr.execute(sql)

        return json.dumps(data,sort_keys=True)

     #获取文章
    @http.route('/api/orders/<int:id>',type='http',auth="none")
    def order(self, id, **post):

        if not request.session.company_id or id<=0:

            _logger.info(request.session.company_id)
            werkzeug.exceptions.abort(werkzeug.utils.redirect('/except', 303))

        order_obj = request.registry.get('born.business.line')
        order = order_obj.browse(request.cr, SUPERUSER_ID,int(id),context=request.context)

        records=[]
        for x in order.line_ids:
            val = {
                'employee_id':x.employee_id.id,
                'employee_name':x.employee_id.name,
                'company_id' :x.company_id.id,
                'company_name' :x.company_id.name,
                'result': x.result,
                'start_date': x.start_date,
                'end_date': x.end_date,
                'state': x.state,
            }
            records.append(val)

        pays=[]
        for x in order.pay_ids:

            if x.state == 'draft':
                state_display=u'待付款'
            elif x.state == 'done':
                state_display=u'已付款'

            if x.pay_method == 'weixin':
                pay_method_name=u'微信'
            elif x.pay_method == 'alipay':
                pay_method_name=u'支付宝'
            elif x.pay_method == 'cash':
                pay_method_name=u'现金'
            elif x.pay_method == 'bank':
                pay_method_name=u'银行卡'
            else:
                pay_method_name=u'其他'

            val = {
                'name':x.name,
                'company_id' :x.company_id.id,
                'customer_name':x.customer_name,
                'company_name' :x.company_id.name,
                'out_trade_no':x.out_trade_no,
                'account':x.account,
                'pay_date': x.pay_date,
                'amount':x.amount,
                'pay_method': x.pay_method,
                'pay_method_name': pay_method_name,
                'state': x.state,
                'state_display': state_display,
                'remark': x.remark,
            }
            pays.append(val)

        if order.state == 'draft':
            state_display=u'待审核'
        elif order.state == 'done':
            state_display=u'待付款'
        elif order.state == 'in':
            state_display=u'已生效'
        elif order.state == 'failed':
            state_display=u'审核未通过'
        elif order.state == 'cancel':
            state_display=u'已取消'

        data = {
            'name': order.name,
            'service_image': order.service_id.image_url or '',
            'create_date': order.create_date,
            'company_id': order.company_id.id,
            'company_name': order.company_id.name,
            'customer_name': order.customer_name,
            'phone':  order.phone,
            'service_id':  order.service_id.id,
            'service_name':  order.service_id.name,
            'service_introduction':  order.service_id.introduction,
            'num': order.num,
            'days': order.days,
            'price': order.price,
            'type': order.service_id.type,
            'expiration_date':  order.expiration_date or '',
            'approved_date':  order.approved_date or '',
            'state': order.state,
            'state_display':state_display,
            'employee_id': order.employee_id.id,
            'employee_name': order.employee_id.name or '',
            'remark': order.remark,
            'records': records,
            'pays': pays,
        }
        return json.dumps(data,sort_keys=True)


    #获取用户详细信息
    @http.route('/api/account/<int:id>', type='http', auth="none",)
    def account_info(self,id, **post):

        if not request.session.company_id or id<=0 :
            werkzeug.exceptions.abort(werkzeug.utils.redirect('/except', 303))

        #获取公司信息
        company=request.registry['res.company'].browse(request.cr, SUPERUSER_ID, int(request.session.company_id))
        service_obj = request.registry.get('born.service')
        service=service_obj.browse(request.cr, SUPERUSER_ID,int(id),context=request.context)
        data={
            'company_id': company.id,
            'company_name': company.name,
            'customer_name': company.contact_name or '',
            'phone': company.phone or '',
            'service_id':service.id,
            'service_name':service.name,
        }
        return json.dumps(data,sort_keys=True)


    #提交注册用户信息
    @http.route('/api/register', type='http', auth="none")
    def register(self, **post):

        if not request.session.company_id:
            werkzeug.exceptions.abort(werkzeug.utils.redirect('/except', 303))

        obj_business = request.registry['born.business.line']
        val = {
            'company_id': int(request.session.company_id),
            'customer_name': post.get('customer_name',False),
            'phone': post.get('phone',False),
            'state': 'done',
            'service_id': post.get('service_id',False),
        }

        line_id = obj_business.create(request.cr,SUPERUSER_ID,val)
        data = {
            'id':line_id,
        }
        return json.dumps(data,sort_keys=True)