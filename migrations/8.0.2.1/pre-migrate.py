import logging
#from openerp import SUPERUSER_ID
#from openerp.modules.registry import RegistryManager
#from openerp.exceptions import except_orm, Warning

_logger = logging.getLogger('upgrade')

def migrate(cr, version):
    if not version:
        return

    cr.execute("""
        update ir_ui_view set active = false where name = 'stock.picking.contract.delivery.tree';
        update ir_ui_view set active = false where name = 'stock.picking.contract.form';
        update ir_ui_view set active = false where name = 'stock.picking.inherit.contract.form';
        update ir_ui_view set active = false where name = 'stock.picking.search.inherit.contracts';

    """)



