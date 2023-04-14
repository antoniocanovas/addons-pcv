{
    'name': 'eCommerce ServiceDate',
    'category': 'Hidden',
    'summary': 'Sell rental products on your eCommerce',
    'version': '1.0',
    'description': """
This module allows you to sell rental products in your eCommerce with
appropriate views and selling choices.
    """,
    'depends': ['website_sale',],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_sale_dateservice/static/src/scss/*.scss',
            'website_sale_dateservice/static/src/js/*.js',
        ],
    },
    'auto_install': True,
}
