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
