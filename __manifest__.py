# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Cogitoweb (<http://cogitoweb.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Partner Contract Pricelist",
    'summary': "Partner Contract Pricelist",

    'description': """
        This module add the following functionality:
            * New tab "Product Pricelist" in Sales/Sales/Contracts form to configure Products
            * Generate a Contract from a Sale Order
            * Istat revaluation for contracts
            * Import a Sale Order line to contract
    """,

    'author': "Cogito",
    'website': "http://www.cogitoweb.it",

    'category': "Tools",
    'version': "10.0.2.2.0",

    # any module necessary for this one to work correctly
    'depends': [
        'stock',
        'accounting_full',
        # 'account_analytic_analysis'
    ],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',

        # wizard
        'wizard/istat_revaluation.xml',
        'wizard/pricelist_from_order_line.xml',
        'wizard/duplicate_pricelist_from_contract.xml',

        # views
        'views/account_analytic_account.xml',
        'views/product_template.xml',
        'views/sale_contract_pricelist.xml',
        'views/sale_order.xml',
        'views/stock_picking_package_preparation.xml',
    ],

    'installable': True,
    'auto_install': False,
}
