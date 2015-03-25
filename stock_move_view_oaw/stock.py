# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from datetime import datetime
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import SUPERUSER_ID
 

class StockMove(models.Model):
    _inherit = 'stock.move'

    pick_partner_id = fields.Many2one(
        related='picking_id.partner_id',
        store=True,
        readonly=True,
        string='Pick Partner'
        )
    quant_lot_id = fields.Many2one(
        'stock.production.lot',
        compute='_get_quant_info',
        store=True,
        readonly=True,
        string='Case No.'
        )
    quant_owner_id = fields.Many2one(
        'res.partner',
        compute='_get_quant_info',
        store=True,
        readonly=True,
        string='Owner'
        )

    @api.multi
    @api.depends('quant_ids')
    def _get_quant_info(self):
        for m in self:
            if m.quant_ids:
                m.quant_lot_id = m.quant_ids[0].lot_id and m.quant_ids[0].lot_id.id
                m.quant_owner_id = m.quant_ids[0].owner_id and m.quant_ids[0].owner_id.id

    def init(self, cr):
        move_ids = self.search(cr, SUPERUSER_ID, [])
        for m in self.browse(cr, SUPERUSER_ID, move_ids):
            m.pick_partner_id = m.picking_id.partner_id and m.picking_id.partner_id.id
            if m.quant_ids:
                m.quant_lot_id = m.quant_ids[0].lot_id and m.quant_ids[0].lot_id.id
                m.quant_owner_id = m.quant_ids[0].owner_id and m.quant_ids[0].owner_id.id