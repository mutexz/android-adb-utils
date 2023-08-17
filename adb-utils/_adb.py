#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import subprocess
import weakref


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
            # 对于还未启动adb进程的话，需要启动进程
            subprocess.run([adb_path(), "start-server"], timeout=20.0)
            return self._create_socket()
