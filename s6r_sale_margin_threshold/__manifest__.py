# Copyright 2025 Scalizer (<https://www.scalizer.fr>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
{
    'name': 'Scalizer Sale Margin Threshold',
    'version': '18.0.1.0.0',
    'author': 'Scalizer',
    'website': 'https://www.scalizer.fr',
    'summary': "Ensure products are sold above their minimum price with margin checks in sale orders.",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'sale_margin',
    ],
    'category': 'Generic Modules/Scalizer',
    'complexity': 'easy',
    'description': '''
        The Scalizer Margin Sale module calculates and enforces the minimum sale price and profit margin for each product.
        When a user attempts to sell a product below its minimum price in a sale order,
        the system triggers a warning, helping businesses maintain profitability and prevent underpricing.
        ''',
    'qweb': [
    ],
    'demo': [
    ],
    'images': [
    ],
    'data': [
        # Views
        'views/res_config_settings_view.xml',
        'views/sale_order_views.xml',
    ],
    'auto_install': True,
    'installable': True,
    'application': False,
}
