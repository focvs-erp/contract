from odoo import fields, api, models

class FaturaConsorcio(models.Model):
    _name = 'contract.fatura_consorcio'
    _description = 'Recebimentos de Faturas do Consórcio'


    cd_fornecedor = fields.Many2one("res.partner", string="Supplier")
    contract_line = fields.Many2one("contract.line", string="Contract Line")
    total_completed = fields.Integer(string="Completed Total")
    value_available_finish = fields.Integer(string="Available")
    data_recebimento = fields.Date(string="Receiving Date")
    cd_unidade_medida = fields.Many2one(related='contract_line.uom_id', string="Unit of Meassure")
    # cd_contrato = fields.Many2one('contract.contract', string="Contrato do Fornecedor")
    cd_contrato = fields.Many2one(related='contract_line.contract_id', string="Supplier Contract")
    cd_produto = fields.Many2one(related='contract_line.product_id', string="Product" )
    balance_percentage = fields.Char(string="Percentage", readonly="1")

