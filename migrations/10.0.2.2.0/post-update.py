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
    
    cr.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='sale_contract_pricelist' and column_name='order_line_id'
    """)
    
    column_exists = cr.dictfetchone()
    
    if column_exists and column_exists['column_name']:

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
        
    else:

        _logger.info(
            "order_line_id does not exist in sale_contract_pricelist, skip migration"
        )
