from odoo import fields, api, models

class FaturaConsorcio(models.Model):
    _name = 'contract.fatura_consorcio'
    _description = 'Recebimentos de Faturas do Consórcio'
    
    cd_fornecedor = fields.Many2one("res.partner", string="Fornecedor")
    total_concluido = fields.Integer(string="Total Concluído")
    valor_disponivel_concluir = fields.Integer(string="Total Disponível a Concluir")
    data_recebimento = fields.Char(string="Data Recebimento")
    cd_unidade_medida = fields.Many2one('uom.uom',string="Unidade de medida")
    cd_contrato = fields.Many2one('contract.contract', string="Contrato do Fornecedor")
