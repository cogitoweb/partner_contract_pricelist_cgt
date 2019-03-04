# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import pprint
import logging
_logger = logging.getLogger(__name__)


class PricelistProductProduct(models.Model):
    _inherit = "product.product"


    # Fields declaration

    sale_ok = fields.Boolean(
        related='product_tmpl_id.sale_ok',
    )


    # Business methods

    @api.multi
    def get_product_sale_price_unit(self, partner_id=None, date=None, contract_id=None):
        self.ensure_one()

        # alias
        Pricelist = self.env['sale.contract.pricelist']

        if contract_id:
            res_pricelist = Pricelist.search([
                ('analytic_account_id', '=', contract_id.id),
                ('product_id', '=', self.id)
            ], order='sequence')

            if res_pricelist:
                _logger.info(
                    "Price for product %s found in CONTRACT %s"
                    % (self.default_code, contract_id.id)
                )
                return res_pricelist[0].sell_price

        # no results from contract, or no contract at all.
        # call super() and search on partner/default pricelist,
        # or get sell price from product template
        pid = contract_id.partner_id if contract_id else partner_id
        return super(PricelistProductProduct, self).get_product_sale_price_unit(pid, date)
