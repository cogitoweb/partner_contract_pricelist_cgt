# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import odoo.addons.decimal_precision as dp

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
        ondelete='cascade',
        auto_join=True,
    )

    partner_id = fields.Many2one(
        related='analytic_account_id.partner_id',
        store=True
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        domain=[('sale_ok', '=', True)],
        auto_join=True,
        required=True,
    )

    product_tmpl_id = fields.Many2one(
        string='Template',
        comodel_name='product.template',
        related='product_id.product_tmpl_id',
        readonly=True
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
        digits=dp.get_precision('Product Price')
    )

    sell_discount = fields.Float(
        string='Sell Discount (%)',
        digits=(4, 1),
        default=0.0
    )

    sequence = fields.Integer(
        string='Sequence',
        default=20
    )

    # Constraints and onchanges

    @api.one
    @api.constrains('sell_discount')
    def _check_sell_discount(self):
        if self.sell_discount < 0 or self.sell_discount > 100:
            raise ValidationError(_("Sell Discount must be between 0 and 100"))


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
