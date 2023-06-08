# -*- coding: utf-8 -*-

from odoo import models, fields, api , _
from datetime import date, datetime
from odoo.exceptions import UserError, Warning


class ScheduleActivityCustomHistory(models.Model):

    _name = 'schedule.activity.custom.history'
    _description = "Schedule Activity History"
    _rec_name = "summary"
    _order = 'id desc'

    res_model_id = fields.Many2one(
        'ir.model', 
        string='Document Model',
        index=True, 
        ondelete='cascade', 
        required=True
    )
    res_model = fields.Char(
        string='Related Document Model',
        index=True, 
        related='res_model_id.model', 
        store=True, 
        readonly=True
    )
    res_id = fields.Many2oneReference(
        string='Related Document ID',
        index=True, 
        required=True, 
        model_field='res_model'
    )
    res_name = fields.Char(
        string='Document Name', 
        store=True,
        help="Display name of the related document.", 
        readonly=True
    )
    supervisor_user_id = fields.Many2one(
        'res.users',
        string='Supervisor',
        copy=False,
    )
    activity_type_id = fields.Many2one(
        'mail.activity.type', 
        string='Activity Type',
        domain="['|', ('res_model_id', '=', False), ('res_model_id', '=', res_model_id)]", 
        ondelete='restrict'
    )
    activity_category = fields.Selection(
        related='activity_type_id.category', 
        string='Action to Perform',
        readonly=True
    )
    activity_decoration = fields.Selection(
        related='activity_type_id.decoration_type', 
        string="Decoration Type",
        readonly=True
    )
    summary = fields.Char(
        string='Summary'
    )
    note = fields.Html(
        string='Note'
    )
    date_deadline = fields.Date(
        string='Due Date', 
        index=True, 
        required=True, 
        default=fields.Date.context_today
    )
    automated = fields.Boolean(
        string='Automated activity', 
        readonly=True,
        help='Indicates this activity has been created automatically and not by any user.'
    )
    user_id = fields.Many2one(
        'res.users', 
        string='Assigned to',
        default=lambda self: self.env.user,
        index=True, 
        required=True
    )
    state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned')], 
        string='State',
    )
    recommended_activity_type_id = fields.Many2one(
        'mail.activity.type', 
        string="Recommended Activity Type"
    )
    previous_activity_type_id = fields.Many2one(
        'mail.activity.type',
        string='Previous Activity Type', 
        readonly=True
    )
    has_recommended_activities = fields.Boolean(
        string='Next activities available',
        help='Technical field for UX purpose'
    )
#     force_next = fields.Boolean(
#         related='activity_type_id.force_next', 
#         string="Trigger Next Activity",
#         readonly=True
#     )
    can_write = fields.Boolean(
        string="Can Write",
        help='Technical field to hide buttons if the current user has no access.'
    )
    
    def unlink(self):
        if not self.env.user.has_group('base.user_admin'):
            raise UserError(_('You can not delete Schedule Activity History.'))


class MailActivity(models.Model):
    _inherit = "mail.activity"

    def _create_custom_schedule_history(self):
        if not self:
            return True
        custom_history_obj = self.env['schedule.activity.custom.history']
        vals = self.read(['res_model_id','res_model','res_id','res_name','supervisor_user_id','activity_type_id',
            'activity_category','activity_decoration','summary', 'note', 'date_deadline',
            'automated','user_id','state','recommended_activity_type_id','previous_activity_type_id',
            'has_recommended_activities','force_next','can_write'])[0]
        vals.update({
            'res_model_id': vals['res_model_id'][0],
            'activity_type_id': vals['activity_type_id'][0] if vals['activity_type_id'] else False,
            'recommended_activity_type_id': vals['recommended_activity_type_id'][0] if vals['recommended_activity_type_id'] else False,
            'previous_activity_type_id': vals['previous_activity_type_id'][0] if vals['previous_activity_type_id'] else False,
            'user_id': vals['user_id'][0],
            'supervisor_user_id': vals['supervisor_user_id'][0] if vals['supervisor_user_id'] else False,
            })
        custom_schedule_history_id = custom_history_obj.create(vals)
        custom_schedule_history_action = self.env.ref('schedule_activity_global_done.action_custom_schedule_activity_history')
        dict_act_window = custom_schedule_history_action.sudo().read([])[0]
        dict_act_window['res_id'] = custom_schedule_history_id.id
        return dict_act_window

    def _action_done(self, feedback=False, attachment_ids=None):
        self._create_custom_schedule_history()
        return super(MailActivity, self)._action_done(feedback=feedback, attachment_ids=attachment_ids)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

    
