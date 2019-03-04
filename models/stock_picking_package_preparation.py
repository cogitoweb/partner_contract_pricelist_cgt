# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import pprint
import logging
_logger = logging.getLogger(__name__)


class PricelistPackagePreparation(models.Model):
    _inherit = "stock.picking.package.preparation"


    # Fields declaration

    use_only_supplied_product = fields.Boolean(
        string="Use only allowed products",
        help="If checked, only the products provided by this supplier "
             "will be shown."
    )
