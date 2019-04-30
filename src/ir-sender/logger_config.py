# from: https://www.nakamuri.info/mw/index.php/Python%E3%81%A7%E7%B0%A1%E5%8D%98%E3%81%AB%E3%83%AD%E3%82%AE%E3%83%B3%E3%82%B0%E3%82%92%E8%A1%8C%E3%81%86%E3%81%AB%E3%81%AF

import sys
from logging import DEBUG, INFO
from logging import Formatter, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler

# ルートロガーの作成。ログレベル=デバッグ
_root_logger = getLogger('')
_root_logger.setLevel(DEBUG)

# フォーマッターの作成(時刻、ログレベル、モジュール名、関数名、行番号: メッセージ　を出力)
_simpleFormatter = Formatter(
    fmt='%(asctime)s %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s'
)

# コンソール用ハンドラの作成。標準出力へ出力。ログレベル=デバッグ。書式は上記フォーマッター
_consoleHandler = StreamHandler(sys.stdout)
_consoleHandler.setLevel(DEBUG)
_consoleHandler.setFormatter(_simpleFormatter)

# コンソール用ハンドラをルートロガーに追加
_root_logger.addHandler(_consoleHandler)

# ファイル用ハンドラの作成。ファイル名は log/ir-sender.log, ログレベル=INFO, ファイルサイズ 1MB, バックアップファイル３個まで、エンコーディングは utf-8
_fileHandler = RotatingFileHandler(
    filename='log/ir-sender.log', maxBytes=1000000, backupCount=3, encoding='utf-8'
)
_fileHandler.setLevel(INFO)
_fileHandler.setFormatter(_simpleFormatter)

# ファイル用ハンドラをルートロガーに追加
_root_logger.addHandler(_fileHandler)