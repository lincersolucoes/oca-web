# -*- coding: utf-8 -*-
##############################################################################
##############################################################################
{
    'name': 'Widget Form Reload',
    'version': '10.0.0.0.0',
    'author': 'Intelligenti',
    'category': 'CRM',
    'website': 'http://intelligenti.com.br',
    'description': """
     Reload form without reloading whole tab
    """,
    'depends': [
                'base',
                'web'],
    'data': [
             'views/reload_form_view.xml',
            ],
    'demo_xml': [],
    'test': [],
    'qweb' : [
    ],
    'installable': True,
    'auto_install' : True,
}
