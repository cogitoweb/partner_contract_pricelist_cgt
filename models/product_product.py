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


    # CRUD methods (and name_get, name_search, ...) overrides

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        use_only_supplied_product = self.env.context.get('show_only_contract_products', False)
        contract_id = self.env.context.get('contract_id', False)

        # filter search results showing only the products in the pricelist
        if use_only_supplied_product:
            product_list = self.env['sale.contract.pricelist'].search([
                ('analytic_account_id', '=', contract_id)
            ])

            if product_list:
                args += [
                    ('id', 'in', [x.product_id.id for x in product_list])
                ]

        return super(PricelistProductProduct, self).search(
            args, offset=offset, limit=limit, order=order, count=count
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
        p_id = contract_id.partner_id if contract_id else partner_id
        return super(PricelistProductProduct, self).get_product_sale_price_unit(p_id, date)


    @api.multi
    def get_product_pricelist_discount(self, contract_id):
        self.ensure_one()

        # alias
        Pricelist = self.env['sale.contract.pricelist']

        if not contract_id:
            # how should I answer you?
            return 0

        # get discount from pricelist
        res_pricelist = Pricelist.search([
            ('analytic_account_id', '=', contract_id.id),
            ('product_id', '=', self.id)
        ], order='sequence')

        # return discount or zero
        if res_pricelist:
            return res_pricelist[0].sell_discount
        else:
            return 0
