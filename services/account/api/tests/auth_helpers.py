import jwt


TEST_JWT_SECRET = "test-secret-that-is-at-least-32-bytes"
TEST_JWT_AUDIENCE = "authenticated"


def authorization_header_for(supabase_user_id):
    token = jwt.encode(
        {"sub": str(supabase_user_id), "aud": TEST_JWT_AUDIENCE},
        TEST_JWT_SECRET,
        algorithm="HS256",
    )
    return f"Bearer {token}"
