# Copyright 2023 Serincloud SL.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Custom Website PCV",
    "summary": "Customs Website PCV",
    "version": "16.0.1.0.0",
    'category': 'Sales',
    "author": "Serincloud SL, ",
    "website": "https://www.ingenieriacloud.com",
    "license": "AGPL-3",
    "depends": [
        "website_event",
        "website_sale_product_brand",
                ],
    "data": [
        "views/website_event_views.xml",
        "views/website_sale_views.xml",
        "views/website_sale_product_brand_views.xml",
    ],
    "installable": True,
}
