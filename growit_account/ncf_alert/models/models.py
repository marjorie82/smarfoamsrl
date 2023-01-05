# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

DEFAULT_MESSAGE = "Default message"

SUCCESS = "success"
DANGER = "danger"
WARNING = "warning"
INFO = "info"
DEFAULT = "default"


class ncf_alert(models.Model):
    _inherit = 'ir.sequence'

    max_ncf = fields.Integer()
    notification_ncf = fields.Integer()
    channel = fields.Many2one('mail.channel')
    user_ids = fields.Many2many('res.users')

    def _next(self, sequence_date=None):
        """ Returns the next number in the preferred sequence in all the ones given in self."""

        if self.l10n_latam_document_type_id:
            if self.number_next == self.notification_ncf:
                for user in self.user_ids:
                    resto = self.number_next_actual = self.notification_ncf
                    _logger.error((user.name, 'Notificado'))
                    error_msg = 'Los comprobantes estan por acabarse en la compañia {0}, quedan {1}.'.format(
                        self.company_id.name,
                        resto
                    )

                    user.notify_info(
                        message=error_msg,
                        sticky=True,
                        title='Notificacion de Comprobantes'
                    )
                self.action_send_notification(
                    self.l10n_latam_document_type_id.name)

            elif self.number_next == self.max_ncf:
                for user in self.user_ids:
                    _logger.error((user.name, 'Notificado'))

                    error_msg = 'Los comprobantes se han agotado en la compañia {0}.'.format(
                        self.company_id.name,
                    )

                    user.notify_danger(
                        message=error_msg,
                        sticky=True,
                        title='Notificacion de Comprobantes'
                    )

            elif self.number_next == self.max_ncf + 1:
                raise UserError('No queda mas comprobantes de: %s' %
                                self.l10n_latam_document_type_id.name)

        if not self.use_date_range:
            return self._next_do()

        # date mode
        dt = sequence_date or self._context.get(
            'ir_sequence_date', fields.Date.today())
        seq_date = self.env['ir.sequence.date_range'].search([
            ('sequence_id', '=', self.id),
            ('date_from', '<=', dt),
            ('date_to', '>=', dt)], limit=1)

        if not seq_date:
            seq_date = self._create_date_range_seq(dt)

        return seq_date.with_context(ir_sequence_date_range=seq_date.date_from)._next()

    def action_send_notification(self, ncf_type=False):
        msg = 'Los comprobantes %s estan por agotarse Numero Siguiente:%d de %d' % (
            ncf_type, self.number_next, self.max_ncf)

        self.env['mail.message'].with_user(SUPERUSER_ID).create({
            'model': 'mail.channel',
            'subtype_id': self.env.ref('mail.mt_comment').id,
            'body': msg,
            # self.env.ref('ncf_alert.notification_ncf').id)],
            'channel_ids': [(4, self.channel.id)],
            # .env.ref('ncf_alert.notification_ncf').id,
            'res_id': self.channel.id,
        })


class ResPartner(models.Model):
    _inherit = 'res.users'

    def _notify_channel(
        self, type_message=DEFAULT, message=DEFAULT_MESSAGE, title=None, sticky=False
    ):
        channel_name_field = "notify_{}_channel_name".format(type_message)
        bus_message = {
            "type": type_message,
            "message": message,
            "title": title,
            "sticky": sticky,
        }
        notifications = [(record[channel_name_field], bus_message)
                         for record in self]
        self.env["bus.bus"].sendmany(notifications)

