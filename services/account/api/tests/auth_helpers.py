from types import SimpleNamespace
from unittest.mock import patch

import jwt
from cryptography.hazmat.primitives.asymmetric import ec

TEST_JWT_AUDIENCE = "authenticated"
TEST_JWT_ISSUER = "https://test-project.supabase.co/auth/v1"
TEST_JWKS_URL = "https://test-project.supabase.co/auth/v1/.well-known/jwks.json"
TEST_PRIVATE_KEY = ec.generate_private_key(ec.SECP256R1())
TEST_PUBLIC_KEY = TEST_PRIVATE_KEY.public_key()


def _fake_signing_key_for(token):
    return SimpleNamespace(key=TEST_PUBLIC_KEY)


def authorization_header_for(supabase_user_id):
    token = jwt.encode(
        {
            "sub": str(supabase_user_id),
            "aud": TEST_JWT_AUDIENCE,
            "iss": TEST_JWT_ISSUER,
        },
        TEST_PRIVATE_KEY,
        algorithm="ES256",
        headers={"kid": "test-key"},
    )
    return f"Bearer {token}"


class SupabaseAuthTestMixin:
    def setUp(self):
        self.jwks_client_patcher = patch(
            "api.auth._get_jwks_client",
            return_value=SimpleNamespace(
                get_signing_key_from_jwt=_fake_signing_key_for
            ),
        )
        self.jwks_client_patcher.start()
        self.addCleanup(self.jwks_client_patcher.stop)
        super().setUp()
