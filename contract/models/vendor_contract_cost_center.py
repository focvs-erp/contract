from odoo import fields, models


class VendorContractCostCenter(models.Model):
    _inherit = 'contract.contract'

    cost_center = fields.One2many('ax4b_accounting.cost_center')
