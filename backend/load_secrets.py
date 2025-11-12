"""
Load secrets from Docker secrets files or environment variables.

This module provides a unified way to load secrets from either:
1. Docker secrets (mounted files in /run/secrets/)
2. Environment variables (fallback for local development)
"""

import os
from pathlib import Path


def load_secret(secret_name: str, env_var_name: str = None) -> str:
    """
    Load a secret from Docker secrets file or environment variable.

    Args:
        secret_name: Name of the secret file (e.g., 'openai_api_key')
        env_var_name: Environment variable name to use as fallback

    Returns:
        Secret value as string

    Raises:
        ValueError: If secret cannot be loaded from either source
    """
    # Try Docker secret first (production/secure mode)
    secret_path = Path(f"/run/secrets/{secret_name}")
    if secret_path.exists():
        try:
            with open(secret_path, 'r') as f:
                secret_value = f.read().strip()
                if secret_value:
                    return secret_value
        except Exception as e:
            print(f"Warning: Could not read secret from {secret_path}: {e}")

    # Fall back to environment variable (local development)
    if env_var_name:
        env_value = os.getenv(env_var_name)
        if env_value:
            return env_value

    # No secret found
    raise ValueError(
        f"Secret '{secret_name}' not found in /run/secrets/ "
        f"and environment variable '{env_var_name}' is not set"
    )


def get_openai_api_key() -> str:
    """Get OpenAI API key from secrets or environment."""
    return load_secret("openai_api_key", "OPENAI_API_KEY")


def get_postgres_password() -> str:
    """Get Postgres password from secrets or environment."""
    return load_secret("postgres_password", "POSTGRES_PASSWORD")
