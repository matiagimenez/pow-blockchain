FROM astral/uv:0.9.11-python3.12-trixie-slim

WORKDIR /app

RUN useradd -m -d /home/nonroot -s /bin/bash nonroot
RUN chown -R nonroot:nonroot /app

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY pool_manager pool_manager

USER nonroot

RUN uv sync --frozen

EXPOSE 5000

CMD ["uv", "run", "uvicorn", "pool_manager.main:main", "--host", "0.0.0.0", "--port", "5000"]
    