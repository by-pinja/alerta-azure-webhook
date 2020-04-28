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

    def test_azuremonitor_webhook_commonschema(self):

        """ See https://docs.microsoft.com/en-us/azure/azure-monitor/platform/alerts-common-schema-definitions """

        new_metric_alert = r"""
        {
            "schemaId": "azureMonitorCommonAlertSchema",
            "data": {
                "essentials": {
                    "alertId": "/subscriptions/<subscription ID>/providers/Microsoft.AlertsManagement/alerts/b9569717-bc32-442f-add5-83a997729330",
                    "alertRule": "WCUS-R2-Gen2",
                    "severity": "Sev3",
                    "signalType": "Metric",
                    "monitorCondition": "Resolved",
                    "monitoringService": "Platform",
                    "alertTargetIDs": [
                        "/subscriptions/<subscription ID>/resourcegroups/pipelinealertrg/providers/microsoft.compute/virtualmachines/wcus-r2-gen2"
                    ],
                    "originAlertId": "3f2d4487-b0fc-4125-8bd5-7ad17384221e_PipeLineAlertRG_microsoft.insights_metricAlerts_WCUS-R2-Gen2_-117781227",
                    "firedDateTime": "2019-03-22T13:58:24.3713213Z",
                    "resolvedDateTime": "2019-03-22T14:03:16.2246313Z",
                    "description": "Such bad alert, help here https://helpme.io/ or http://helpme.foo",
                    "essentialsVersion": "1.0",
                    "alertContextVersion": "1.0"
                },
                "alertContext": {
                    "properties": null,
                    "conditionType": "SingleResourceMultipleMetricCriteria",
                    "condition": {
                        "windowSize": "PT5M",
                        "allOf": [
                        {
                            "metricName": "Percentage CPU",
                            "metricNamespace": "Microsoft.Compute/virtualMachines",
                            "operator": "GreaterThan",
                            "threshold": "25",
                            "timeAggregation": "Average",
                            "dimensions": [
                            {
                                "name": "ResourceId",
                                "value": "3efad9dc-3d50-4eac-9c87-8b3fd6f97e4e"
                            }
                            ],
                            "metricValue": 7.727
                        }
                        ]
                    }
                }
            }
        }
        """

        response = self.client.post('/webhooks/azuremonitor', data=new_metric_alert, content_type='application/json')

        self.assertEqual(response.status_code, 201, response.data)
        data = json.loads(response.data.decode('utf-8'))
        # self.assertEqual(data['alert']['resource'], 'diag500')
        # self.assertEqual(data['alert']['event'], 'StorageCheck')
        # self.assertEqual(data['alert']['environment'], 'Production')
        # self.assertEqual(data['alert']['severity'], 'informational')
        # self.assertEqual(data['alert']['status'], 'open')
        # self.assertEqual(data['alert']['service'], ['Microsoft.Storage/storageAccounts'])
        # self.assertEqual(data['alert']['group'], 'Contoso')
        # self.assertEqual(data['alert']['value'], '1 Transactions')
        # self.assertEqual(data['alert']['text'], 'INFORMATIONAL: 1 Transactions (GreaterThan 0)')
        # self.assertEqual(sorted(data['alert']['tags']), ['key1=value1', 'key2=value2'])

        # new_metric_alert = r"""
        # {
        #     "schemaId": "azureMonitorCommonAlertSchema",
        #     "data": {
        #         "essentials": {
        #         "alertId": "/subscriptions/<subscription ID>/providers/Microsoft.AlertsManagement/alerts/b9569717-bc32-442f-add5-83a997729330",
        #         "alertRule": "WCUS-R2-Gen2",
        #         "severity": "Sev3",
        #         "signalType": "Metric",
        #         "monitorCondition": "Resolved",
        #         "monitoringService": "Platform",
        #         "alertTargetIDs": [
        #             "/subscriptions/<subscription ID>/resourcegroups/pipelinealertrg/providers/microsoft.compute/virtualmachines/wcus-r2-gen2"
        #         ],
        #         "originAlertId": "3f2d4487-b0fc-4125-8bd5-7ad17384221e_PipeLineAlertRG_microsoft.insights_metricAlerts_WCUS-R2-Gen2_-117781227",
        #         "firedDateTime": "2019-03-22T13:58:24.3713213Z",
        #         "resolvedDateTime": "2019-03-22T14:03:16.2246313Z",
        #         "description": "",
        #         "essentialsVersion": "1.0",
        #         "alertContextVersion": "1.0"
        #         },
        #         "alertContext": {
        #         "properties": null,
        #         "conditionType": "SingleResourceMultipleMetricCriteria",
        #         "condition": {
        #             "windowSize": "PT5M",
        #             "allOf": [
        #             {
        #                 "metricName": "Percentage CPU",
        #                 "metricNamespace": "Microsoft.Compute/virtualMachines",
        #                 "operator": "GreaterThan",
        #                 "threshold": "25",
        #                 "timeAggregation": "Average",
        #                 "dimensions": [
        #                 {
        #                     "name": "ResourceId",
        #                     "value": "3efad9dc-3d50-4eac-9c87-8b3fd6f97e4e"
        #                 }
        #                 ],
        #                 "metricValue": 7.727
        #             }
        #             ]
        #         }
        #         }
        #     }
        # }
        # """

        # response = self.client.post('/webhooks/azuremonitor?environment=Development', data=new_metric_alert, content_type='application/json')

        # self.assertEqual(response.status_code, 201, response.data)
        # data = json.loads(response.data.decode('utf-8'))
        # self.assertEqual(data['alert']['resource'], 'web01')
        # self.assertEqual(data['alert']['event'], 'CpuUtilHigh')
        # self.assertEqual(data['alert']['environment'], 'Development')
        # self.assertEqual(data['alert']['severity'], 'ok')
        # self.assertEqual(data['alert']['status'], 'closed')
        # self.assertEqual(data['alert']['service'], ['Microsoft.Compute/virtualMachines'])
        # self.assertEqual(data['alert']['group'], 'Web')
        # self.assertEqual(data['alert']['value'], '85 Percentage CPU')
        # self.assertEqual(data['alert']['text'], 'OK: 85 Percentage CPU (GreaterThan 90)')
        # self.assertEqual(sorted(data['alert']['tags']), [])

if __name__ == '__main__':
    unittest.main()