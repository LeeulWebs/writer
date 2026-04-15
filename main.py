import sys
from streamlit.web import cli as stcli


def main():
    sys.argv = [
        "streamlit", "run", "app.py",
        "--server.port=5000",
        "--server.address=0.0.0.0"
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
