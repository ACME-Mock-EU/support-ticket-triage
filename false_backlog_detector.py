# False Backlog Detector
# Identify and filter stale, aging, and false positive support tickets

import pandas as pd
from datetime import datetime, timedelta

class FalseBacklogDetector:
    def __init__(self):
        self.wfc_aging_threshold_weeks = 2  # Waiting for customer >2 weeks
        self.no_update_threshold_days = 7  # No activity >7 days
        self.confirmed_false_confidence = 0.95
        self.likely_false_confidence = 0.70
        self.possible_false_confidence = 0.50
    
    def detect_confirmed_false(self, ticket):
        '''Identify confirmed false backlog tickets'''
        false_status = ticket.get('False Backlog', '')
        return 'Confirmed false' in str(false_status)
    
    def detect_likely_false(self, ticket):
        '''Identify likely false backlog (WFC aging)'''
        false_status = ticket.get('False Backlog', '')
        return 'Likely' in str(false_status)
    
    def detect_possible_false(self, ticket):
        '''Identify possible false backlog (needs review)'''
        false_status = ticket.get('False Backlog', '')
        return 'Possible' in str(false_status)
    
    def analyze_false_backlog(self, tickets_df):
        '''Analyze false backlog distribution'''
        analysis = {
            'confirmed_false': 0,
            'likely_false': 0,
            'possible_false': 0,
            'actionable': 0,
            'total': len(tickets_df)
        }
        
        for _, ticket in tickets_df.iterrows():
            if self.detect_confirmed_false(ticket):
                analysis['confirmed_false'] += 1
            elif self.detect_likely_false(ticket):
                analysis['likely_false'] += 1
            elif self.detect_possible_false(ticket):
                analysis['possible_false'] += 1
            else:
                analysis['actionable'] += 1
        
        # Calculate percentages
        analysis['false_backlog_total'] = analysis['confirmed_false'] + analysis['likely_false'] + analysis['possible_false']
        analysis['false_backlog_pct'] = round((analysis['false_backlog_total'] / analysis['total']) * 100, 1)
        analysis['actionable_pct'] = round((analysis['actionable'] / analysis['total']) * 100, 1)
        
        return analysis
    
    def quarantine_false_backlog(self, tickets_df):
        '''Quarantine confirmed false backlog tickets'''
        false_backlog_tickets = []
        actionable_tickets = []
        
        for _, ticket in tickets_df.iterrows():
            if self.detect_confirmed_false(ticket):
                false_backlog_tickets.append(ticket)
            else:
                actionable_tickets.append(ticket)
        
        return {
            'false_backlog_quarantined': len(false_backlog_tickets),
            'actionable_remaining': len(actionable_tickets),
            'reduction_pct': round((len(false_backlog_tickets) / len(tickets_df)) * 100, 1)
        }
    
    def wfc_aging_analysis(self, tickets_df):
        '''Analyze Waiting for Customer (WFC) aging'''
        wfc_aging_tickets = []
        
        for _, ticket in tickets_df.iterrows():
            false_status = ticket.get('False Backlog', '')
            if 'WFC aging' in str(false_status):
                wfc_aging_tickets.append({
                    'ticket_id': ticket.get('**Ticket ID', 'Unknown'),
                    'status': false_status,
                    'confidence': self.likely_false_confidence,
                    'action': 'Review WFC status, consider follow-up'
                })
        
        return {
            'wfc_aging_count': len(wfc_aging_tickets),
            'wfc_aging_pct': round((len(wfc_aging_tickets) / len(tickets_df)) * 100, 1),
            'tickets': wfc_aging_tickets
        }
    
    def backlog_quality_report(self, tickets_df):
        '''Generate backlog quality report'''
        false_analysis = self.analyze_false_backlog(tickets_df)
        wfc_analysis = self.wfc_aging_analysis(tickets_df)
        quarantine = self.quarantine_false_backlog(tickets_df)
        
        report = {
            'total_backlog': false_analysis['total'],
            'false_backlog_pct': false_analysis['false_backlog_pct'],
            'confirmed_false': false_analysis['confirmed_false'],
            'likely_false': false_analysis['likely_false'],
            'possible_false': false_analysis['possible_false'],
            'wfc_aging': wfc_analysis['wfc_aging_count'],
            'actionable_tickets': false_analysis['actionable'],
            'recommended_action': 'Quarantine false backlog to improve visibility',
            'expected_clarity_improvement': f"Reduce apparent backlog by {false_analysis['false_backlog_pct']}%"
        }
        
        return report

if __name__ == "__main__":
    detector = FalseBacklogDetector()
    print("False Backlog Detector v1.0 initialized")
    print("Detection: Confirmed false, Likely false (WFC aging), Possible false")
