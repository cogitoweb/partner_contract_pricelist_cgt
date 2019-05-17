# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import pprint
import logging
_logger = logging.getLogger(__name__)


class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"


    # Fields declaration

    pricelist_ids = fields.One2many(
        comodel_name='sale.contract.pricelist',
        inverse_name='analytic_account_id',
        string='Pricelists'
    )

    istat_revaluation_enabled = fields.Boolean(
        string='Istat revaluation',
        default=False,
    )

    istat_revaluation_year = fields.Integer(
        string='Istat revaluation year',
    )

    istat_revaluation_percentage = fields.Integer(
        string='Istat revaluation (%)',
    )


    # Business methods

    @api.multi
    def add_pricelist_from_sale_order_line(self, order_line_id):
        # @param order_line_id: sale.order.line() obj
        # @out: False or sale.contract.pricelist() obj
        self.ensure_one()

        if not order_line_id:
            return False

        # create pricelist from order line
        # [TODO] _prepare_vals()
        res = self.env['sale.contract.pricelist'].create({
            'analytic_account_id': self.id,
            'product_id': order_line_id.product_id.id,
            'description': order_line_id.name,
            'product_uom_id': order_line_id.product_uom.id,
            'minimum_stock_qty': order_line_id.product_uom_qty,
            'sell_price': order_line_id.price_unit,
            'sell_discount': order_line_id.discount,
        })

        # link new record to sale order line
        order_line_id.pricelist_id = res.id
        return res
