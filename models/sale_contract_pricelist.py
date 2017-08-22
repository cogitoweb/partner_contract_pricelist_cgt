# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class SaleContractPricelist(models.Model):
    _name = "sale.contract.pricelist"
    _description = "Sales Contract Pricelist"
    _order = "sequence"


    @api.onchange('product_id')
    def onchange_product(self):
        self.update({'product_uom_id': self.product_id.product_tmpl_id.uom_id.id})


    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', ondelete="cascade")
    product_id = fields.Many2one('product.product', 'Product', domain="[('type','in',('product', 'consu'))]")
    product_uom_id = fields.Many2one('product.uom', 'Product UOM')
    sell_price = fields.Float('Sell Price')
    minimum_stock_qty = fields.Integer('Minimum Stock Quantity')
    sequence = fields.Integer('Sequence')
