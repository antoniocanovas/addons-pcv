{
    'name': 'eCommerce sale line commitment date',
    'category': 'Hidden',
    'summary': 'Products price from sale order line commitment date',
    'version': '16.0.0.1.0',
    'license': 'AGPL-3',
    'description': """
    """,
    'author': "SERINCLOUD, S.L.",
    'website': "http://www.ingenieriacloud.com",
    'depends': ['website_sale','sale_order_line_date'],
    'data': [
        'views/templates.xml',
        'security/website_sale.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'website_sale_line_commitment_date/static/src/scss/*.scss',
            'website_sale_line_commitment_date/static/src/js/*.js',
        ],
    },
    'auto_install': True,
}
