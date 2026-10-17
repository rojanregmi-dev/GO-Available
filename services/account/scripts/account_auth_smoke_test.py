"""Check that a real Supabase bearer token reaches the Account API."""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_ACCOUNT_URL = "http://127.0.0.1:8000/api/v1/account/me"


def main():
    token = os.getenv("SUPABASE_SMOKE_TEST_TOKEN")
    if not token:
        print("SUPABASE_SMOKE_TEST_TOKEN is required.", file=sys.stderr)
        return 2

    account_url = os.getenv("ACCOUNT_API_URL", DEFAULT_ACCOUNT_URL)
    request = Request(
        account_url,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )

    try:
        with urlopen(request, timeout=10) as response:
            status_code = response.status
            response_body = response.read().decode("utf-8")
    except HTTPError as error:
        status_code = error.code
        response_body = error.read().decode("utf-8")
    except URLError as error:
        print(f"Account API is unreachable: {error.reason}", file=sys.stderr)
        return 1

    print(f"Account API status: {status_code}")
    try:
        print(json.dumps(json.loads(response_body), indent=2, sort_keys=True))
    except json.JSONDecodeError:
        print(response_body)

    if status_code in {200, 404}:
        print("Authentication reached the Account Service successfully.")
        return 0

    print("Authentication smoke test failed.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
