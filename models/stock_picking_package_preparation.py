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



class PricelistPackagePreparationLine(models.Model):
    _inherit = "stock.picking.package.preparation.line"


    # Constraints and onchanges

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(PricelistPackagePreparationLine, self)._onchange_product_id()

        # search in pricelist requires contract_id, which cant be
        # obtained from package_preparation_id using self._origin
        # because DDT can still be unsaved right now, so we pass ids
        # through context and convert them to obj
        contract_id = self._context.get('contract_id', False)

        if self.product_id:
            # browse(False) = False
            contract_id = self.env['account.analytic.account'].browse(contract_id)
            discount = self.product_id.get_product_pricelist_discount(contract_id)
            self.discount = discount
