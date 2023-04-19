{
    'name': 'eCommerce sale line commitment date',
    'category': 'Hidden',
    'summary': 'Products price from sale order line commitment date',
    'version': '1.0',
    'description': """
    """,
    'depends': ['website_sale',],
    'data': [
        'views/templates.xml',
        'security/ir.model.access.csv',
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
