# -*- coding: utf-8 -*-
##############################################################################
#  COMPANY: BORN
#  AUTHOR: LH
#  EMAIL: arborous@gmail.com
#  VERSION : 1.0   NEW  2014/07/21
#  UPDATE : NONE
#  Copyright (C) 2011-2014 www.wevip.com All Rights Reserved
##############################################################################

{
    'name': "服务",
    'author': 'BORN',
    'summary': 'BORN',
    'description': """
     """,
    'category': 'BORN',
    'sequence': 8,
    'website': 'http://www.wevip.com',
    'images': [],
    'depends': ['base','web_cleditor'],
 
    'demo': [],
    'init_xml': [],
    'data': [
        'security/groups.xml',
        'born_service.xml',
        'security/ir.model.access.csv',
        'sequence.xml',
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}
