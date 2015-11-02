# -*- coding: utf-8 -*-
##############################################################################
#  COMPANY: BORN
#  AUTHOR: LH
#  EMAIL: arborous@gmail.com
#  VERSION : 1.0   NEW  2014/07/21
#  UPDATE : NONE
#  Copyright (C) 2011-2014 www.wevip.com All Rights Reserved
##############################################################################

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from tool.s3client import s3client

try:
    from openerp import SUPERUSER_ID
except ImportError:
    SUPERUSER_ID = SUPERUSER_ID


#文章分类
class content_category(osv.osv):
    _name = "content.category"
    _columns = {
        'name': fields.char('名称', required=True),
    }

#文章
class born_content(osv.osv):
    _name = "born.content"
    _columns = {
        'name' : fields.char(u'标题',required=True),
        'image' : fields.binary(u'图片'),
        'image_url':fields.text(u'图片地址',help=u"S3图片地址"),
        'file_name':fields.char(u'文件名称',size=255,help=u"文件名称"),
        'content' : fields.text(u'文章内容',required=True),
        'category_id' : fields.many2one('content.category',u'文章分类'),
        'state' : fields.selection([('draft', u'草稿'), ('done', u'已审核'),('cancel', u'已取消')], u'状态', ),
        'sequence': fields.integer(u'排序'),
        'flow': fields.integer(u'浏览数'),
        'type' : fields.selection([('service', u'服务说明'), ('infomation', u'动态信息'),('adv', u'广告'),('notice', u'通知'),('other', u'其他')], u'文章类型', ),
    }

    _defaults = {
        'state': lambda *a: 'draft',
        'sequence':0,
        'flow':0,
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('image',False):

            s3 =s3client(self)
            image_url=s3.upload(cr,uid,vals.get('image'),vals.get('file_name','image.png'))
            vals['image_url']=image_url

        #本地保存
        return super(born_content, self).create(cr, uid, vals, context=context)

    #修改
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('image',False):
            s3 = s3client(self)
            image_url=s3.upload(cr,uid,vals.get('image'),vals.get('file_name','image.png'))
            vals['image_url']=image_url

        return super(born_content, self).write(cr, uid, ids, vals, context=context)

    #审核
    def draft_to_done(self, cr, uid, ids, context={}):
        state = 'done'
        self.write(cr, uid, ids, {'state': state})
        return True

    #取消
    def done_to_cancel(self, cr, uid, ids, context={}):
        state = 'cancel'
        self.write(cr, uid, ids, {'state': state})
        return True

    def cancel_to_draft(self, cr, uid, ids, context={}):
        state = 'draft'
        self.write(cr, uid, ids, {'state': state})
        return True


#服务
class born_service(osv.osv):
    _name = "born.service"

    _columns = {
        'name': fields.char(u'名称'),
        'image' : fields.binary(u'图片'),
        'image_url':fields.text(u'图片地址',help=u"S3图片地址"),
        'file_name':fields.char(u'文件名称',size=255,help=u"文件名称"),
        'introduction': fields.char(u'简介'),
        'describe': fields.text(u'描述'),
        'is_regiest': fields.boolean(u'是否需要登记注册'),
        'regiest_url': fields.char(u'注册地址'),
        'price': fields.float(u'价格',help=u'购买此服务的价格',digits_compute=dp.get_precision('Account')),
        'type': fields.selection([('days', '天数计'),('num','次数计')], '计费模式'),
        'num': fields.integer(u'次数'),
        'days': fields.integer(u'天数'),
        'state': fields.selection([('draft', u'草稿'), ('done', u'已发布'),('cancel', u'已下线')], u'状态', ),
        'business_ids': fields.one2many('born.business.line','service_id',u'已登记的商家'),
        'contents_ids': fields.many2many('born.content','res_service_content_rel','s_id','cid',u'文章列表'),
        'sequence': fields.integer(u'排序'),
    }

    _defaults = {
        'type': 'num',
        'state':'draft',
        'sequence':0,
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('image',False):

            s3 =s3client(self)
            image_url=s3.upload(cr,uid,vals.get('image'),vals.get('file_name','image.png'))
            vals['image_url']=image_url

        #本地保存
        return super(born_service, self).create(cr, uid, vals, context=context)

    #修改
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('image',False):
            s3 = s3client(self)
            image_url=s3.upload(cr,uid,vals.get('image'),vals.get('file_name','image.png'))
            vals['image_url']=image_url

        return super(born_service, self).write(cr, uid, ids, vals, context=context)

    #审核
    def draft_to_done(self, cr, uid, ids, context={}):
        state = 'done'
        self.write(cr, uid, ids, {'state': state})
        return True

    #取消
    def done_to_cancel(self, cr, uid, ids, context={}):
        state = 'cancel'
        self.write(cr, uid, ids, {'state': state})
        return True

    def cancel_to_draft(self, cr, uid, ids, context={}):
        state = 'draft'
        self.write(cr, uid, ids, {'state': state})
        return True

#已注册商户
class born_business_line(osv.osv):
    _name = "born.business.line"

    _columns = {
        'name': fields.char(u'服务号',required=True),
        'company_id': fields.many2one("res.company",u'公司',required=True),
        'customer_name': fields.char(u'申请人',required=True),
        'phone': fields.char(u'联系电话',required=True),
        'service_id': fields.many2one("born.service",u'注册服务',required=True,ondelete='cascade',),
        'price': fields.related("service_id", "price",type="float",  string=u"价格",store=True ),
        'num': fields.related("service_id", "num",type="integer",  string=u"总次数",store=True ),
        'days': fields.related("service_id", "days",type="integer",  string=u"总天数" ,store=True),
        'expiration_date': fields.date(u'过期日期'),
        'approved_date': fields.date(u'生效日期'),
        'state': fields.selection([('draft', u'待审核'),
                                    ('done', u'已审核，待付款'),
                                    ('in', u'已生效'),
                                    ('gone', u'已过期'),
                                    ('failed', u'审核未通过'),
                                    ('cancel', u'已取消')], u'状态', ),
        'employee_id':fields.many2one('hr.employee', u'服务担当'),
        'remark': fields.text(u'备注'),
        'line_ids': fields.one2many('born.service.record','business_id',u'服务履历'),
        'pay_ids': fields.one2many('born.pay.line','business_id',u'付款履历'),
    }

    _defaults = {
        'state': lambda *a: 'draft',
        'name':'/',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/' :
            vals['name'] ='%s%s' % ('SE', self.pool.get('ir.sequence').get(cr, uid, 'service.no') or '/')

        return super(born_business_line, self).create(cr, uid, vals, context=context)

    #删除
    def unlink(self, cr, uid, ids,context=None):
        state = self.read(cr, uid, ids, ['state'], context=context)[0]["state"]
        if state in('cancel','draft'):
            return osv.osv.unlink(self, cr, uid, ids)
        else:
            raise osv.except_osv(u'系统警告',u'已生效服务不能删除! ')

    def regiest_pass(self, cr, uid, ids, context={}):
        state = 'done'
        self.write(cr, uid, ids, {'state': state})
        return True

    def regiest_notpass(self, cr, uid, ids, context={}):
        state = 'failed'
        self.write(cr, uid, ids, {'state': state})
        return True

    def regiest_pay(self, cr, uid, ids, context={}):
        state = 'in'
        self.write(cr, uid, ids, {'state': state})
        return True

    def regiest_gone(self, cr, uid, ids, context={}):
        state = 'gone'
        self.write(cr, uid, ids, {'state': state})
        return True

    def regiest_repay(self, cr, uid, ids, context={}):
        state = 'in'
        self.write(cr, uid, ids, {'state': state})
        return True

    def regiest_cancel(self, cr, uid, ids, context={}):
        state = 'cancel'
        self.write(cr, uid, ids, {'state': state})
        return True


#服务记录
class born_service_record(osv.osv):
    _name = 'born.service.record'
    _columns = {
        'business_id': fields.many2one('born.business.line', u'服务', ondelete='cascade',required=True ),
        'employee_id':fields.many2one('hr.employee', u'服务担当',required=True),
        'company_id' : fields.related('business_id','company_id',type='many2one', relation='res.company', string=u"公司" ),
        'demand': fields.text(u'需求',required=True),
        'result': fields.text(u'处理结果'),
        'start_date': fields.date(u'处理开始日期'),
        'end_date': fields.date(u'处理结束日期'),
        'state': fields.selection([('draft', u'草稿'), ('doing', u'处理中'),('success', u'处理成功'),('faild', u'处理失败')], u'状态', ),
    }

    def draft_to_doing(self, cr, uid, ids, context={}):
        state = 'doing'
        self.write(cr, uid, ids, {'state': state})
        return True

    def doing_to_success(self, cr, uid, ids, context={}):
        state = 'success'
        self.write(cr, uid, ids, {'state': state})
        return True

    def doing_to_faild(self, cr, uid, ids, context={}):
        state = 'faild'
        self.write(cr, uid, ids, {'state': state})
        return True

    _defaults = {
        'state': lambda *a: 'draft',
    }
#付款记录
class born_pay_line(osv.osv):
    _name = 'born.pay.line'
    _columns = {
        'name':fields.char(u'订单号',size=255,help=u"支付订单号",required=True),
        'business_id': fields.many2one('born.business.line', u'服务',required=True ,ondelete='cascade',),
        'company_id' : fields.related('business_id','company_id',type='many2one', relation='res.company', string=u"公司" ),
        'customer_name':fields.char(u'付款人',size=255,help=u"付款人",required=True),
        'out_trade_no':fields.char(u'流水号',size=255,help=u"流水号",required=True),
        'account':fields.char(u'收款账号',size=255,help=u"收款账号",required=True),
        'pay_date': fields.date(u'付款完成日期'),
        'amount':fields.float(u'金额',digits_compute=dp.get_precision('Account')),
        'pay_method': fields.selection([
            ('weixin', u'微信'),
            ('alipay', u'支付宝'),
            ('cash', u'现金'),
            ('bank', u'银行卡'),
            ('other', u'其他'),
            ], u'支付方式',  help=u'支付方式', select=True),
        'state': fields.selection([('draft', u'草稿'), ('done', u'已付款')], u'状态', ),
        'remark': fields.text(u'备注'),
    }

    _defaults = {
        'state': lambda *a: 'draft',
        'name':'/',
    }

    #审核
    def draft_to_done(self, cr, uid, ids, context={}):
        state = 'done'
        self.write(cr, uid, ids, {'state': state})
        return True

    #取消
    def done_to_cancel(self, cr, uid, ids, context={}):
        state = 'cancel'
        self.write(cr, uid, ids, {'state': state})
        return True

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/' :
            vals['name'] ='%s%s' % ('PAY', self.pool.get('ir.sequence').get(cr, uid, 'pay.no') or '/')

        return super(born_pay_line, self).create(cr, uid, vals, context=context)