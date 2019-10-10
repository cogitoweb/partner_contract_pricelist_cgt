# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import datetime

import logging
import pprint
_logger = logging.getLogger(__name__)


class DuplicatePricelistFromContract(models.TransientModel):
    _name = 'wizard.duplicate_pricelist_from_contract'
