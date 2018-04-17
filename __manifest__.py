# -*- coding: utf-8 -*-
{
    'name': "transfer_stock_to_location",

    'summary': """Transfer Stock to a Location""",

    'description': """
        Select Products and on hand qty minus reserved will be added to a new stock operation to transfer to a destination location
    """,

    'author': "WAVE, LLC",
    'website': "http://wave.us/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'wizard/stock_to_location_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}