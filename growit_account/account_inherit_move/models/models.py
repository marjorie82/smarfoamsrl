# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class account_inherit_move(models.Model):
    _inherit = 'account.move'

    @api.constrains("name", "journal_id", "partner_id", "state", "l10n_do_fiscal_number")
    def _check_unique_sequence_number(self):
        l10n_do_invoices = self.filtered(
            lambda inv: inv.l10n_latam_use_documents
                        and inv.country_code == "DO"
                        and inv.state == "posted"
                        and inv.move_type in ("in_invoice", "in_refund")
        )
        if l10n_do_invoices:
            self.flush(
                ["name", "journal_id", "move_type", "state", "l10n_do_fiscal_number", "partner_id"]
            )
            self._cr.execute(
                """
                SELECT move2.id, move2.l10n_do_fiscal_number
                FROM account_move move
                INNER JOIN account_move move2 ON
                    move2.l10n_do_fiscal_number = move.l10n_do_fiscal_number
                    AND move2.journal_id = move.journal_id
                    AND move2.move_type = move.move_type
                    AND move2.partner_id = move.partner_id
                    AND move2.id != move.id
                WHERE move.id IN %s AND move2.state = 'posted'
            """,
                [tuple(l10n_do_invoices.ids)],
            )
            res = self._cr.fetchone()
            if res:
                raise ValidationError(
                    ("Numero de comprobante fiscal %s ya existe para el proveedor %s")
                    %(self.l10n_do_fiscal_number, self.partner_id.name)
                )

        super(account_inherit_move, (self - l10n_do_invoices))._check_unique_sequence_number()





