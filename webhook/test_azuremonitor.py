import json
import unittest

class AzureMonitoringWebhookTestCase(unittest.TestCase):

    def setUp(self):
        import alerta_pinjaazuremonitor
        from alerta.app import create_app, custom_webhooks

        test_config = {
            'TESTING': True,
            'AUTH_REQUIRED': False
        }
        self.app = create_app(test_config)
        self.client = self.app.test_client()

        custom_webhooks.webhooks['azuremonitor'] = alerta_pinjaazuremonitor.AzureMonitorWebhook()

    def test_azuremonitor_webhook_commonschema_fired(self):

        """ See https://docs.microsoft.com/en-us/azure/azure-monitor/platform/alerts-common-schema-definitions """

        new_metric_alert = r"""
        {
            "schemaId": "azureMonitorCommonAlertSchema",
            "data": {
                "essentials": {
                    "alertId": "/subscriptions/90e39383-9de0-4f45-a582-3ab5a6428637/providers/Microsoft.AlertsManagement/alerts/3dccd863-894e-44ed-a8bf-f73f15e3f48c",
                    "alertRule": "Testrule too many good results",
                    "severity": "Sev1",
                    "signalType": "Metric",
                    "monitorCondition": "Fired",
                    "monitoringService": "Platform",
                    "alertTargetIDs": [
                        "/subscriptions/90e39383-9de0-4f45-a582-3ab5a6428637/resourcegroups/testalert1/providers/microsoft.web/sites/alert-testing-web-foo"
                    ],
                    "originAlertId": "90e39383-9de0-4f45-a582-3ab5a6428637_testalert1_microsoft.insights_metricAlerts_foobar_-1615335870",
                    "firedDateTime": "2020-04-28T11:07:37.1106903Z",
                    "description": "Description here, links https://fixme.io, http://foo.bar",
                    "essentialsVersion": "1.0",
                    "alertContextVersion": "1.0"
                },
                "alertContext": {
                    "properties": null,
                    "conditionType": "SingleResourceMultipleMetricCriteria",
                    "condition": {
                        "windowSize": "PT1M",
                        "allOf": [
                            {
                                "metricName": "Http2xx",
                                "metricNamespace": "Microsoft.Web/sites",
                                "operator": "GreaterThan",
                                "threshold": "1",
                                "timeAggregation": "Total",
                                "dimensions": [
                                    {
                                        "name": "ResourceId",
                                        "value": "alert-testing-web-foo.azurewebsites.net"
                                    }
                                ],
                                "metricValue": 27,
                                "webTestName": null
                            }
                        ],
                        "windowStartTime": "2020-04-28T11:03:21.624Z",
                        "windowEndTime": "2020-04-28T11:04:21.624Z"
                    }
                }
            }
        }
        """

        response = self.client.post('/webhooks/azuremonitor', data=new_metric_alert, content_type='application/json')

        self.assertEqual(response.status_code, 201, response.data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['alert']['resource'], '/subscriptions/90e39383-9de0-4f45-a582-3ab5a6428637/resourcegroups/testalert1/providers/microsoft.web/sites/alert-testing-web-foo')
        self.assertEqual(data['alert']['event'], 'Testrule too many good results (3dccd863-894e-44ed-a8bf-f73f15e3f48c)')
        self.assertEqual(data['alert']['resource'], '/subscriptions/90e39383-9de0-4f45-a582-3ab5a6428637/resourcegroups/testalert1/providers/microsoft.web/sites/alert-testing-web-foo')
        self.assertEqual(data['alert']['severity'], 'major')
        self.assertEqual(data['alert']['status'], 'Open')

    def test_azuremonitor_webhook_commonschema_resolved(self):

        """ See https://docs.microsoft.com/en-us/azure/azure-monitor/platform/alerts-common-schema-definitions """

        new_metric_alert = r"""
        {
            "schemaId": "azureMonitorCommonAlertSchema",
            "data": {
                "essentials": {
                    "alertId": "/subscriptions/90e39383-9de0-4f45-a582-3ab5a6428637/providers/Microsoft.AlertsManagement/alerts/3dccd863-894e-44ed-a8bf-f73f15e3f48c",
                    "alertRule": "Testrule too many good results",
                    "severity": "Sev1",
                    "signalType": "Metric",
                    "monitorCondition": "Resolved",
                    "monitoringService": "Platform",
                    "alertTargetIDs": [
                        "/subscriptions/90e39383-9de0-4f45-a582-3ab5a6428637/resourcegroups/testalert1/providers/microsoft.web/sites/alert-testing-web-foo"
                    ],
                    "originAlertId": "90e39383-9de0-4f45-a582-3ab5a6428637_testalert1_microsoft.Testrule too many good results_-1615335870",
                    "firedDateTime": "2020-04-28T11:07:37.1106903Z",
                    "resolvedDateTime": "2020-04-28T11:10:41.6356374Z",
                    "description": "Description here, links https://fixme.io, http://foo.bar",
                    "essentialsVersion": "1.0",
                    "alertContextVersion": "1.0"
                },
                "alertContext": {
                    "properties": null,
                    "conditionType": "SingleResourceMultipleMetricCriteria",
                    "condition": {
                        "windowSize": "PT1M",
                        "allOf": [
                            {
                                "metricName": "Http2xx",
                                "metricNamespace": "Microsoft.Web/sites",
                                "operator": "GreaterThan",
                                "threshold": "1",
                                "timeAggregation": "Total",
                                "dimensions": [
                                    {
                                        "name": "ResourceId",
                                        "value": "alert-testing-web-foo.azurewebsites.net"
                                    }
                                ],
                                "metricValue": 0,
                                "webTestName": null
                            }
                        ],
                        "windowStartTime": "2020-04-28T11:06:21.649Z",
                        "windowEndTime": "2020-04-28T11:07:21.649Z"
                    }
                }
            }
        }
        """

        response = self.client.post('/webhooks/azuremonitor', data=new_metric_alert, content_type='application/json')

        self.assertEqual(response.status_code, 201, response.data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['alert']['status'], 'Closed')

if __name__ == '__main__':
    unittest.main()