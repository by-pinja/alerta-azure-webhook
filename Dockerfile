FROM alerta/alerta-web

COPY ./ /opt/src/
RUN /venv/bin/pip install /opt/src/webhook