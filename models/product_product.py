# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import pprint
import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"


    # Fields declaration

    sale_ok = fields.Boolean(
        related='product_tmpl_id.sale_ok',
    )
