import uvicorn


def main() -> None:
    uvicorn.run(
        "pow_miner.api.app:app",
        reload=True,
        host="0.0.0.0",
        port=5000,
    )


if __name__ == "__main__":
    main()
