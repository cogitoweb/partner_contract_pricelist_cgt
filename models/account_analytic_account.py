# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"


    pricelist_ids = fields.One2many(
            comodel_name='sale.contract.pricelist', 
            inverse_name='analytic_account_id', 
            string='Pricelists'
        )
