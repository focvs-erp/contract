from odoo import fields, models


class VendorContractCostCenter(models.Model):
    _inherit = 'contract.contract'

    cost_center = fields.Many2one('ax4b_accounting.cost_center')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['cost_center'] = ", s.cost_center"
        groupby += ', s.cost_center'
        return super(VendorContractCostCenter, self)._query(with_clause, fields, groupby, from_clause)
