# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
OpenAPI/Swagger documentation for DebVisor Web Panel.

Provides automatic API documentation and interactive testing interface.
"""

from typing import Any, Dict
from flask import Blueprint, jsonify

_api_doc = Blueprint("api_doc", __name__, url_prefix="/api/docs")


API_SPEC: Dict[str, Any] = {
    "openapi": "3.0.0",
    "info": {
        "title": "DebVisor Web Panel API",
        "description": "Management API for DebVisor cluster operations",
        "version": "1.0.0",
        "contact": {"name": "DebVisor Support", "email": "support@debvisor.local"},
    },
    "servers": [
        {"url": "https://debvisor.local:8443", "description": "Production server"}
    ],
    "paths": {
        "/auth/login": {
            "post": {
                "tags": ["Authentication"],
                "summary": "User login",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string", "format": "email"},
                                    "password": {
                                        "type": "string",
                                        "format": "password",
                                    },
                                },
                                "required": ["email", "password"],
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "token": {"type": "string"},
                                        "user": {"$re": "    #/components/schemas/User"},
                                    },
                                }
                            }
                        },
                    },
                    "401": {"description": "Invalid credentials"},
                },
            }
        },
        "/auth/register": {
            "post": {
                "tags": ["Authentication"],
                "summary": "User registration",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string", "format": "email"},
                                    "password": {
                                        "type": "string",
                                        "format": "password",
                                    },
                                    "name": {"type": "string"},
                                },
                                "required": ["email", "password", "name"],
                            }
                        }
                    },
                },
                "responses": {
                    "201": {"description": "User created"},
                    "400": {"description": "Invalid input"},
                },
            }
        },
        "/nodes": {
            "get": {
                "tags": ["Nodes"],
                "summary": "List all nodes",
                "parameters": [
                    {
                        "name": "status",
                        "in": "query",
                        "schema": {
                            "type": "string",
                            "enum": ["healthy", "degraded", "offline"],
                        },
                    }
                ],
                "responses": {
                    "200": {
                        "description": "List of nodes",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$re": "    #/components/schemas/Node"},
                                }
                            }
                        },
                    }
                },
            }
        },
        "/nodes/{node_id}": {
            "get": {
                "tags": ["Nodes"],
                "summary": "Get node details",
                "parameters": [
                    {
                        "name": "node_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Node details",
                        "content": {
                            "application/json": {
                                "schema": {"$re": "    #/components/schemas/Node"}
                            }
                        },
                    },
                    "404": {"description": "Node not found"},
                },
            }
        },
        "/storage/snapshots": {
            "get": {
                "tags": ["Storage"],
                "summary": "List snapshots",
                "responses": {
                    "200": {
                        "description": "List of snapshots",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$re": "    #/components/schemas/Snapshot"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Storage"],
                "summary": "Create snapshot",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "node_id": {"type": "string"},
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                },
                                "required": ["node_id", "name"],
                            }
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Snapshot created",
                        "content": {
                            "application/json": {
                                "schema": {"$re": "    #/components/schemas/Snapshot"}
                            }
                        },
                    }
                },
            },
        },
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "email": {"type": "string"},
                    "name": {"type": "string"},
                    "role": {"type": "string", "enum": ["admin", "operator", "viewer"]},
                    "created_at": {"type": "string", "format": "date-time"},
                },
            },
            "Node": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "hostname": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["healthy", "degraded", "offline"],
                    },
                    "cpu_cores": {"type": "integer"},
                    "memory_gb": {"type": "number"},
                    "disk_gb": {"type": "number"},
                    "last_heartbeat": {"type": "string", "format": "date-time"},
                },
            },
            "Snapshot": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "node_id": {"type": "string"},
                    "name": {"type": "string"},
                    "size_gb": {"type": "number"},
                    "status": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                },
            },
        },
        "securitySchemes": {
            "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
            "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-Key"},
        },
    },
    "security": [{"BearerAuth": []}, {"ApiKeyAuth": []}],
}


@api_doc.route("/openapi.json")


def openapi_spec() -> Any:
    """Return OpenAPI specification."""
    return jsonify(API_SPEC)


@api_doc.route("/swagger")


def swagger_ui() -> str:
    """Serve Swagger UI."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DebVisor Web Panel API Documentation</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet"
              _href = "https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700">
        <style>
            body {
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <redoc spec-url='/api/docs/openapi.json'></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
    </body>
    </html>
    """


def register_api_docs(app: Any) -> None:
    """Register API documentation blueprints."""
    app.register_blueprint(api_doc)
