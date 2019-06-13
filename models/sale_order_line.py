# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import pprint
import logging
_logger = logging.getLogger(__name__)


class PricelistSaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    # Fields declaration

    pricelist_id = fields.Many2one(
        string='Pricelist',
        comodel_name='sale.contract.pricelist',
        ondelete='set null',
        copy=False,
    )
