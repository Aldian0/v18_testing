from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Ekstensi field state 
    state = fields.Selection(selection_add=[
        
        ('to_confim', 'Draft'),
        # ('confirm', 'C'),
        ('rejected', 'Rejected'),
        ('to_accept', 'To Accept'),
        ('accept', 'Accept'),


    ], default='to_confim', tracking=True)

    rejection_reason = fields.Text(string="Alasan Penolakan", tracking=True)

    def action_to_accept(self):
        # for rec in self:
        self.state = 'to_accept'
    def action_accept(self):
        # for rec in self:
        self.state = 'draft' 

    revision_no = fields.Integer(string="Revision", default=0, copy=False)
    base_name = fields.Char(string="Base Name", copy=False)

    def action_create_revision(self):
        for rec in self:

            # Simpan nama awal pertama kali
            if not rec.base_name:
                rec.base_name = rec.name

            # Tambah revision
            rec.revision_no += 1

            # Generate nama baru
            rec.name = f"{rec.base_name}-R{rec.revision_no}"
    
    

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