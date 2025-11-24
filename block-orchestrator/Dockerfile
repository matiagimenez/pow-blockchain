FROM astral/uv:0.9.11-python3.12-trixie-slim


WORKDIR /app

RUN useradd -m -d /home/nonroot -s /bin/bash nonroot
RUN chown -R nonroot:nonroot /app

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY block_orchestrator block_orchestrator

USER nonroot

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "block_orchestrator.main:main", "--host", "0.0.0.0", "--port", "8000"]
