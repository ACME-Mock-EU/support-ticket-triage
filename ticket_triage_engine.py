# Support Ticket Triage Engine
# Intelligent ticket routing, classification, and priority assignment

import pandas as pd
from datetime import datetime, timedelta

class TicketTriageEngine:
    def __init__(self):
        self.priority_mapping = {
            'sso_token': 'P1',  # Authentication critical
            'api_403_sync': 'P1',  # Critical sync failure
            'api_403_scope': 'P2',  # Scope mismatch, can workaround
            'invoice_dispute': 'P2',  # Billing, important but not blocking
            'har_request': 'P3',  # Diagnostic, lower priority
        }
        self.p1_sla_hours = 4
        self.p2_sla_hours = 24
        self.p3_sla_hours = 48
    
    def load_tickets(self, filepath):
        '''Load Q3 2026 support ticket data'''
        df = pd.read_excel(filepath)
        return df
    
    def classify_ticket(self, ticket_row):
        '''Classify ticket by issue type and assign priority'''
        issue_type = 'unknown'
        
        if 'SSO Token' in str(ticket_row):
            issue_type = 'sso_token'
        elif '403' in str(ticket_row):
            if 'scope' in str(ticket_row).lower():
                issue_type = 'api_403_scope'
            else:
                issue_type = 'api_403_sync'
        elif 'Invoice' in str(ticket_row):
            issue_type = 'invoice_dispute'
        elif 'HAR' in str(ticket_row):
            issue_type = 'har_request'
        
        priority = self.priority_mapping.get(issue_type, 'P3')
        sla_hours = self._get_sla_hours(priority)
        
        return {
            'issue_type': issue_type,
            'priority': priority,
            'sla_hours': sla_hours
        }
    
    def _get_sla_hours(self, priority):
        '''Get SLA hours based on priority'''
        if priority == 'P1':
            return self.p1_sla_hours
        elif priority == 'P2':
            return self.p2_sla_hours
        else:
            return self.p3_sla_hours
    
    def route_ticket(self, ticket_data):
        '''Route ticket to appropriate team'''
        priority = ticket_data.get('priority', 'P3')
        issue_type = ticket_data.get('issue_type', 'unknown')
        
        routing = {}
        
        if priority == 'P1':
            routing['team'] = 'Engineering'
            routing['urgency'] = 'Immediate'
            routing['escalation'] = 'Director-level'
        elif priority == 'P2':
            if issue_type == 'invoice_dispute':
                routing['team'] = 'RevOps'
                routing['urgency'] = 'High'
            else:
                routing['team'] = 'Engineering'
                routing['urgency'] = 'High'
                routing['escalation'] = 'Hotfix planned'
        else:
            routing['team'] = 'Support Queue'
            routing['urgency'] = 'Normal'
        
        return routing
    
    def detect_false_backlog(self, ticket_row):
        '''Detect stale/false backlog tickets'''
        backlog_status = ticket_row.get('False Backlog', '')
        
        if 'Confirmed false' in str(backlog_status):
            return {'is_false': True, 'confidence': 0.95, 'action': 'Quarantine'}
        elif 'Likely' in str(backlog_status):
            return {'is_false': True, 'confidence': 0.70, 'action': 'Review'}
        elif 'Possible' in str(backlog_status):
            return {'is_false': True, 'confidence': 0.50, 'action': 'Monitor'}
        else:
            return {'is_false': False, 'confidence': 1.0, 'action': 'Active'}
    
    def engineering_triage_status(self, ticket_row):
        '''Determine engineering triage status and action'''
        eng_status = ticket_row.get('ENG-Assist Requested', 'Not required')
        
        status_mapping = {
            'Not required': 'Closed',
            'Queued for weekly triage': 'Queued',
            'ENG engaged (P1)': 'In Progress - P1',
            'ENG-Assist requested': 'Pending Assignment',
            'Hotfix in progress (P2)': 'In Progress - P2',
            'Yes': 'Requested',
            'No': 'Not Needed'
        }
        
        return status_mapping.get(eng_status, 'Unknown')
    
    def revops_validation_status(self, ticket_row):
        '''Determine RevOps validation status'''
        revops_status = ticket_row.get('RevOps Validation Pending,', 'Not required')
        
        status_mapping = {
            'Not required': 'No validation needed',
            'Queued for weekly triage': 'Queued',
            'RevOps validation required': 'Validation Pending',
            'RevOps + CS joint review': 'Joint Review In Progress',
        }
        
        return status_mapping.get(revops_status, 'Unknown')
    
    def calculate_sla_breach(self, created_date, priority):
        '''Calculate if ticket is breaching SLA'''
        sla_hours = self._get_sla_hours(priority)
        created = pd.to_datetime(created_date)
        now = datetime.now()
        hours_elapsed = (now - created).total_seconds() / 3600
        
        return {
            'hours_elapsed': round(hours_elapsed, 1),
            'sla_hours': sla_hours,
            'is_breached': hours_elapsed > sla_hours,
            'breach_hours': max(0, hours_elapsed - sla_hours)
        }
    
    def burndown_velocity(self, tickets_df):
        '''Calculate backlog burn-down velocity'''
        total_tickets = len(tickets_df)
        p1_count = sum(1 for _, row in tickets_df.iterrows() if self.classify_ticket(row).get('priority') == 'P1')
        p2_count = sum(1 for _, row in tickets_df.iterrows() if self.classify_ticket(row).get('priority') == 'P2')
        p3_count = total_tickets - p1_count - p2_count
        
        false_backlog = sum(1 for _, row in tickets_df.iterrows() if self.detect_false_backlog(row).get('is_false'))
        actionable_tickets = total_tickets - false_backlog
        
        velocity = {
            'total_backlog': total_tickets,
            'p1_tickets': p1_count,
            'p2_tickets': p2_count,
            'p3_tickets': p3_count,
            'false_backlog_count': false_backlog,
            'false_backlog_pct': round((false_backlog / total_tickets) * 100, 1),
            'actionable_tickets': actionable_tickets,
            'p1_pct': round((p1_count / total_tickets) * 100, 1),
            'engineering_engagement_rate': round((p1_count + p2_count) / total_tickets * 100, 1)
        }
        
        return velocity

if __name__ == "__main__":
    engine = TicketTriageEngine()
    print("Ticket Triage Engine v1.0 initialized")
    print("Q3 2026 Backlog: 50 tickets | False backlog detection: Active")
