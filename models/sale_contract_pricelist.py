# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class SaleContractPricelist(models.Model):
    _name = "sale.contract.pricelist"
    _description = "Sales Contract Pricelist"
    _order = "sequence"

    @api.one
    @api.constrains('sell_discount')
    def _check_description(self):
        if self.sell_discount < 0 or self.sell_discount > 100:
            raise ValidationError("Sell Discount must be between 0 and 100")

    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Analytic Account', ondelete="cascade")
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    product_uom_id = fields.Many2one(related='product_id.product_tmpl_id.uom_id', store=True)
    minimum_stock_qty = fields.Integer(string='Minimum Stock Quantity')
    description = fields.Char(string='Description')
    sell_price = fields.Float(string='Sell Price')
    sell_discount = fields.Float(string='Sell Discount (%)', digits=(6,3), default=0.0)
    sequence = fields.Integer(string='Sequence', default=20)
