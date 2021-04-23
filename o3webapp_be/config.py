# config
import os

# EGI CheckIn OIDC instance
EGI_URL = os.getenv('EGI_URL', 'https://aai-dev.egi.eu/oidc/')
# O3webapp Frontend
O3WEB_URL = os.getenv('O3WEB_URL', 'http://o3web.test.fedcloud.eu/')
# O3API instance
O3API_URL = os.getenv('O3API_URL', 'http://o3api.test.fedcloud.eu:30505/api/')
O3API_INFO = 'api-info'
O3API_DATA = 'data'
O3API_MODELS_LIST = 'models/list'