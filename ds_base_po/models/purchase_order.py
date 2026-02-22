from odoo import models, fields, api, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Ekstensi field state tanpa merusak alur standar Odoo
    state = fields.Selection(selection_add=[
        # ('to_approve_manager', 'Approve Manager'),
        # ('to_approve_dept', 'Approve Dept Head'),
        # ('to_approve_cfo', 'Approve CFO'),
        ('to_confim', 'Draft'),
        # ('confirm', 'C'),
        ('rejected', 'Rejected'),
        ('to_accept', 'To Accept'),
        ('accept', 'Accept'),


    ], default='to_confim', tracking=True)


    def action_to_accept(self):
        # for rec in self:
        self.state = 'to_accept'
    def action_accept(self):
        # for rec in self:
        self.state = 'draft'

    # def action_rejected(self):
    #     # for rec in self:
    #     self.state = 'rejected'

    rejection_reason = fields.Text(string="Alasan Penolakan", tracking=True)

    # def action_submit_for_approval(self):
    #     """
    #     Mengevaluasi nilai PO dan menentukan tahap persetujuan berikutnya.
    #     """
    #     for rec in self:
    #         amount = rec.amount_total
            
    #         # Logika Filter berdasarkan Nominal PO
    #         if amount < 5000000:
    #             rec.state = 'to_approve_manager'
    #             next_role = "Manager"
    #         elif 5000000 <= amount <= 20000000:
    #             rec.state = 'to_approve_dept'
    #             next_role = "Kepala Departemen"
    #         else:
    #             rec.state = 'to_approve_cfo'
    #             next_role = "CFO"
            
    #         # Mencatat di chatter & memicu notifikasi email ke follower/grup terkait
    #         msg = _("PO sebesar IDR {:,.2f} diajukan. Menunggu persetujuan dari: {}").format(amount, next_role)
    #         rec.message_post(body=msg, subtype_xmlid='mail.mt_comment')

    def action_approve_custom(self):
        """
        Aksi saat tombol Approve ditekan oleh role yang berwenang.
        """
        for rec in self:
            if rec.state == 'to_approve_manager':
                rec.button_confirm() # Jika disetujui Manager, langsung jadi PO
                msg = _("PO Disetujui oleh Manager.")
                
            elif rec.state == 'to_approve_dept':
                rec.button_confirm() # Jika disetujui dept head, langsung jadi PO
                msg = _("PO Disetujui oleh Kepala Departemen")
                
            elif rec.state == 'to_approve_cfo':
                rec.button_confirm() # Final approval dari CFO
                msg = _("PO Disetujui oleh CFO.")
            else:
                continue
            
            rec.message_post(body=msg, subtype_xmlid='mail.mt_comment')

    def action_reject_order(self):
        """
        Membuka jendela pop-up (Wizard) agar user wajib mengisi alasan penolakan.
        """
        return {
            'name': _('Alasan Penolakan PO'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            # Mem-passing ID PO saat ini ke dalam Wizard
            'context': {'default_order_id': self.id}
        }