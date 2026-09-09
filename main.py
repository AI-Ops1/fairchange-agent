"""AgentCore Runtime entrypoint for FairChange."""

from fairchange.runtime import create_app


if __name__ == "__main__":
    create_app().run()
