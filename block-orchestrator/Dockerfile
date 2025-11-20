FROM uv:0.9.10-python3.12-trixie-slim

WORKDIR /app

RUN useradd -m -d /home/nonroot -s /bin/bash nonroot
RUN chown -R nonroot:nonroot /app
RUN apt-get update && apt-get install -y

COPY pyproject.toml pyproject.toml
COPY block_orchestrator/ block_orchestrator/

USER nonroot

RUN uv pip install -r requirements.txt

EXPOSE 5000

CMD ["uv", "run", "block_orchestrator.main:app", "--host", "0.0.0.0", "--port", "5000"]