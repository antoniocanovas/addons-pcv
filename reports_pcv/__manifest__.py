# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Reports PCV",
    "summary": "Reports PCV",
    "version": "16.0.0.1.0",
    "category": "Reports",
    "author": "SerinCloud, ",
    "website": "https://ingeniriacloud.com",
    "license": "AGPL-3",
    "depends": ['account',
                "purchase",
                "custom_pcv",
                ],
    "data": [
        "views/report_purchaseorder_document.xml",
        "views/purchase_order_portal_content.xml",
    ],
    "installable": True,
}
