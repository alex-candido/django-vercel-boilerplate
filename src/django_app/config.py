from pathlib import Path
from typing import Dict
from pydantic_settings import BaseSettings
from pydantic import validator, Field
from datetime import timedelta

import os
import dj_database_url

_ENV_FOLDER = Path(__file__).resolve().parent.parent.parent / 'envs'
APP_ENV = os.getenv('APP_ENV')

class ConfigService(BaseSettings):
    database_dsn: str
    database_conn: Dict = Field(init=False, default=None)
    debug: bool = False
    language_code: str = 'en-us'
    secret_key: str
    allowed_hosts: list[str] = Field(default_factory=list)
    installed_apps: list[str] = Field(default_factory=list)
    middlewares_additional: list[str] = Field(default_factory=list)
    simple_jwt: Dict = Field(default_factory=dict)
    rest_framework: Dict = Field(default_factory=dict)
    
    class Config:
        env_file = f'{_ENV_FOLDER}/.env', f'{_ENV_FOLDER}/.env.{APP_ENV}'
        
        @classmethod
        def parse_env_var(cls, _field_name, raw_value: str):
            return cls.json_loads(raw_value)
    
    @validator('database_conn', pre=True, allow_reuse=True)
    def make_database_conn(cls, _v, values, **kwargs):
        return dj_database_url.config(default=values['database_dsn'])
    
    @validator('simple_jwt', pre=True)
    def parse_simple_jwt(cls, v):
        if isinstance(v, dict):
            if 'ACCESS_TOKEN_LIFETIME' in v:
                v['ACCESS_TOKEN_LIFETIME'] = eval(v['ACCESS_TOKEN_LIFETIME'])
            if 'REFRESH_TOKEN_LIFETIME' in v:
                v['REFRESH_TOKEN_LIFETIME'] = eval(v['REFRESH_TOKEN_LIFETIME'])
        return v
        
config_service = ConfigService()