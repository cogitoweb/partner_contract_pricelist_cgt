# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016 CogitoWEB (<http://cogitoweb.it>).
#
##############################################################################

from openerp import models, fields, api

class ContractDeliveryInvoice(models.TransientModel):
    _name = "contract.delivery.invoice.create"
    _description = "Contract Delivery Invoice - Create"


    @api.multi
    def action_create_invoice(self):
        context = self._context
