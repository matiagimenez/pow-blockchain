import uvicorn


def main() -> None:
    uvicorn.run("block_orchestrator.api.app:app", reload=True, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
