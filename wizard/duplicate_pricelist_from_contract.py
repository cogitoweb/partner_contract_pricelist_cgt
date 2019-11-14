# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import datetime

import logging
import pprint
_logger = logging.getLogger(__name__)


class DuplicatePricelistFromContract(models.TransientModel):
    _name = 'wizard.duplicate_pricelist_from_contract'

    # Default methods
    def _get_contract_id(self):
        return self.env['account.analytic.account'].browse(self._context.get('active_id'))

    # Fields declaration

    # current active contract
    default_contract_id = fields.Many2one(
        string='Contract',
        comodel_name='account.analytic.account',
        domain="[('type', '=', 'contract')]",
        default=_get_contract_id,
    )

    # import from contract
    contract_id = fields.Many2one(
        string='Contract',
        comodel_name='account.analytic.account',
        domain="[('type', '=', 'contract')]",
    )

    pricelist_id = fields.Many2one(
        string="Price Listing",
        comodel_name="product.pricelist"
    )

    pricelist_line_ids = fields.Many2many(
        string='Price List item',
        comodel_name='product.pricelist.item',
        relation='pricelist_wizard_contract_rel'
    )

    pricelist_contract_line_ids = fields.Many2many(
        string='Price List Contract item',
        comodel_name='sale.contract.pricelist',
        relation='pricelist_wizard_contract_line_rel'
    )

    pipe_list_ids = fields.Char(
        string='list_ids',
    )

    pipe_contract_list_ids = fields.Char(
        string='list_ids',
    )

    # Constraints and onchanges
    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        line_ids = self._get_pricelist_line_ids(self.pricelist_id)
        self.pricelist_line_ids = line_ids.ids

    @api.onchange('contract_id')
    def _onchange_contract_line_ids(self):
        pipe_list_ids = self._get_contract_pricelist_line_ids(self.contract_id)
        self.pricelist_contract_line_ids = pipe_list_ids.ids

    @api.onchange('pricelist_line_ids')
    def _onchange_pricelist_line_ids(self):
        # can't use self.pricelist_line_ids in action, so we create
        # a piped string with the ids
        self.pipe_list_ids = '|'.join([str(x) for x in self.pricelist_line_ids.ids])

    @api.onchange('pricelist_contract_line_ids')
    def _onchange_pricelist_contract_line_ids(self):
        # can't use self.pricelist_contract_line_ids in action, so we create
        # a piped string with the ids
        self.pipe_contract_list_ids = '|'.join([str(x) for x in self.pricelist_contract_line_ids.ids])

    # Action methods
    @api.multi
    def action_add_pricelist(self):

        # //////////////////////// VALIDATION  //////////////////////////////
        #no contract selected
        if not self.contract_id and self.pricelist_id and not self.default_contract_id:
            return {
                'type': 'ir.actions.act_window.message',
                'title': _('Message'),
                'message': _("No contract selected."),
                'close_button_title': _('Close')
            }

        elif not self.contract_id and self.pricelist_id and not self.default_contract_id:
            # no pricelist selected
            return {
                'type': 'ir.actions.act_window.message',
                'title': _('Message'),
                'message': _("No pricelist selected."),
                'close_button_title': _('Close')
            }

        # this should never happen
        elif not self.contract_id and not self.pricelist_id:
            return {
                'type': 'ir.actions.act_window.message',
                'title': _('Message'),
                'message': _("You have to select at least one field"),
                'close_button_title': _('Close')
            }
        # this should never happen
        elif self.contract_id and self.pricelist_id:
            return {
                'type': 'ir.actions.act_window.message',
                'title': _('Message'),
                'message': _("You have to select only one field"),
                'close_button_title': _('Close')
            }

        #//////////////////////// END VALIDATION  //////////////////////////////

        #//////////////////////// LISTING PRICE  //////////////////////////////

        ProductPriceItem = self.env['product.pricelist.item']
        pricelist_line_ids = self.pricelist_line_ids
        if self.pricelist_line_ids:
            # easy
            pricelist_line_ids = self.pricelist_line_ids
        elif self.pipe_list_ids:
            # cant use self.pricelist_line_ids directly since at this
            # point is empty for some reason. Used onchange() to convert
            # self.pricelist_line_ids to list of ids, piped with '|'.
            # here we split the string, convert values to int and browse them.
            list_of_ids = self.pipe_list_ids.split('|')
            list_of_int_ids = map(int, list_of_ids)
            pricelist_line_ids = ProductPriceItem.browse(list_of_int_ids)

        # double check - filter out already added lines
        clean_price_line_ids = pricelist_line_ids.filtered(lambda x: x.pricelist_id)

        # create pricelist lines
        for price_line in clean_price_line_ids:
            self.default_contract_id.add_pricelist_from_price_line(price_line)

        #//////////////////////// END LISTING PRICE  //////////////////////////////

        #//////////////////////// CONTRACT PRICE  //////////////////////////////

        pricelist_contract_line_ids = self.pricelist_contract_line_ids

        # add pricelist line from contract
        ProductContractPriceItem = self.env['sale.contract.pricelist']
        if self.pricelist_contract_line_ids:
            # easy
            pricelist_contract_line_ids = self.pricelist_contract_line_ids
        elif self.pipe_contract_list_ids:
            # cant use self.pricelist_contract_line_ids directly since at this
            # point is empty for some reason. Used onchange() to convert
            # self.pricelist_contract_line_ids to list of ids, piped with '|'.
            # here we split the string, convert values to int and browse them.
            list_of_ids = self.pipe_contract_list_ids.split('|')
            list_of_int_ids = map(int, list_of_ids)
            pricelist_contract_line_ids = ProductContractPriceItem.browse(list_of_int_ids)

        # double check - filter out already added lines
        clean_price_contract_line_ids = pricelist_contract_line_ids.filtered(lambda x: x.analytic_account_id)

        # create pricelist lines
        for price_contract_line in clean_price_contract_line_ids:
            self.default_contract_id.add_pricelist_from_contarct_price_line(price_contract_line)

        if self.contract_id:
            _logger.info("Imported pricelist in contract %s from contract %s" % (self.default_contract_id.id, self.contract_id.id))
        else:
            _logger.info("Imported pricelist in contract %s from generic pricelist %s" % (self.default_contract_id.id, self.pricelist_id))

        return {
            'type': 'ir.actions.act_window.message',
            'title': _('Message'),
            'message': _("Lines added to contract pricelist"),
            'close_button_title': False,
            'buttons': [{
                'type': 'ir.actions.act_window_close',
                'name': _('Close')
            }]
        }
        #//////////////////////// END CONTRACT PRICE  //////////////////////////////       

    # Business methods listing price
    def _get_pricelist_line_ids(self, pricelist_id):
        ProductPriceItem = self.env['product.pricelist.item']

        # return nothing
        if not pricelist_id:
            return ProductPriceItem

        # all lines from this order, not already added anywhere
        pricelist_line_ids = ProductPriceItem.search([
            ('pricelist_id', '=', pricelist_id.id),
        ])

        return pricelist_line_ids

    # Business methods contract price
    def _get_contract_pricelist_line_ids(self, contract_line_ids):
        ProductContractPriceItem = self.env['sale.contract.pricelist']

        # return nothing
        if not contract_line_ids:
            return ProductContractPriceItem

        # all lines from this order, not already added anywhere
        pricelist_contract_line_ids = ProductContractPriceItem.search([
            ('analytic_account_id', '=', contract_line_ids.id),
        ])

        return pricelist_contract_line_ids
