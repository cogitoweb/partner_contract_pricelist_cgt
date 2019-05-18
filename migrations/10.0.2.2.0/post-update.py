# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

import pprint
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info(
        "Running post-migrate script. Old version was %s"
        % version
    )

    # from v10.0.2.2.0, reference between sale_order_line and
    # sale_contract_pricelist are not saved on scp but in sol
    cr.execute("""
        UPDATE sale_order_line
        SET pricelist_id = subquery.pricelist_id
        FROM (
            SELECT scp.id AS pricelist_id, sol.id AS order_line_id
            FROM sale_contract_pricelist scp
            INNER JOIN sale_order_line sol ON scp.order_line_id = sol.id
        ) AS subquery
        WHERE id = subquery.order_line_id
    """)
