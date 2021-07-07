from odoo import fields, api, models

class FaturaConsorcio(models.Model):
    _name = 'contract.fatura_consorcio'
    _description = 'Recebimentos de Faturas do Consórcio'

    cd_fornecedor = fields.Many2one("res.partner", string="Fornecedor")
    contract_line = fields.Many2one("contract.line", string="Linha do Contrato")
    total_concluido = fields.Integer(string="Total Concluído")
    valor_disponivel_concluir = fields.Integer(string="Total Disponível a Concluir")
    data_recebimento = fields.Date(string="Data Recebimento")
    cd_unidade_medida = fields.Many2one(related='contract_line.uom_id', string="Unidade de medida")
    # cd_contrato = fields.Many2one('contract.contract', string="Contrato do Fornecedor")
    cd_contrato = fields.Many2one(related='contract_line.contract_id', string="Contrato do Fornecedor")
    cd_produto = fields.Many2one(related='contract_line.product_id', string="Produto" )

