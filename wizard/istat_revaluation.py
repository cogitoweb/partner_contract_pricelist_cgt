# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import datetime

import logging
import pprint
_logger = logging.getLogger(__name__)


class PricelistApplyIstatRevaluation(models.TransientModel):
    _name = 'wizard.istat_revaluation'


    # Default methods

    def _get_contract_ids(self):
        return self.env['account.analytic.account'].browse(self._context.get('active_ids'))

    def _get_year_list(self):
        year = datetime.datetime.today().year
        return [(x, x) for x in range(year, year - 5, -1)]


    # Fields declaration

    contract_ids = fields.Many2many(
        string='Contracts',
        comodel_name='account.analytic.account',
        default=_get_contract_ids,
    )

    target_year = fields.Selection(
        string='Year',
        selection=_get_year_list
    )

    target_percentage = fields.Float(
        string='Percentage (%)',
    )


    # Action methods

    @api.multi
    def action_apply_istat_revaluation(self):

        for contract in self.contract_ids:

            # feature disabled
            if not contract.istat_revaluation_enabled:
                continue

            # already done for this target year
            if contract.istat_revaluation_year >= self.target_year:
                continue

            # loop on pricelist
            # and add target_percentage to price
            for pricelist in contract.pricelist_ids:
                current_price = pricelist.sell_price
                increment = self.target_percentage * current_price / 100
                pricelist.write(
                    {'sell_price': current_price + increment}
                )

            # set last execution year/percentage
            contract.istat_revaluation_year = self.target_year
            contract.istat_revaluation_percentage = self.target_percentage

        # compose message
        msg = _("%s contracts updated for %s Istat revaluation with %s%%.")

        return {
            'type': 'ir.actions.act_window.message',
            'title': _('Message'),
            'message': msg % (len(self.contract_ids), self.target_year, self.target_percentage),
            'close_button_title': False,
            'buttons': [{
                'type': 'ir.actions.act_window_close',
                'name': _('Close')
            }]
        }
