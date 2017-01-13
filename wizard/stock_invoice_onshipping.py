# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Cogitoweb (<http://cogitoweb.it>).
#
##############################################################################


from openerp.osv import fields, osv
from openerp.tools.translate import _

class stock_invoice_onshipping(osv.osv_memory):
    _inherit = "stock.invoice.onshipping"

    def _get_journal(self, cr, uid, context=None):
        journal_obj = self.pool.get('account.journal')
        journal_type = self._get_journal_type(cr, uid, context=context)
        journals = journal_obj.search(cr, uid, [('type', '=', journal_type)])
        return journals and journals[0] or False

    def _get_journal_type(self, cr, uid, context=None):
        if context is None:
            context = {}
        pick_obj = self.pool.get('stock.picking')
        active_ids = context.get('active_ids',[])
        for pick in pick_obj.browse(cr, uid, active_ids, context=context):
            if (pick.is_contract_delivery == False):
                return super(stock_invoice_onshipping, self)._get_journal_type(cr, uid, context=context)
        return 'sale'

    _defaults = {
        'journal_type': _get_journal_type,
        'journal_id' : _get_journal,
        }

    def onchange_journal_id(self, cr, uid, ids, journal_id, context=None):
        pick_obj = self.pool.get('stock.picking')
        active_ids = context.get('active_ids',[])
        domain = {}
        value = {}
        for pick in pick_obj.browse(cr, uid, active_ids, context=context):
            if (pick.is_contract_delivery == False):
                return super(stock_invoice_onshipping, self).onchange_journal_id(cr, uid, ids, journal_id, context=context)
        domain['type'] = 'sale'
        if journal_id:
            journal = self.pool['account.journal'].browse(cr, uid, journal_id, context=context)
            value['journal_type'] = journal.type
        return {'value': value, 'domain': domain}

    def view_init(self, cr, uid, fields_list, context=None):
        if context is None:
            context = {}
        pick_obj = self.pool.get('stock.picking')
        count = 0
        active_ids = context.get('active_ids',[])
        for pick in pick_obj.browse(cr, uid, active_ids, context=context):
            if (pick.is_contract_delivery == False):
                return super(stock_invoice_onshipping, self).view_init(cr, uid, fields_list, context=context)
        return None

    def open_invoice(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        active_ids = context.get('active_ids',[])
        picking_pool = self.pool.get('stock.picking')
        for pick in picking_pool.browse(cr, uid, active_ids, context=context):
            if (pick.is_contract_delivery == False):
                return super(stock_invoice_onshipping, self).open_invoice(cr, uid, ids, context=context)

        invoice_ids = self.create_invoice(cr, uid, ids, context=context)
        if not invoice_ids:
            raise osv.except_osv(_('Error!'), _('No invoice created!'))

        data = self.browse(cr, uid, ids[0], context=context)

        action_model = False
        action = {}
        
        inv_type = 'out_invoice'
        data_pool = self.pool.get('ir.model.data')
        if inv_type == "out_invoice":
            action_id = data_pool.xmlid_to_res_id(cr, uid, 'account.action_invoice_tree1')
        
        if action_id:
            action_pool = self.pool['ir.actions.act_window']
            action = action_pool.read(cr, uid, action_id, context=context)
            action['domain'] = "[('id','in', ["+','.join(map(str,invoice_ids))+"])]"
            return action
        return True


    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, context=None):
        if context is None:
            context = {}
        partner, currency_id, company_id, user_id = key
        if inv_type in ('out_invoice', 'out_refund'):
            account_id = partner.property_account_receivable.id
            payment_term = partner.property_payment_term.id or False
        return {
            'user_id': user_id,
            'partner_id': partner.id,
            'account_id': account_id,
            'payment_term': payment_term,
            'type': inv_type,
            'fiscal_position': partner.property_account_position.id,
            'company_id': company_id,
            'currency_id': currency_id,
            'journal_id': journal_id,
        }

    def create_invoice(self, cr, uid, ids, context=None):
        context = dict(context or {})
        picking_pool = self.pool.get('stock.picking')
        invoice_obj = self.pool.get('account.invoice')
        
        rec = self.browse(cr, uid, ids)[0]
        invoices = {}
        invoice_ids = []

        pickings = context.get('active_ids', [])
        for pick in picking_pool.browse(cr, uid, pickings, context=context):
            if pick.is_contract_delivery == True and pick.contract_to_invoice == True and pick.state == 'done':
                key = (pick.partner_id, pick.company_id.currency_id.id, pick.company_id.id, uid)
                invoice_vals = self._get_invoice_vals(cr, uid, key, 'out_invoice', rec.journal_id.id, context=context)
                invoice_vals['origin'] = pick.name
                invoice_vals['date_invoice'] = rec.invoice_date

                if rec.group == False or pick.partner_id.id not in invoices.keys():
                    # Get account and payment terms
                    invoice_id = invoice_obj.create(cr, uid, invoice_vals, context)
                    invoice_ids.append(invoice_id)
                    invoices[pick.partner_id.id] = invoice_id
                else:
                    invoice = invoice_obj.browse(cr, uid, [invoices[pick.partner_id.id]], context=context)
                    merge_vals = {}
                    if not invoice.origin or invoice_vals['origin'] not in invoice.origin.split(', '):
                        invoice_origin = filter(None, [invoice.origin, invoice_vals['origin']])
                        merge_vals['origin'] = ', '.join(invoice_origin)
                    if invoice_vals.get('name', False) and (not invoice.name or invoice_vals['name'] not in invoice.name.split(', ')):
                        invoice_name = filter(None, [invoice.name, invoice_vals['name']])
                        merge_vals['name'] = ', '.join(invoice_name)
                    if merge_vals:
                        invoice.write(merge_vals)

                for line in pick.contract_delivery_line:
                    if line.invoice_state == '2binvoiced':
                        price_unit = line.contract_pricelist_line_id and line.contract_pricelist_line_id.sell_price
                        if not price_unit:
                            price_unit = line.product_id.product_tmpl_id.list_price
                        invoice_line_vals = {
                            'product_id': line.product_id.id,
                            'name': line.name or '/',
                            'partner_id': pick.partner_id.id,
                            'quantity': line.product_uom_qty,
                            'price_unit': price_unit,
                            'invoice_id': rec.group and invoices[pick.partner_id.id] or invoice_id
                        }
                        taxes = []
                        for tax in line.product_id.taxes_id:
                            taxes.append(tax.id)
                        invoice_line_vals['invoice_line_tax_id'] = [[6, 0, taxes]]

                        account_id = line.product_id.property_account_income.id
                        if not account_id:
                            account_id = line.product_id.categ_id.property_account_income_categ.id
                        invoice_line_vals['account_id'] = account_id

                        self.pool.get('account.invoice.line').create(cr, uid, invoice_line_vals, context)

                        self.pool.get('stock.move.contract').write(cr, uid, [line.id], {'invoice_state': 'invoiced'})

                #check if all lines are invoiced:
                flag = False
                invoiced = True
                for line in pick.contract_delivery_line:
                    if line.invoice_state == '2binvoiced':
                        flag = True
                        invoiced = False
                picking_pool.write(cr, uid, [pick.id], {
                                                        'contract_to_invoice': flag, 
                                                        'contract_invoiced': invoiced,
                                                        'invoice_id': invoice_id})

        return invoice_ids

