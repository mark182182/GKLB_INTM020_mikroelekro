import os


def read_env_var(key: str) -> str:
  value = os.getenv(key)
  if value is not None:
    return value
  else:
    raise ValueError(f'{key} is not defined in the environment.')
