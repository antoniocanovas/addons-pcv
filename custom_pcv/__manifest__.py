# Copyright 2023 Serincloud SL.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Custom PCV",
    "summary": "Customs PCV",
    "version": "16.0.1.0.1",
    'category': 'Sales',
    "author": "Serincloud SL, ",
    "website": "https://www.ingenieriacloud.com",
    "license": "AGPL-3",
    "depends": [
        "sale_management",
        "purchase",
        "sale_purchase",
        "product_variant_sale_price",
        "website_sale",
        "website_event",
        "sale_order_line_date",
        "base_automation",
    ],
    "data": [
        "views/product_views.xml",
        "views/sale_order_views.xml",
        "views/purchase_order_views.xml",
        "views/event_views.xml",
        "data/automatic_actions.xml",
    ],
    "installable": True,
}
