from odoo import fields, models


class VendorContractCostCenter(models.Model):
    _inherit = 'contract.contract'

    cost_center_id = fields.Many2one('ax4b_accounting.cost_center')