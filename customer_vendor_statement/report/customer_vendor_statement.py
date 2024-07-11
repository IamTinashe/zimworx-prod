# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import api, fields, models


class CustomerVendorStatement(models.AbstractModel):
    """Model of Customer Activity Statement"""
    _name = 'report.customer_vendor_statement.statement'

    def _get_account_initial_balance(self, company_id, partner_ids, date_start):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_start = datetime.strptime(date_start, DEFAULT_SERVER_DATE_FORMAT).date()

        q1_query = self._initial_balance_sql_q1(partners, date_start)
        q2_query = self._initial_balance_sql_q2(company_id)

        self.env.cr.execute(f"""
            WITH Q1 AS ({q1_query}), Q2 AS ({q2_query})
            SELECT partner_id, currency_id, balance
            FROM Q2
        """)

        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)

        return res

    def _initial_balance_sql_q1(self, partners, date_start):
        partners_list = ', '.join(
            f"'{partner}'" for partner in partners)  # Ensure partners are safely quoted if they are strings
        return f"""
            SELECT l.partner_id, l.currency_id, l.company_id,
            CASE WHEN l.currency_id is not null AND l.amount_currency > 0.0
                THEN SUM(l.amount_currency)
                ELSE SUM(l.debit)
            END AS debit,
            CASE WHEN l.currency_id is not null AND l.amount_currency < 0.0
                THEN SUM(l.amount_currency * (-1))
                ELSE SUM(l.credit)
            END AS credit
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account a ON l.account_id = a.id
            WHERE l.partner_id IN ({partners_list}) AND a.account_type = 'income'
                AND l.date <= '{date_start}' AND not l.blocked
            GROUP BY l.partner_id, l.currency_id, l.company_id
        """

    def _initial_balance_sql_q2(self, company_id):
        return f"""
            SELECT Q1.partner_id, SUM(Q1.debit - Q1.credit) AS balance,
            COALESCE(Q1.currency_id, c.currency_id) AS currency_id
            FROM Q1
            JOIN res_company c ON c.id = Q1.company_id
            WHERE c.id = {company_id}
            GROUP BY Q1.partner_id, Q1.currency_id, c.currency_id
        """

    def _format_date_to_partner_lang(self, str_date, partner_id):
        lang_code = self.env['res.partner'].browse(partner_id).lang
        lang_id = self.env['res.lang']._lang_get(lang_code)
        lang = self.env['res.lang'].browse(lang_id)
        date = str_date
        return date

    def _initial_balance_sql_q1_payable(self, partners, date_start):
        return f"""
            SELECT l.partner_id, l.currency_id, l.company_id,
            CASE WHEN l.currency_id is not null AND l.amount_currency > 0.0
                THEN SUM(l.amount_currency)
                ELSE SUM(l.debit)
            END as debit,
            CASE WHEN l.currency_id is not null AND l.amount_currency < 0.0
                THEN SUM(l.amount_currency * (-1))
                ELSE SUM(l.credit)
            END as credit
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account a ON l.account_id = a.id
            WHERE l.partner_id IN ({partners}) AND l.account_type = 'expense'
                  AND l.date <= '{date_start}' AND not l.blocked
            GROUP BY l.partner_id, l.currency_id, l.company_id
        """

    def _initial_balance_sql_q1_receivable_and_payable(self, partners, date_start):
        return f"""
            SELECT l.partner_id, l.currency_id, l.company_id,
            CASE WHEN l.currency_id is not null AND l.amount_currency > 0.0
                THEN SUM(l.amount_currency)
                ELSE SUM(l.debit)
            END as debit,
            CASE WHEN l.currency_id is not null AND l.amount_currency < 0.0
                THEN SUM(l.amount_currency * (-1))
                ELSE SUM(l.credit)
            END as credit
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account a ON l.account_id = a.id
            WHERE l.partner_id IN ({partners}) AND (l.account_type = 'expense' OR l.account_type = 'income')
                  AND l.date <= '{date_start}' AND not l.blocked
            GROUP BY l.partner_id, l.currency_id, l.company_id
        """

    def _initial_balance_sql_q2_payable(self, company_id):
        return """
            SELECT Q1.partner_id, debit-credit AS balance,
            COALESCE(Q1.currency_id, c.currency_id) AS currency_id
            FROM Q1
            JOIN res_company c ON (c.id = Q1.company_id)
            WHERE c.id = %s
        """ % company_id

    def _initial_balance_sql_q2_receivable_and_payable(self, company_id):
        return f"""
            SELECT Q1.partner_id, debit - credit AS balance,
            COALESCE(Q1.currency_id, c.currency_id) AS currency_id
            FROM Q1
            JOIN res_company c ON c.id = Q1.company_id
            WHERE c.id = {company_id}
        """

    def _get_account_initial_balance_payable(self, company_id, partner_ids,
                                     date_start):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_start = datetime.strptime(
            date_start, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s)
        SELECT partner_id, currency_id, balance
        FROM Q2""" % (self._initial_balance_sql_q1_payable(partners, date_start),
                      self._initial_balance_sql_q2_payable(company_id)))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _get_account_initial_balance_receivable_and_payable(self, company_id, partner_ids,
                                     date_start):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_start = datetime.strptime(
            date_start, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s)
        SELECT partner_id, currency_id, balance
        FROM Q2""" % (self._initial_balance_sql_q1_receivable_and_payable(partners, date_start),
                      self._initial_balance_sql_q2_receivable_and_payable(company_id)))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _display_lines_sql_q1(self, partners, date_start, date_end):
        return f"""
            SELECT m.name AS move_id, aa.code AS account_id, l.partner_id, l.date, l.name,
                   l.ref, l.blocked, l.currency_id, l.company_id,
            CASE WHEN (l.currency_id is not null AND l.amount_currency > 0.0)
                THEN SUM(l.amount_currency)
                ELSE SUM(l.debit)
            END as debit,
            CASE WHEN (l.currency_id is not null AND l.amount_currency < 0.0)
                THEN SUM(l.amount_currency * (-1))
                ELSE SUM(l.credit)
            END as credit,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_move m ON (l.move_id = m.id)
            JOIN account_account aa ON (l.account_id = aa.id)
            WHERE l.partner_id IN ({partners}) AND l.account_type = 'income'
                  AND '{date_start}' <= l.date AND l.date <= '{date_end}'
            GROUP BY l.partner_id, m.name, aa.code, l.date, l.date_maturity, l.name,
                     l.ref, l.blocked, l.currency_id, l.amount_currency, l.company_id
        """

    def _display_lines_sql_q1_payable(self, partners, date_start, date_end):
        return f"""
            SELECT m.name AS move_id, aa.code AS account_id, l.partner_id, l.date, l.name,
                                    l.ref, l.blocked, l.currency_id, l.company_id,
            CASE WHEN (l.currency_id is not null AND l.amount_currency > 0.0)
                THEN SUM(l.amount_currency)
                ELSE SUM(l.debit)
            END as debit,
            CASE WHEN (l.currency_id is not null AND l.amount_currency < 0.0)
                THEN SUM(l.amount_currency * (-1))
                ELSE SUM(l.credit)
            END as credit,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account aa ON l.account_id = aa.id
            WHERE l.partner_id IN ({partners}) AND l.account_type = 'expense'
                  AND '{date_start}' < l.date AND l.date <= '{date_end}'
            GROUP BY l.partner_id, m.name, aa.id, l.date, l.date_maturity, l.name,
                                    l.ref, l.blocked, l.currency_id,
                                    l.amount_currency, l.company_id
        """

    def _display_lines_sql_q1_receivable_and_payable(self, partners, date_start, date_end):
        return f"""
            SELECT m.name AS move_id, aa.code AS account_id, l.partner_id, l.date, l.name,
                                l.ref, l.blocked, l.currency_id, l.company_id,
            CASE WHEN (l.currency_id is not null AND l.amount_currency > 0.0)
                THEN SUM(l.amount_currency)
                ELSE SUM(l.debit)
            END as debit,
            CASE WHEN (l.currency_id is not null AND l.amount_currency < 0.0)
                THEN SUM(l.amount_currency * (-1))
                ELSE SUM(l.credit)
            END as credit,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account aa ON l.account_id = aa.id
            WHERE l.partner_id IN ({partners}) AND (l.account_type = 'expense' OR l.account_type = 'income')
                  AND '{date_start}' < l.date AND l.date <= '{date_end}'
            GROUP BY l.partner_id, m.name, aa.id, l.date, l.date_maturity, l.name,
                                l.ref, l.blocked, l.currency_id,
                                l.amount_currency, l.company_id
        """

    def _display_lines_sql_q2(self, company_id):
        return """
            SELECT Q1.partner_id, move_id, account_id, date, date_maturity, Q1.name, ref,
                            debit, credit, debit-credit as amount, blocked,
            COALESCE(Q1.currency_id, c.currency_id) AS currency_id
            FROM Q1
            JOIN res_company c ON (c.id = Q1.company_id)
            WHERE c.id = %s
        """ % company_id

    def _display_lines_sql_q2_payable(self, company_id):
        return """
            SELECT Q1.partner_id, move_id, account_id, date, date_maturity, Q1.name, ref,
                            debit, credit, debit-credit as amount, blocked,
            COALESCE(Q1.currency_id, c.currency_id) AS currency_id
            FROM Q1
            JOIN res_company c ON (c.id = Q1.company_id)
            WHERE c.id = %s
        """ % company_id

    def _display_lines_sql_q2_receivable_and_payable(self, company_id):
        return """
            SELECT Q1.partner_id, move_id, account_id, date, date_maturity, Q1.name, ref,
                            debit, credit, debit-credit as amount, blocked,
            COALESCE(Q1.currency_id, c.currency_id) AS currency_id
            FROM Q1
            JOIN res_company c ON (c.id = Q1.company_id)
            WHERE c.id = %s
        """ % company_id

    def _get_account_display_lines(self, company_id, partner_ids, date_start, date_end):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_start = datetime.strptime(date_start, DEFAULT_SERVER_DATE_FORMAT).date()
        date_end = datetime.strptime(date_end, DEFAULT_SERVER_DATE_FORMAT).date()

        q1_query = self._display_lines_sql_q1(partners, date_start, date_end)
        q2_query = self._display_lines_sql_q2(company_id)

        self.env.cr.execute(f"""
            WITH Q1 AS ({q1_query}), Q2 AS ({q2_query})
            SELECT partner_id, move_id, account_id, date, date_maturity, name, ref, debit,
                   credit, amount, blocked, currency_id
            FROM Q2
            ORDER BY date, date_maturity, move_id
        """)

        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _get_account_display_lines_payable(self, company_id, partner_ids, date_start,
                                   date_end):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_start = datetime.strptime(
            date_start, DEFAULT_SERVER_DATE_FORMAT).date()
        date_end = datetime.strptime(
            date_end, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s)
        SELECT partner_id, move_id, account_id, date, date_maturity, name, ref, debit,
                            credit, amount, blocked, currency_id
        FROM Q2
        ORDER BY date, date_maturity, move_id""" % (
            self._display_lines_sql_q1_payable(partners, date_start, date_end),
            self._display_lines_sql_q2_payable(company_id)))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _get_account_display_lines_receivable_and_payable(self, company_id, partner_ids, date_start,
                                   date_end):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_start = datetime.strptime(
            date_start, DEFAULT_SERVER_DATE_FORMAT).date()
        date_end = datetime.strptime(
            date_end, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s)
        SELECT partner_id, move_id, account_id, date, date_maturity, name, ref, debit,
                            credit, amount, blocked, currency_id
        FROM Q2
        ORDER BY date, date_maturity, move_id""" % (
            self._display_lines_sql_q1_receivable_and_payable(partners, date_start, date_end),
            self._display_lines_sql_q2_receivable_and_payable(company_id)))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _show_buckets_sql_q1(self, partners, date_start, date_end):
        return f"""
            SELECT l.partner_id, l.currency_id, l.company_id, l.move_id,
            CASE WHEN l.balance > 0.0
                THEN l.balance - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.balance + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due,
            CASE WHEN l.balance > 0.0
                THEN l.amount_currency - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.amount_currency + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due_currency,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account aa ON l.account_id = aa.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.credit_move_id = l2.id
                WHERE '{date_start}' <= l2.date AND l2.date <= '{date_end}'
            ) as pd ON pd.debit_move_id = l.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.debit_move_id = l2.id
                WHERE '{date_start}' <= l2.date AND l2.date <= '{date_end}'
            ) as pc ON pc.credit_move_id = l.id
            WHERE l.partner_id IN ({partners}) AND l.account_type = 'income'
                AND '{date_start}' <= l.date AND l.date <= '{date_end}' AND not l.reconciled AND not l.blocked
            GROUP BY l.partner_id, l.currency_id, l.date, l.date_maturity,
                                l.amount_currency, l.balance, l.move_id,
                                l.company_id
        """

    def _show_buckets_sql_q1_payable(self, partners, date_start, date_end):
        return f"""
            SELECT l.partner_id, l.currency_id, l.company_id, l.move_id,
            CASE WHEN l.balance > 0.0
                THEN l.balance - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.balance + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due,
            CASE WHEN l.balance > 0.0
                THEN l.amount_currency - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.amount_currency + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due_currency,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account aa ON l.account_id = aa.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.credit_move_id = l2.id
                WHERE '{date_start}' <= l2.date AND l2.date <= '{date_end}'
            ) as pd ON pd.debit_move_id = l.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.debit_move_id = l2.id
                WHERE '{date_start}' <= l2.date AND l2.date <= '{date_end}'
            ) as pc ON pc.credit_move_id = l.id
            WHERE l.partner_id IN ({partners}) AND l.account_type = 'expense'
                AND '{date_start}' <= l.date AND l.date <= '{date_end}' AND not l.reconciled AND not l.blocked
            GROUP BY l.partner_id, l.currency_id, l.date, l.date_maturity,
                        l.amount_currency, l.balance, l.move_id,
                        l.company_id
        """

    def _show_buckets_sql_q1_receivable_and_payable(self, partners, date_start, date_end):
        return f"""
            SELECT l.partner_id, l.currency_id, l.company_id, l.move_id,
            CASE WHEN l.balance > 0.0
                THEN l.balance - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.balance + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due,
            CASE WHEN l.balance > 0.0
                THEN l.amount_currency - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.amount_currency + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due_currency,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account aa ON l.account_id = aa.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.credit_move_id = l2.id
                WHERE '{date_start}' <= l2.date AND l2.date <= '{date_end}'
            ) as pd ON pd.debit_move_id = l.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.debit_move_id = l2.id
                WHERE '{date_start}' <= l2.date AND l2.date <= '{date_end}'
            ) as pc ON pc.credit_move_id = l.id
            WHERE l.partner_id IN ({partners}) AND (l.account_type = 'expense' OR l.account_type = 'income') 
                AND '{date_start}' <= l.date AND l.date <= '{date_end}' AND not l.reconciled AND not l.blocked
            GROUP BY l.partner_id, l.currency_id, l.date, l.date_maturity,
                                l.amount_currency, l.balance, l.move_id,
                                l.company_id
        """

    def _show_overdue_sql_q1(self, partners, date_end):
        return f"""
            SELECT l.partner_id, l.currency_id, l.company_id, l.move_id,
            CASE WHEN l.balance > 0.0
                THEN l.balance - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.balance + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due,
            CASE WHEN l.balance > 0.0
                THEN l.amount_currency - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.amount_currency + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due_currency,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account a ON l.account_id = a.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.credit_move_id = l2.id
                WHERE '{date_end}' <= l2.date
            ) as pd ON pd.debit_move_id = l.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.debit_move_id = l2.id
                WHERE '{date_end}' <= l2.date
            ) as pc ON pc.credit_move_id = l.id
            WHERE l.partner_id IN ({partners}) AND l.account_type = 'income'
                AND not l.reconciled AND not l.blocked
            GROUP BY l.partner_id, l.currency_id, l.date, l.date_maturity,
                        l.amount_currency, l.balance, l.move_id,
                        l.company_id
        """

    def _show_overdue_sql_q1_payable(self, partners, date_end):
        return f"""
            SELECT l.partner_id, l.currency_id, l.company_id, l.move_id,
            CASE WHEN l.balance > 0.0
                THEN l.balance - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.balance + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due,
            CASE WHEN l.balance > 0.0
                THEN l.amount_currency - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.amount_currency + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due_currency,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account aa ON l.account_id = aa.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.credit_move_id = l2.id
                WHERE '{date_end}' <= l2.date
            ) as pd ON pd.debit_move_id = l.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.debit_move_id = l2.id
                WHERE '{date_end}' <= l2.date
            ) as pc ON pc.credit_move_id = l.id
            WHERE l.partner_id IN ({partners}) AND l.account_type = 'expense'
                AND not l.reconciled AND not l.blocked
            GROUP BY l.partner_id, l.currency_id, l.date, l.date_maturity,
                        l.amount_currency, l.balance, l.move_id,
                        l.company_id
        """

    def _show_overdue_sql_q1_receivable_and_payable(self, partners, date_end):
        return f"""
            SELECT l.partner_id, l.currency_id, l.company_id, l.move_id,
            CASE WHEN l.balance > 0.0
                THEN l.balance - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.balance + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due,
            CASE WHEN l.balance > 0.0
                THEN l.amount_currency - SUM(COALESCE(pd.amount, 0.0))
                ELSE l.amount_currency + SUM(COALESCE(pc.amount, 0.0))
            END AS open_due_currency,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_move m ON l.move_id = m.id
            JOIN account_account aa ON l.account_id = aa.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.credit_move_id = l2.id
                WHERE '{date_end}' <= l2.date
            ) as pd ON pd.debit_move_id = l.id
            LEFT JOIN (
                SELECT pr.*
                FROM account_partial_reconcile pr
                INNER JOIN account_move_line l2 ON pr.debit_move_id = l2.id
                WHERE '{date_end}' <= l2.date
            ) as pc ON pc.credit_move_id = l.id
            WHERE l.partner_id IN ({partners}) AND (l.account_type = 'expense' OR l.account_type = 'income') 
                AND not l.reconciled AND not l.blocked
            GROUP BY l.partner_id, l.currency_id, l.date, l.date_maturity,
                        l.amount_currency, l.balance, l.move_id,
                        l.company_id
        """

    def _show_buckets_sql_q2(self, today, minus_30, minus_60, minus_90):
        return """
            SELECT partner_id, currency_id, date_maturity, open_due,
                            open_due_currency, move_id, company_id,
            CASE
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is null THEN open_due
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_1_30,
            CASE
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is null THEN open_due
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_30_60,
            CASE
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is null THEN open_due
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_60_90,
            CASE
                WHEN date_maturity <= '%s' AND currency_id is null
                                THEN open_due
                WHEN date_maturity <= '%s' AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_over_90
            FROM Q1
            GROUP BY partner_id, currency_id, date_maturity, open_due,
                                open_due_currency, move_id, company_id
        """ % (minus_30, today, minus_30, today, minus_60,
               minus_30, minus_60, minus_30, minus_90, minus_60, minus_90,
               minus_60, minus_90, minus_90)

    def _show_overdue_sql_q2(self, date_end):
        return f"""
            SELECT partner_id, currency_id, date_maturity, open_due,
                            open_due_currency, move_id, company_id,
            CASE
                WHEN '{date_end}' <= date_maturity AND currency_id is null
                                THEN open_due
                WHEN '{date_end}' <= date_maturity AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as current
            FROM Q1
            GROUP BY partner_id, currency_id, date_maturity, open_due,
                                open_due_currency, move_id, company_id
        """

    def _show_buckets_sql_q2_receivable_and_payable(self,
        today, minus_30, minus_60, minus_90):
        return """
            SELECT partner_id, currency_id, date_maturity, open_due,
                            open_due_currency, move_id, company_id,
            CASE
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is null THEN open_due
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_1_30,
            CASE
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is null THEN open_due
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_30_60,
            CASE
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is null THEN open_due
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_60_90,
            CASE
                WHEN date_maturity <= '%s' AND currency_id is null
                                THEN open_due
                WHEN date_maturity <= '%s' AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_over_90
            FROM Q1
            GROUP BY partner_id, currency_id, date_maturity, open_due,
                                open_due_currency, move_id, company_id
        """ % (minus_30, today, minus_30, today, minus_60,
               minus_30, minus_60, minus_30, minus_90, minus_60, minus_90,
               minus_60, minus_90, minus_90)

    def _show_buckets_sql_q2_payable(self, today, minus_30, minus_60, minus_90):
        return """
            SELECT partner_id, currency_id, date_maturity, open_due,
                            open_due_currency, move_id, company_id,
            CASE
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is null THEN open_due
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_1_30,
            CASE
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is null THEN open_due
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_30_60,
            CASE
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is null THEN open_due
                WHEN '%s' < date_maturity AND date_maturity <= '%s'
                                AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_60_90,
            CASE
                WHEN date_maturity <= '%s' AND currency_id is null
                                THEN open_due
                WHEN date_maturity <= '%s' AND currency_id is not null
                                THEN open_due_currency
                ELSE 0.0
            END as b_over_90
            FROM Q1
            GROUP BY partner_id, currency_id, date_maturity, open_due,
                                open_due_currency, move_id, company_id
        """ % (minus_30, today, minus_30, today, minus_60,
               minus_30, minus_60, minus_30, minus_90, minus_60, minus_90,
               minus_60, minus_90, minus_90)

    def _show_buckets_sql_q3(self, company_id):
        return """
            SELECT Q2.partner_id, b_1_30, b_30_60, b_60_90, b_over_90,
            COALESCE(Q2.currency_id, c.currency_id) AS currency_id
            FROM Q2
            JOIN res_company c ON (c.id = Q2.company_id)
            WHERE c.id = %s
        """ % company_id

    def _show_buckets_sql_q3_payable(self, company_id):
        return """
            SELECT Q2.partner_id, b_1_30, b_30_60, b_60_90, b_over_90,
            COALESCE(Q2.currency_id, c.currency_id) AS currency_id
            FROM Q2
            JOIN res_company c ON (c.id = Q2.company_id)
            WHERE c.id = %s
        """ % company_id

    def _show_buckets_sql_q3_receivable_and_payable(self, company_id):
        return """
            SELECT Q2.partner_id, b_1_30, b_30_60, b_60_90, b_over_90,
            COALESCE(Q2.currency_id, c.currency_id) AS currency_id
            FROM Q2
            JOIN res_company c ON (c.id = Q2.company_id)
            WHERE c.id = %s
        """ % company_id

    def _show_overdue_sql_q3(self, company_id):
        return f"""
            SELECT Q2.partner_id, current,
            COALESCE(Q2.currency_id, c.currency_id) AS currency_id
            FROM Q2
            JOIN res_company c ON c.id = Q2.company_id
            WHERE c.id = {company_id}
        """

    def _show_buckets_sql_q4(self):
        return """
            SELECT partner_id, currency_id,
                                sum(b_1_30) as b_1_30,
                                sum(b_30_60) as b_30_60,
                                sum(b_60_90) as b_60_90,
                                sum(b_over_90) as b_over_90
            FROM Q3
            GROUP BY partner_id, currency_id
        """

    def _show_buckets_sql_q4_payable(self):
        return """
            SELECT partner_id, currency_id,
                                sum(b_1_30) as b_1_30,
                                sum(b_30_60) as b_30_60,
                                sum(b_60_90) as b_60_90,
                                sum(b_over_90) as b_over_90
            FROM Q3
            GROUP BY partner_id, currency_id
        """

    def _show_buckets_sql_q4_receivable_and_payable(self):
        return """
            SELECT partner_id, currency_id,
                                sum(b_1_30) as b_1_30,
                                sum(b_30_60) as b_30_60,
                                sum(b_60_90) as b_60_90,
                                sum(b_over_90) as b_over_90
            FROM Q3
            GROUP BY partner_id, currency_id
        """

    def _show_overdue_sql_q4(self):
        return """
            SELECT partner_id, currency_id,
                                sum(current) as current
            FROM Q3
            GROUP BY partner_id, currency_id
        """

    _bucket_dates = {
        'today': fields.date.today(),
        'minus_30': fields.date.today() - timedelta(days=30),
        'minus_60': fields.date.today() - timedelta(days=60),
        'minus_90': fields.date.today() - timedelta(days=90),
    }

    def _get_account_show_buckets(self, company_id, partner_ids, date_start, date_end):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_end = datetime.strptime(
            date_end, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s),
        Q3 AS (%s), Q4 AS (%s)
        SELECT partner_id, currency_id, b_1_30, b_30_60, b_60_90, b_over_90,
                            b_1_30+b_30_60+b_60_90+b_over_90
                            AS balance
        FROM Q4
        GROUP BY partner_id, currency_id, b_1_30, b_30_60, b_60_90,
            b_over_90""" % (
            self._show_buckets_sql_q1(partners, date_start, date_end),
            self._show_buckets_sql_q2(
                self._bucket_dates['today'],
                self._bucket_dates['minus_30'],
                self._bucket_dates['minus_60'],
                self._bucket_dates['minus_90']),
            self._show_buckets_sql_q3(company_id),
            self._show_buckets_sql_q4()))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _get_account_show_buckets_payable(self, company_id, partner_ids, date_start, date_end):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_start = datetime.strptime(
            date_start, DEFAULT_SERVER_DATE_FORMAT).date()
        date_end = datetime.strptime(
            date_end, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s),
        Q3 AS (%s), Q4 AS (%s)
        SELECT partner_id, currency_id, b_1_30, b_30_60, b_60_90,b_over_90,
                            b_1_30+b_30_60+b_60_90+b_over_90
                            AS balance
        FROM Q4
        GROUP BY partner_id, currency_id, b_1_30, b_30_60, b_60_90,
            b_over_90""" % (
            self._show_buckets_sql_q1_payable(partners, date_start, date_end),
            self._show_buckets_sql_q2_payable(
                self._bucket_dates['today'],
                self._bucket_dates['minus_30'],
                self._bucket_dates['minus_60'],
                self._bucket_dates['minus_90']),
            self._show_buckets_sql_q3_payable(company_id),
            self._show_buckets_sql_q4_payable()))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _get_account_show_buckets_receivable_and_payable(self, company_id, partner_ids, date_start, date_end):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_end = datetime.strptime(
            date_end, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s),
        Q3 AS (%s), Q4 AS (%s)
        SELECT partner_id, currency_id, b_1_30, b_30_60, b_60_90, b_over_90,
                            b_1_30+b_30_60+b_60_90+b_over_90
                            AS balance
        FROM Q4
        GROUP BY partner_id, currency_id, b_1_30, b_30_60, b_60_90,
        b_over_90""" % (
            self._show_buckets_sql_q1_receivable_and_payable(partners, date_start, date_end),
            self._show_buckets_sql_q2_receivable_and_payable(
                self._bucket_dates['today'],
                self._bucket_dates['minus_30'],
                self._bucket_dates['minus_60'],
                self._bucket_dates['minus_90']),
            self._show_buckets_sql_q3_receivable_and_payable(company_id),
            self._show_buckets_sql_q4_receivable_and_payable()))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _get_account_show_overdue(self, company_id, partner_ids, date_end):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_end = datetime.strptime(
            date_end, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s),
        Q3 AS (%s), Q4 AS (%s)
        SELECT partner_id, currency_id, current
        FROM Q4
        GROUP BY partner_id, currency_id, current
            """ % (
            self._show_overdue_sql_q1(partners, date_end),
            self._show_overdue_sql_q2(date_end),
            self._show_overdue_sql_q3(company_id),
            self._show_overdue_sql_q4()))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _get_account_show_overdue_payable(self, company_id, partner_ids, date_end):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_end = datetime.strptime(
            date_end, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s),
        Q3 AS (%s), Q4 AS (%s)
        SELECT partner_id, currency_id, current
        FROM Q4
        GROUP BY partner_id, currency_id, current
            """ % (
            self._show_overdue_sql_q1_payable(partners, date_end),
            self._show_overdue_sql_q2(date_end),
            self._show_overdue_sql_q3(company_id),
            self._show_overdue_sql_q4()))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _get_account_show_overdue_receivable_and_payable(self, company_id, partner_ids, date_end):
        res = dict(map(lambda x: (x, []), partner_ids))
        partners = ', '.join([str(i) for i in partner_ids])
        date_end = datetime.strptime(
            date_end, DEFAULT_SERVER_DATE_FORMAT).date()
        self.env.cr.execute("""WITH Q1 AS (%s), Q2 AS (%s),
        Q3 AS (%s), Q4 AS (%s)
        SELECT partner_id, currency_id, current
        FROM Q4
        GROUP BY partner_id, currency_id, current
            """ % (
            self._show_overdue_sql_q1_receivable_and_payable(partners, date_end),
            self._show_overdue_sql_q2(date_end),
            self._show_overdue_sql_q3(company_id),
            self._show_overdue_sql_q4()))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        company_id = data['company_id']
        partner_ids = data['partner_ids']
        date_start = data['date_start']
        date_end = data['date_end']
        today = fields.Date.today()

        # Initialize dictionaries
        overdues_to_display = {}
        balance_start_to_display, buckets_to_display = {}, {}
        lines_to_display, amount_due = {}, {}
        currency_to_display = {}
        today_display, date_start_display, date_end_display = {}, {}, {}

        # Initialize variables to avoid UnboundLocalError
        balance_start = {}
        lines = {}
        overdues = {}
        buckets = {}

        # Assign values based on report_type
        if data['report_type'] == 'income':
            balance_start = self._get_account_initial_balance(company_id, partner_ids, date_start)
            lines = self._get_account_display_lines(company_id, partner_ids, date_start, date_end)
            overdues = self._get_account_show_overdue(company_id, partner_ids, date_end)
            if data['show_aging_buckets']:
                buckets = self._get_account_show_buckets(company_id, partner_ids, date_start, date_end)

        elif data['report_type'] == 'expense':
            balance_start = self._get_account_initial_balance_payable(company_id, partner_ids, date_start)
            lines = self._get_account_display_lines_payable(company_id, partner_ids, date_start, date_end)
            overdues = self._get_account_show_overdue_payable(company_id, partner_ids, date_end)
            if data['show_aging_buckets']:
                buckets = self._get_account_show_buckets_payable(company_id, partner_ids, date_start, date_end)

        elif data['report_type'] == 'receivable_and_payable':
            balance_start = self._get_account_initial_balance_receivable_and_payable(company_id, partner_ids,
                                                                                     date_start)
            lines = self._get_account_display_lines_receivable_and_payable(company_id, partner_ids, date_start,
                                                                           date_end)
            overdues = self._get_account_show_overdue_receivable_and_payable(company_id, partner_ids, date_end)
            if data['show_aging_buckets']:
                buckets = self._get_account_show_buckets_receivable_and_payable(company_id, partner_ids, date_start,
                                                                                date_end)

        for partner_id in partner_ids:
            today_display[partner_id] = self._format_date_to_partner_lang(today, partner_id)
            date_start_display[partner_id] = self._format_date_to_partner_lang(date_start, partner_id)
            date_end_display[partner_id] = self._format_date_to_partner_lang(date_end, partner_id)

            lines_to_display[partner_id], amount_due[partner_id] = {}, {}
            currency_to_display[partner_id], overdues_to_display[partner_id] = {}, {}
            balance_start_to_display[partner_id] = {}

            for line in balance_start.get(partner_id, []):
                currency = self.env['res.currency'].browse(line['currency_id'])
                balance_start_to_display[partner_id][currency] = line['balance']

            for line in lines.get(partner_id, []):
                currency = self.env['res.currency'].browse(line['currency_id'])
                if currency not in lines_to_display[partner_id]:
                    lines_to_display[partner_id][currency] = []
                    currency_to_display[partner_id][currency] = currency
                    amount_due[partner_id][currency] = balance_start_to_display[partner_id].get(currency, 0.0)
                if not line['blocked']:
                    amount_due[partner_id][currency] += line['amount']
                line['balance'] = amount_due[partner_id][currency]
                line['date'] = self._format_date_to_partner_lang(line['date'], partner_id)
                line['date_maturity'] = self._format_date_to_partner_lang(line['date_maturity'], partner_id)
                lines_to_display[partner_id][currency].append(line)

            for line in overdues.get(partner_id, []):
                currency = self.env['res.currency'].browse(line['currency_id'])
                overdues_to_display[partner_id][currency] = line['current']

            if data['show_aging_buckets']:
                buckets_to_display[partner_id] = {}
                for line in buckets.get(partner_id, []):
                    currency = self.env['res.currency'].browse(line['currency_id'])
                    if currency not in buckets_to_display[partner_id]:
                        buckets_to_display[partner_id][currency] = []
                    buckets_to_display[partner_id][currency] = line

        return {
            'doc_ids': partner_ids,
            'doc_model': 'res.partner',
            'docs': self.env['res.partner'].browse(partner_ids),
            'amount_due': amount_due,
            'total_overdues': overdues_to_display,
            'balance_forward': balance_start_to_display,
            'lines': lines_to_display,
            'buckets': buckets_to_display,
            'company_id': self.env.user.company_id,
            'currencies': currency_to_display,
            'show_buckets': data['show_aging_buckets'],
            'filter_non_due_partners': data['filter_partners_non_due'],
            'date_start': date_start_display,
            'date_end': date_end_display,
            'date': today_display,
        }

    # Define that field in python and make it storable and try installing it.
