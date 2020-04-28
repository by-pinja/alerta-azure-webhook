[CmdLetBinding()]
Param(
    [string][Parameter(Mandatory)]$ApiKey,
    [ValidateSet("Fired", "Resolved")]
    [string][Parameter(Mandatory)]$Action,
    [string][Parameter()]$AlertaHost = "http://localhost:8080"
)

$bodyFired = '
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
}'


$bodyResolved = '
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
}'

$request = "http://localhost:8080/api/webhooks/pinjaazuremonitor?api-key=SzqHdwASjo0Rn9KivBvq4Ut-qyu6vl8tVbE3_87j"

Invoke-RestMethod -Method POST $request -Body $body -ContentType "application/json"
