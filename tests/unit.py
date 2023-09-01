import unittest
import sys
import os
from datetime import datetime
import requests
from unittest.mock import patch, MagicMock

# Adiciona o diretório 'src' ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import cdi
