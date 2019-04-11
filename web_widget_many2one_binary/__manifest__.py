# -*- encoding: utf-8 -*-
{
    'name': 'Widget Many2one Binary',
    'version': '10.0.0.0.0',
    'author': 'Intelligenti',
    'category': 'Extra Tools',
    'website': 'http://intelligenti.com.br',
    'description': """
    * Binary widget for many2one Field
    """,
    'depends': ['web','base'],
    'qweb': [
        'static/src/xml/widget_template.xml',
    ],
    'data': [
        'views/widget_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
