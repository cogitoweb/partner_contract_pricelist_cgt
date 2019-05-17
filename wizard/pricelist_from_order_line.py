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
        domain="[('state', 'in', ('sale', 'done'))]"
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

    pipe_list_ids = fields.Char(
        string='list_ids',
    )


    # Constraints and onchanges

    @api.onchange('order_id')
    def _onchange_order_id(self):
        line_ids = self._get_order_line_ids(self.order_id)
        self.order_line_ids = line_ids.ids


    @api.onchange('order_line_ids')
    def _onchange_order_line_ids(self):
        # can't use self.order_line_ids in action, so we create
        # a piped string with the ids
        self.pipe_list_ids = '|'.join([str(x) for x in self.order_line_ids.ids])


    # Action methods

    @api.multi
    def action_add_to_pricelist(self):
        Pricelist = self.env['sale.contract.pricelist']
        SaleOrderLine = self.env['sale.order.line']

        if self.order_line_ids:
            # easy
            order_line_ids = self.order_line_ids

        elif self.pipe_list_ids:
            # cant use self.order_line_ids directly since at this
            # point is empty for some reason. Used onchange() to convert
            # self.order_line_ids to list of ids, piped with '|'.
            # here we split the string, convert values to int and browse them.
            list_of_ids = self.pipe_list_ids.split('|')
            list_of_int_ids = map(int, list_of_ids)
            order_line_ids = SaleOrderLine.browse(list_of_int_ids)

        else:
            # nothing to add
            return {
                'type': 'ir.actions.act_window.message',
                'title': _('Message'),
                'message': _("No sale order lines selected."),
                'close_button_title': _('Close')
            }

        # this should never happen
        if not self.contract_id:
            return {
                'type': 'ir.actions.act_window.message',
                'title': _('Message'),
                'message': _("No contract selected."),
                'close_button_title': _('Close')
            }

        # double check - filter out already added lines
        clean_order_line_ids = order_line_ids.filtered(lambda x: not x.pricelist_id)

        # create pricelist lines
        for order_line in clean_order_line_ids:
            res = Pricelist.create({
                'analytic_account_id': self.contract_id.id,
                'product_id': order_line.product_id.id,
                'description': order_line.name,
                'product_uom_id': order_line.product_uom.id,
                'minimum_stock_qty': order_line.product_uom_qty,
                'sell_price': order_line.price_unit,
                'sell_discount': order_line.discount,
            })

            # set link
            order_line.pricelist_id = res.id

        return {
            'type': 'ir.actions.act_window.message',
            'title': _('Message'),
            'message': _("Lines from sale order added to contract pricelist"),
            'close_button_title': False,
            'buttons': [{
                'type': 'ir.actions.act_window_close',
                'name': _('Close')
            }]
        }


    # Business methods

    def _get_order_line_ids(self, order_id):
        SaleOrderLine = self.env['sale.order.line']

        # return nothing
        if not order_id:
            return SaleOrderLine

        # all lines from this order, not already added anywhere
        order_line_ids = SaleOrderLine.search([
            ('order_id', '=', order_id.id),
            ('pricelist_id', '=', False)
        ])

        return order_line_ids
