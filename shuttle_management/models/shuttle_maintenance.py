from odoo import fields, models, api


class ShuttleMaintenance(models.Model):
    """THIS MODEL FOR SHUTTLE MAINTENANCE MANAGEMENT"""
    _name = 'shuttle.maintenance'
    _description = 'Shuttle Maintenance Records'

    shuttle_id = fields.Many2one('shuttles.model', string='Shuttle', required=True)
    maintenance_date = fields.Date(string='Maintenance Date', required=True)
    maintenance_type = fields.Selection([
        ('routine', 'Routine'),
        ('repair', 'Repair'),
        ('emergency', 'Emergency')
    ], string='Maintenance Type', required=True)
    cost = fields.Float(string='Maintenance Cost')
    maintenance_description = fields.Text(string='Description')
    performed_by = fields.Many2one('res.partner', string='Performed By')
    next_maintenance_date = fields.Date(string='Next Maintenance Date')