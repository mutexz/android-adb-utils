#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import subprocess
import weakref

from _utils import adb_path
from errors import AdbError, AdbTimeoutError


def _check_server(host: str, port: int) -> bool:
    # return if server is running
    s = socket.socket()
    try:
        s.connect((host, port))
        return True
    except socket.error as e:
        return False
    finally:
        s.close()


class AdbConnection(object):

    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port
        self.__conn = self._safe_connect()
        self._finalizer = weakref.finalize(self, self.conn.close)

    @property
    def conn(self) -> socket.socket:
        return self.__conn

    def _create_socket(self) -> socket.socket:
        adb_host = self.__host
        adb_port = self.__port
        s = socket.socket()
        try:
            s.connect((adb_host, adb_port))
            return s
        except socket.error as e:
            s.close()
            raise

    def _safe_connect(self):
        try:
            return self._create_socket()
        except ConnectionRefusedError:
            # 对于还未启动adb进程的话，需要启动adb server进程, 这样才可以连接
            subprocess.run([adb_path(), "start-server"], timeout=20.0)
            return self._create_socket()

    @property
    def closed(self) -> bool:
        return not self._finalizer.alive

    def close(self):
        # 调用_finalizer的回调函数，也即close方法
        self._finalizer()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def send(self, data: bytes) -> int:
        return self.conn.send(data)

    def _read_fully(self, n: int) -> bytes:
        t = n
        buffer = b''
        while t > 0:
            chunk = self.conn.recv(t)
            if not chunk:
                break
            buffer += chunk
            t = n - len(buffer)
        return buffer

    def read(self, n: int) -> bytes:
        try:
            return self._read_fully(n)
        except socket.timeout:
            raise AdbTimeoutError("adb read timeout")
