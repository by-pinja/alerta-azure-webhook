from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name="pinja-alerta-azure-monitor",
    version=version,
    description='Alerta webhook for Azure Monitor with common schema support',
    url='https://github.com/by-pinja/alerta-azuremonitor',
    license='MIT',
    author='Pinja LTD',
    author_email='pekka.savolainen@pinja.com',
    packages=find_packages(),
    py_modules=['alerta_pinjaazuremonitor'],
    install_requires=[
        'python-dateutil'
    ],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.webhooks': [
            'pinjaazuremonitor = alerta_pinjaazuremonitor:AzureMonitorWebhook'
        ]
    }
)
