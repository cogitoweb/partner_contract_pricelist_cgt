# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import pprint
import logging
_logger = logging.getLogger(__name__)


class SaleContractPricelist(models.Model):
    _name = "sale.contract.pricelist"
    _description = "Sales Contract Pricelist"
    _order = "sequence, product_id"
    _rec_name = "product_id"


    # Fields declaration

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        ondelete="cascade"
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        domain=[('sale_ok', '=', True)]
    )

    product_uom_id = fields.Many2one(
        related='product_id.product_tmpl_id.uom_id',
        store=True
    )

    minimum_stock_qty = fields.Integer(
        string='Minimum Stock Quantity'
    )

    description = fields.Char(
        string='Description'
    )

    sell_price = fields.Float(
        string='Sell Price',
        digits=(10, 3)
    )

    sell_discount = fields.Float(
        string='Sell Discount (%)',
        digits=(6, 3), default=0.0
    )

    sequence = fields.Integer(
        string='Sequence',
        default=20
    )

    order_line_id = fields.Many2one(
        string='Order line',
        comodel_name='sale.order.line',
        ondelete='set null',
    )


    # Constraints and onchanges

    @api.one
    @api.constrains('sell_discount')
    def _check_description(self):
        if self.sell_discount < 0 or self.sell_discount > 100:
            raise ValidationError("Sell Discount must be between 0 and 100")


    # CRUD methods (and name_get, name_search, ...) overrides

    def read(self, fields, load='_classic_read'):
        """ Without this call, dynamic fields build by fields_view_get()
            generate a log warning, i.e.:
            sale.contract.pricelist.read() with unknown field 'name'
        """
        real_fields = fields
        if fields:
            # We remove fields which are not in _fields
            real_fields = [x for x in fields if x in self._fields]

        return super(SaleContractPricelist, self).read(real_fields, load=load)
