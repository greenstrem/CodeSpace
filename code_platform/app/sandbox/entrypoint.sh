#!/bin/sh
# Ограничение времени выполнения (например, 5 секунд)
timeout 5 python3 code_executor.py "$@"
