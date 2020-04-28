# Alerta - Pinja Azure monitor

Modified version to support better formatting and common alert schema based on <https://github.com/alerta/alerta-contrib/tree/master/webhooks/azuremonitor>.

Features:

- Accepts alerts using `azureMonitorCommonAlertSchema` in azure web hooks.
- Parse any link in description as clickable link.
- Parse link from alert to azure portal which gives easy access to original alert and resources.

To install this extension to alerta:

```bash
pip install git+https://github.com/by-pinja/alerta-azure-webhook.git#subdirectory=webhook
```

## Query parameters

You can add certain additional parameters to webhooks for additional information that isn't available in common alert schema payload.

For example `http://localhost:8080/api/webhooks/pinjaazuremonitor?api-key=apikeyhere&service=my-best-service&environment=Staging`

- Service: `service`
- Environment: `environment` (defaults to 'Production').
- Runbook: `runbook_url`, add custom link to runbook with alerts.

## Requirements for development

Repository contains development container that can be used with VScode remote container development.

If you prefer not to use container based development see details what is required for environment from [./devcontainer](./devcontainer) folder.

In development container with VSCode just run F5 and it will execute tests which you can use to further develop and debug webhook code.

## Spinning instance for testing

If you have docker and docker-compose installed you can test alerta with this web hook easilyt. To start alerta that contains webhook installed for testing simply run:

```powershell
docker-compose up --build
```

And then you navigate to <http://localhost:8080> and login with `admin@alerta.io/alerta`. Get ApiKey from settings and use it to send
new alert via azure monitoring web hook:

```powershell
./scripts/SendAlert -ApiKey YourApiKeyHere -Condition Fired
```

Now you should see new alert in alerta at <http://localhost:8080>.
