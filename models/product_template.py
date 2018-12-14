# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, \
    DEFAULT_SERVER_DATE_FORMAT

import pprint
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Compute

    # Fields

    # Methods

    @api.multi
    def action_view_contract_lines(self):
        self.ensure_one()
        action = self.env.ref('partner_contract_pricelist_cgt.sale_contract_pricelist_action')
        product_ids = self.with_context(active_test=False).product_variant_ids.ids

        # sequences can be copied by slicing
        new_domain = action.domain[:]
        new_domain.append(('product_id.product_tmpl_id', '=', self.id))

        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': "{'default_product_id': " + str(product_ids[0]) + "}",
            'res_model': action.res_model,
            'domain': new_domain
        }
