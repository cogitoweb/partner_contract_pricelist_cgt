# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"


    @api.one
    @api.constrains('pricelist_ids')
    def check_qty(self):
        for rec in self:
            for line in rec.pricelist_ids:
                if line.minimum_stock_qty <= 0:
                    raise ValidationError(_('Invalid Product Pricelist!\n\nMinimum Stock Quantity must be greater than 0.'))

    pricelist_ids = fields.One2many('sale.contract.pricelist', 'analytic_account_id', 'Pricelists')
