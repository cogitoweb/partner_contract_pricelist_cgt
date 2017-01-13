# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Cogitoweb (<http://cogitoweb.it>).
#
##############################################################################

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from openerp.tools.translate import _
from datetime import datetime

class Picking(models.Model):
    _inherit = "stock.picking"

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self._context and 'contract_order' in self._context:
            contracts = self.env['account.analytic.account'].search([('partner_id','=',self.partner_id.id), ('state','=','open')])
            self.update({'contract_id': False})
            if contracts and len(contracts) == 1:
                self.update({'contract_id': contracts[0].id})

    @api.onchange('contract_id')
    def onchange_contract(self):
        self.update({'is_contract_delivery': False})
        self.update({'contract_delivery_line': [[6, 0, []]]})
        if self.contract_id:
            picking_type = self.env['stock.picking.type'].search([('code','=','outgoing')], limit=1)
            self.update({'picking_type_id': picking_type.id})
            self.update({'is_contract_delivery': True})
            contract = self.contract_id
            lines = []
            for pricelist in contract.pricelist_ids:
                line_data = [0 , False, {
                                'product_id': pricelist.product_id.id,
                                'product_uom_qty': pricelist.minimum_stock_qty,
                                'name': pricelist.product_id.product_tmpl_id.name,
                                'product_uom': pricelist.product_uom_id and pricelist.product_uom_id.id or \
                                                pricelist.product_id.product_tmpl_id.uom_id.id,
                                'date': datetime.now(),
                                'date_expected': datetime.now(),
                                'invoice_state': '2binvoiced',
                                'state': 'draft',
                                'contract_pricelist_line_id': pricelist.id,
                }]
                lines.append(line_data)
            self.update({'contract_delivery_line': lines})

    @api.depends('contract_delivery_line', 'state')
    def _to_invoice(self):
        for picking in self:
            invoiced = False
            for line in picking.contract_delivery_line:
                if line.invoice_state == '2binvoiced':
                    invoiced = True
            picking.contract_to_invoice = invoiced

    contract_id = fields.Many2one('account.analytic.account', 'Contract', readonly=True, states={'draft': [('readonly', False)]})
    is_contract_delivery = fields.Boolean('Is Contract Delivery?')
    contract_delivery_line = fields.One2many('stock.move.contract', 'picking_id', 'Products', readonly=True, states={'draft': [('readonly', False)]})
    contract_to_invoice = fields.Boolean(compute="_to_invoice", string='To Invoice', store=True)
    contract_invoiced = fields.Boolean('Invoiced')
    invoice_id = fields.Many2one('account.invoice', 'Invoice Reference', ondelete='restrict')

    @api.multi
    def unlink(self):
        for picking in self:
            if picking.state == 'done':
                raise ValidationError('\nTransferred Delivery Order cannot be deleted.')
        return super(Picking, self).unlink()

    @api.multi
    def action_transfer(self):
        for picking in self:
            for line in picking.contract_delivery_line:
                line.write({'state':'done'})
            self._cr.execute("update stock_picking set state='done' where id=%s"%(picking.id))
            self._cr.commit()
            return True

    @api.multi
    def open_contract_invoice(self):
    	for pick in self:
    		ctx = {'form_view_ref': 'account.invoice_form'}
    		if pick.invoice_id:
    			return {
		    		'type': 'ir.actions.act_window',
		    		'res_model': 'account.invoice',
		    		'res_id': pick.invoice_id.id,
		    		'view_type': 'form',
		    		'view_mode': 'form',
		    		'target': 'current',
		    		'name': 'Contract Delivery Invoice',
		    		'context': ctx,
		    	}


class StockMoveContract(models.Model):
    _name = "stock.move.contract"
    _description = "Moves - Contract Delivery"

    picking_id = fields.Many2one('stock.picking', 'Picking')
    product_id = fields.Many2one('product.product', 'Product')
    name = fields.Char('Description')
    product_uom_qty = fields.Float('Quantity')
    product_uom = fields.Many2one('product.uom', 'Unit of Measure')
    date = fields.Date('Date')
    date_expected = fields.Date('Expected Date')
    invoice_state = fields.Selection([
                            ("invoiced", "Invoiced"),
                            ("2binvoiced", "To Be Invoiced"),
                            ("none", "Not Applicable")
                            ], "Invoice Control", required=True,
            states={'draft': [('readonly', False)]}, default='2binvoiced')
    state = fields.Selection([('draft', 'New'), ('done','Done')], 'State', default='draft')
    contract_pricelist_line_id = fields.Many2one('sale.contract.pricelist', 'Pricelist Line Id')
    
    @api.onchange('product_id')
    def onchange_product(self):
        for line in self:
            line.product_uom = line.product_id.product_tmpl_id.uom_id.id
