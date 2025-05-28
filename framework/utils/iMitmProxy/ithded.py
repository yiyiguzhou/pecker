# -*- coding: UTF-8 -*-

"""
File Name:      threads
Author:         zhangwei04
Create Date:    2018/1/12
"""
import os
import time
import threading
import subprocess


class IpeckerPopen(subprocess.Popen):
    """
    阻塞性线程
    """
    __coding_style = "utf-8"

    def __init__(self, args, timeout=None, shell=False, except_flag=False,
                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                 encoding=None, errors=None, bufsize=-1):
        self.__cmd = args
        self.__timeout = timeout
        self.__except_flag = except_flag
        super(IpeckerPopen, self).__init__(args, shell=shell, stdin=stdin, stdout=stdout,
                                           stderr=stderr, encoding=encoding, errors=errors, bufsize=bufsize)

    def execute(self, input=None, timeout=None):
        """
        开始线程
        Args:
            input: 交互式命令
            timeout: 超时
        Returns:
            线程执行后的输出信息
        """
        if not timeout:
            timeout = self.__timeout
        try:
            outs, errs = self.communicate(input=input, timeout=timeout)
        except subprocess.TimeoutExpired:
            self.kill()
            outs, errs = self.communicate()
            if self.__except_flag:
                raise Exception(self.__cmd, self.__timeout)
        try:
            outs = outs.decode(IpeckerPopen.__coding_style).strip() if outs else None
            errs = errs.decode(IpeckerPopen.__coding_style).strip() if errs else None
        except:
            outs = outs.decode('utf-8').strip() if outs else None
            errs = errs.decode('utf-8').strip() if errs else None
        return outs, errs


class IpeckerThread(object):
    """非阻塞性线程程处理类"""
    def __init__(self, cmd, std_flag=False, log_file=None, time_interval=0.1, repeat_flag=False, shell=False):
        self._log_file = None
        self._run_flag = True
        self._cmd = cmd
        self._std_flg = std_flag
        self._time_interval = time_interval
        self._shell = shell
        self.thread = None
        self._proc = None

        if log_file:
            self._log_file = os.path.abspath(log_file)
            log_file_dir = os.path.dirname(self._log_file)
            if not os.path.exists(log_file_dir):
                os.makedirs(log_file_dir)

    def start(self, func=None, *args, **kwargs):
        """
        启动线程
        """
        if func:
            self.thread = threading.Thread(target=self._run_func(func, *args, **kwargs))
        else:
            self.thread = threading.Thread(target=self._run, args=())
            self.thread.start()

    def stop(self):
        """
        停止线程
        """
        if self._run_flag:
            self._run_flag = False

    def communicate(self, input, timeout=None):
        """
        线程交互
        Args:
            input:输入参数
            timeout: 超时
        """
        if self._proc:
            self._proc.communicate(input, timeout)

    def send_signal(self, sig):
        if self._proc:
            self._proc.send_signal(sig)

    @property
    def is_start(self):
        """线程是否被启动"""
        return True if self.thread else False

    @property
    def is_stop(self):
        """线程是否停止"""
        return True if self._run_flag else False

    def _run(self):
        """运行线程"""
        if self._log_file:
            stdout = open(self._log_file, "w+", encoding='utf-8')
            stderr = stdout
        elif self._std_flg:
            stdout = subprocess.PIPE
            stderr = subprocess.PIPE
        else:
            stdout = None
            stderr = None

        self._run_flag = True
        with IpeckerPopen(self._cmd, stdout=stdout, stderr=stderr, shell=self._shell) as proc:
            self._proc = proc
            while True:
                if self._run_flag:
                    time.sleep(self._time_interval)
                else:
                    proc.terminate()
                    proc.wait()
                    break
        if self._log_file:
            stdout.close()

    def _run_func(self, func, *args, **kwargs):
        func(*args, **kwargs)


class IpeckerRepeatThread(IpeckerThread):
    """命令重复执行线程"""
    def __init__(self, cmd=None, std_flag=False, log_file=None, time_interval=0.1, shell=False):
        super(IpeckerRepeatThread, self).__init__(cmd, std_flag=std_flag, log_file=log_file, time_interval=time_interval,shell=shell)

    def start(self, func=None, *args, **kwargs):
        """
        启动线程
        """
        if func:
            self.thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        else:
            self.thread = threading.Thread(target=self._run, args=())
        self.thread.start()

    def _run(self):
        """运行线程"""
        if self._log_file:
            stdout = open(self._log_file, "w+")
            stderr = stdout
        elif self._std_flg:
            stdout = subprocess.PIPE
            stderr = subprocess.PIPE
        else:
            stdout = None
            stderr = None

        self._run_flag = True
        while self._run_flag:
            stdout.writelines(self.get_time_stamp())
            stdout.flush()
            with IpeckerPopen(self._cmd, stdout=stdout, stderr=stderr, shell=self._shell) as proc:
                self._proc = proc
                proc.execute()
                time.sleep(self._time_interval)
                proc.terminate()
                proc.wait()

        if self._log_file:
            stdout.close()

    def _run_func(self, func, *args, **kwargs):
        """重复执行函数"""
        self._run_flag = True
        while self._run_flag:
            func(*args, **kwargs)

    @classmethod
    def get_time_stamp(cls):
        """获取本地时间函数
        Returns：
            格式化的时间，如：06-12 21:49:02.291
        """
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d " % (data_head, data_secs)
        return time_stamp


if __name__ == "__main__":
    i = IpeckerPopen("tasklist | findstr node", timeout=20, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    with IpeckerPopen("ping 127.0.0.1", shell=True, except_flag=True, timeout=30) as p:
        pass
        print(p.execute())
