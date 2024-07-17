import configparser
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
from sklearn.preprocessing import MinMaxScaler
import os
import sys

# `data_fetching` modülünü import edebilmek için sys.path'e dizin ekleme
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data_fetching'))
from data_fetching import fetch_data, load_api_keys, initialize_binance

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '..', 'Trade
