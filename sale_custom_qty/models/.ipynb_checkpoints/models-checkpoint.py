# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class sale_custom_qty(models.Model):
    _inherit = 'sale.order.line'
    
    qty = fields.Integer("Cantidad")
    anch = fields.Integer("Ancho")
    larg = fields.Integer("Largo")
    alt = fields.Char("Altura")

    @api.onchange('anch','larg','qty','alt')
    def onchange_quantity(self):
        r2 = 0
        for rec in self:
            if " " in rec.alt:
                space = rec.alt.split(" ")
                slash = space[1].split("/")
                r1 = rec.anch*rec.larg*(int(space[0])+round(int(slash[0])/int(slash[1]),2))
                r2 = r1/144
                
            if "/" in rec.alt and not " " in rec.alt:
                sslash = rec.alt.split("/")
                rr1 = rec.anch*rec.larg*(round(int(sslash[0])/int(sslash[1]),2))
                r2 = rr1/144
            rec.product_uom_qty = r2*rec.qty
