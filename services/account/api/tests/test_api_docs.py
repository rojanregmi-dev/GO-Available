from django.test import TestCase
from rest_framework.test import APIClient


class ApiDocsTests(TestCase):
    def test_schema_endpoint_returns_openapi_schema(self):
        client = APIClient()

        response = client.get("/api/schema/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["info"]["title"], "GO Available Account Service API"
        )
        self.assertEqual(
            response.data["components"]["securitySchemes"]["bearerAuth"]["scheme"],
            "bearer",
        )
        self.assertEqual(
            response.data["paths"]["/api/v1/account"]["post"]["security"],
            [{"bearerAuth": []}],
        )
        self.assertNotIn("security", response.data["paths"]["/api/v1/health"]["get"])

    def test_docs_endpoint_returns_swagger_ui(self):
        client = APIClient()

        response = client.get("/api/docs/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "swagger-ui")
