# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import datetime

import logging
import pprint
_logger = logging.getLogger(__name__)


class PricelistPricelistFromOrderLine(models.TransientModel):
    _name = 'wizard.pricelist_from_order_line'


    # Default methods

    def _get_contract_id(self):
        return self.env['account.analytic.account'].browse(self._context.get('active_id'))


    # Fields declaration

    order_id = fields.Many2one(
        string='Sale Order',
        comodel_name='sale.order',
    )

    order_line_ids = fields.Many2many(
        string='Sale Order lines',
        comodel_name='sale.order.line',
    )

    contract_id = fields.Many2one(
        string='Contract',
        comodel_name='account.analytic.account',
        default=_get_contract_id,
    )


    # Constraints and onchanges

    @api.onchange('order_id')
    def _onchange_order_id(self):
        line_ids = self._get_order_line_ids(self.order_id)
        self.order_line_ids = line_ids.ids


    def _get_order_line_ids(self, order_id):
        Pricelist = self.env['sale.contract.pricelist']
        SaleOrderLine = self.env['sale.order.line']

        # return nothing
        if not order_id:
            return SaleOrderLine

        # all lines from this order
        order_line_ids = SaleOrderLine.search([('order_id', '=', order_id.id)])

        # check if already used in pricelist
        linked_pricelist_ids = Pricelist.search([
            ('order_line_id', 'in', order_line_ids.ids)
        ])

        # get sale order lines to exclude
        order_line_to_exlude_ids = linked_pricelist_ids.mapped('order_line_id')

        # return diff
        return order_line_ids - order_line_to_exlude_ids


    # Action methods

    @api.multi
    def action_add_to_pricelist(self):
        pass
