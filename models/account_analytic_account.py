#-*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from openerp.tools.translate import _

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