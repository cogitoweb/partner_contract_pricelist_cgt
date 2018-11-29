# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ProductProduct(models.Model):
    _inherit = "product.product"


    # Fields declaration

    sale_ok = fields.Boolean(
        related='product_tmpl_id.sale_ok',
    )
