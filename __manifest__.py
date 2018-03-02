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
        This module adds following functionality :
            1) It adds "Product Pricelist" tab in Sales/Sales/Contracts form to configure Products.
    """,
    
    'author': "Cogito",
    'website': "http://www.cogitoweb.it",

    'category': "Tools",
    'version': "10.0.2.1",
    
    # any module necessary for this one to work correctly
    'depends': ['stock', 'accounting_full'], #account_analytic_analysis
    
    # always loaded
    'data': [
        'views/account_analytic_account.xml',
        'security/ir.model.access.csv',
    ],
    
    'installable': True,
    'auto_install': False,
}
