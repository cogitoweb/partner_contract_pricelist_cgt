# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import datetime

import logging
import pprint
_logger = logging.getLogger(__name__)


class FullApplyIstatRevaluation(models.TransientModel):
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

    target_percentage = fields.Integer(
        string='Percentage (%)',
    )
