# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import pprint
import logging
_logger = logging.getLogger(__name__)


class PricelistIstatRevaluationHistory(models.Model):
    _name = 'istat.revaluation_history'


    # Fields declaration

    contract_id = fields.Many2one(
        string='Contract',
        comodel_name='account.analytic.account',
        domain="[('type', '=', 'contract')]",
    )

    pricelist_id = fields.Many2one(
        string='Product',
        comodel_name='sale.contract.pricelist',
    )

    revaluation_year = fields.Integer(
        string='Year',
    )

    revaluation_percentage = fields.Integer(
        string='Percentage (%)',
    )

    sell_price_original = fields.Float(
        string='Previous sell price',
        digits=(10, 3)
    )

    sell_price_new = fields.Float(
        string='New sell price',
        digits=(10, 3)
    )
