# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta
from collections import defaultdict
from odoo.tools import float_compare, OrderedSet
from collections import defaultdict
from dateutil.relativedelta import relativedelta

from odoo.osv import expression
from odoo.addons.stock.models.stock_rule import ProcurementException
 

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    qty = fields.Integer("Cantidad")
    anch = fields.Integer("Ancho")
    larg = fields.Integer("Largo")
    alt = fields.Char("Altura")
    
class StockRule(models.Model):
    _inherit = 'stock.rule'
    
    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom):
        date_planned = self._get_date_planned(product_id, company_id, values)
        date_deadline = values.get('date_deadline') or date_planned + relativedelta(days=company_id.manufacturing_lead) + relativedelta(days=product_id.produce_delay)
        mo_values = {
            'origin': origin,
            'product_id': product_id.id,
            'product_description_variants': values.get('product_description_variants'),
            'product_qty': product_qty,
            'product_uom_id': product_uom.id,
            'location_src_id': self.location_src_id.id or self.picking_type_id.default_location_src_id.id or location_id.id,
            'location_dest_id': location_id.id,
            'bom_id': bom.id,
            'date_deadline': date_deadline,
            'date_planned_start': date_planned,
            'date_planned_finished': fields.Datetime.from_string(values['date_planned']),
            'procurement_group_id': False,
            'propagate_cancel': self.propagate_cancel,
            'orderpoint_id': values.get('orderpoint_id', False) and values.get('orderpoint_id').id,
            'picking_type_id': self.picking_type_id.id or values['warehouse_id'].manu_type_id.id,
            'company_id': company_id.id,
            'move_dest_ids': values.get('move_dest_ids') and [(4, x.id) for x in values['move_dest_ids']] or False,
            'user_id': False,
            
        }
        sale_id = self.env['sale.order'].search([('name', '=', origin)])
        for line in sale_id.order_line:
            if line.product_id == product_id:
                mo_values.update({
                    'qty':line.qty,
                    'anch': line.anch,
                    'larg': line.larg,
                    'alt': line.alt,
                })
        # Use the procurement group created in _run_pull mrp override
        # Preserve the origin from the original stock move, if available
        if location_id.warehouse_id.manufacture_steps == 'pbm_sam' and values.get('move_dest_ids') and values.get('group_id') and values['move_dest_ids'][0].origin != values['group_id'].name:
            origin = values['move_dest_ids'][0].origin
            mo_values.update({
                'name': values['group_id'].name,
                'procurement_group_id': values['group_id'].id,
                'origin': origin,
            })
        return mo_values


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    qty = fields.Integer("Cantidad")
    anch = fields.Integer("Ancho")
    larg = fields.Integer("Largo")
    alt = fields.Char("Altura")

    @api.onchange('anch','larg','qty','alt')
    def onchange_quantity(self):
        r2 = 0
        for rec in self:
            if rec.alt:
                if " " in rec.alt:
                    space = rec.alt.split(" ")
                    slash = space[1].split("/")
                    r1 = rec.anch*rec.larg*(int(space[0])+round(int(slash[0])/int(slash[1]),2))
                    r2 = r1/144

                elif "/" in rec.alt and not " " in rec.alt:
                    sslash = rec.alt.split("/")
                    rr1 = rec.anch*rec.larg*(round(int(sslash[0])/int(sslash[1]),2))
                    r2 = rr1/144
                else:
                    alone = rec.alt
                    rr1 = rec.anch*rec.larg*(int(alone[0]))
                    r2 = rr1/144
                    
                rec.product_uom_qty = r2*rec.qty
