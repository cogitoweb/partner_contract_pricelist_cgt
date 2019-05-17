# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

import pprint
import logging
_logger = logging.getLogger(__name__)


class PricelistSaleOrder(models.Model):
    _inherit = "sale.order"


    # Fields declaration

    contract_id = fields.Many2one(
        string='Contract',
        comodel_name='account.analytic.account',
        domain=[('type', '=', 'contract')],
        ondelete='set null',
    )


    # Action methods

    @api.multi
    def generate_contract_from_order(self):
        # redirect doesnt work with @api.one
        # solution: @api.multi with ensure_one()
        self.ensure_one()

        # check order state
        if self.state not in ('sale', 'done'):
            raise ValidationError(
                _("Order should be confirmed before creating contract.")
            )

        # you already done this!
        if self.contract_id:
            raise ValidationError(
                _("Contract has already been generated from this order.\n%s")
                % (self.contract_id.name)
            )

        order_confirmation_date = datetime.datetime.strptime(self.confirmation_date, DEFAULT_SERVER_DATETIME_FORMAT).date()
        one_year_later = order_confirmation_date + relativedelta(years=1)

        # default/required vals of the contract
        contract_vals = {
            'name': self.name,
            'type': 'contract',
            'partner_id': self.partner_id.id,
            'start_date': order_confirmation_date,
            'end_date': one_year_later,
            'client_ref': self.client_order_ref or False
        }

        # create contract
        contract_vals = self._prepare_contract_vals(contract_vals)
        new_contract = self.env['account.analytic.account'].create(contract_vals)

        # override name
        new_contract.name = new_contract.generate_contract_name(new_contract.id)

        # copy order lines as contract pricelist lines
        for order_line in self.order_line:
            x = new_contract.add_pricelist_from_sale_order_line(order_line)

        # link sale_order to contract
        self.contract_id = new_contract.id

        # convert partner into customer (if not already)
        self.partner_id.write({
            'customer': True
        })

        # redirect to contract
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.analytic.account',
            'target': 'current',
            'res_id': new_contract.id,
            'type': 'ir.actions.act_window'
        }


    # dumb function for contract_vals overrides
    # before creation
    def _prepare_contract_vals(self, vals):
        return vals
