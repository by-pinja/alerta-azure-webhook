import json
import urllib
import re

from dateutil.parser import parse as parse_date

from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase

SEVERITY_MAP = {
    'Sev0': 'critical',       # Critical
    'Sev1': 'major',          # Error
    'Sev2': 'warning',        # Warning
    'Sev3': 'informational',  # Informational
    'Sev4': 'debug'           # Verbose
}

STATUS_MAP = {
    'Fired': 'Open',
    'Resolved': 'Closed'
}

DEFAULT_SEVERITY_LEVEL = '3'  # 'warning'
DEFAULT_STATUS = 'Fired'

class AzureMonitorWebhook(WebhookBase):
    """
    Microsoft Azure Monitor alerts webhook
    https://docs.microsoft.com/en-us/azure/azure-monitor/platform/alerts-webhooks
    """

    def _resolve_alert_id_short(self, full_alert_id):
        matches = re.search(r".*/(.*)", full_alert_id)
        if matches:
            return matches.group(1)
        else:
            return full_alert_id

    def _replace_text_with_ahref_links(self, text):
        return re.sub(r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", "<a href=\"\\1\">\\1</a>",  text)


    def incoming(self, query_string, payload):

        if 'schemaId' not in payload:
            raise Exception("Invalid payload, no schemaId defined")

        if payload['schemaId'] != 'azureMonitorCommonAlertSchema':
            raise Exception("Only 'azureMonitorCommonAlertSchema' currently supported, please enable common alert schema for alert hook!")

        essentials = payload['data']['essentials']

        severity = SEVERITY_MAP[essentials.get('severity', DEFAULT_SEVERITY_LEVEL)]
        status = STATUS_MAP[essentials.get('monitorCondition', DEFAULT_STATUS)]

        encoded_alert_id = urllib.parse.quote_plus(essentials['alertId'])

        resource = "" if essentials['alertTargetIDs'] is None else ",".join(essentials['alertTargetIDs'])

        event = "{} ({})".format(essentials['alertRule'], self._resolve_alert_id_short(essentials['alertId']))
        environment = query_string.get('environment', 'Production')
        service = query_string.get('service', 'not_defined')

        group = query_string.get('group', '')
        tags = []

        event_type = essentials['signalType']
        text = self._replace_text_with_ahref_links(essentials['description'] or '')
        create_time = parse_date(essentials['firedDateTime'])

        attributes = {}

        incident_url = "https://ms.portal.azure.com/#blade/Microsoft_Azure_Monitoring/AlertDetailsTemplateBlade/alertId/{}".format(encoded_alert_id)
        attributes['AzureMonitoringAlertUrl'] = "<a href=\"{}\" target=\"_blank\">{}</a>".format(incident_url, incident_url)

        #if query_string.get('runbook_url'):
        attributes['runBook'] = "<a href=\"{}\" target=\"_blank\">{}</a>".format(query_string.get('runbook_url', ''), query_string.get('runbook_url', ''))

        return Alert(
            resource=resource,
            event=event,
            environment=environment,
            severity=severity,
            service=[service],
            group=group,
            status=status,
            value="",
            text=text,
            tags=tags,
            attributes=attributes,
            origin='Azure monitoring (webhook)',
            type=event_type,
            create_time=create_time,
            raw_data=json.dumps(payload)
        )
