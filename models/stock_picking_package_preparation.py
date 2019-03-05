# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import pprint
import logging
_logger = logging.getLogger(__name__)


class PricelistPackagePreparation(models.Model):
    _inherit = "stock.picking.package.preparation"


    # Fields declaration

    show_only_contract_products = fields.Boolean(
        string="Show only products from contract",
        help="If checked, only the products in the partner contract will be shown.",
        default=False, store=False
    )
