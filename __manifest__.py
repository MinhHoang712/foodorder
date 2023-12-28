# -*- coding: utf-8 -*-
{
    'name': "foodOrder",

    'summary': """
        Module đặt đồ ăn bùng lổ 
        """,

    'description': """
        Hơn cả Module đặt đồ ăn bùng lổ 
    """,

    'icon':'/food_order/static/description/icon.png',

    'author': "My Company",
    'website': "https://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail'],

    'data': [
        'security/rule.xml',
        'security/ir.model.access.csv',
        'views/food_order_views.xml',
        'views/res_user_views.xml',
        'views/menu.xml',
        'data/notify.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',

}
