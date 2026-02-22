from odoo import models, fields, api, _

class PurchaseOrderRejectWizard(models.TransientModel):
    _name = 'purchase.order.reject.wizard'
    _description = 'Wizard Perubahan State Penolakan PO'

    # Relasi balik ke PO. Boleh Many2one karena dari Transient ke Regular Model.
    order_id = fields.Many2one('purchase.order', string="Referensi PO", required=True, ondelete='cascade')
    reason = fields.Text(string="Alasan Penolakan", required=True)

    def action_confirm_reject(self):
        """
        Menulis alasan ke PO induk dan mengubah state menggunakan Active Record.
        """
        if self.order_id:
            # Update data PO induk
            self.order_id.write({
                'state': 'rejected',
                'rejection_reason': self.reason
            })
            
            # Catat log ke chatter beserta nama user yang mereject
            msg = _("PO Ditolak oleh %s.<br/><b>Alasan:</b> %s") % (self.env.user.name, self.reason)
            self.order_id.message_post(body=msg, subtype_xmlid='mail.mt_comment')
            
        # Menutup jendela pop-up setelah selesai
        return {'type': 'ir.actions.act_window_close'}