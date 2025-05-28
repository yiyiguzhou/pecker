# -*- coding: UTF-8 -*-

"""
File Name:      base_api
Author:         zhangwei04
Create Date:    2019/7/9
"""
import time
from contextlib import contextmanager
from framework.exception.exception import ParamaterError
from framework.logger.logger import g_logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.keys import Keys


from .action_chains import IActionChains
from framework.utils.func import timeout_decorate

DIRECTIONS = {"up", "down", "left", "right"}


class BaseApi(object):
    """selenium基础接口类"""
    def __init__(self):
        self.driver = webdriver.Chrome()
        self._action = None
        self.keys = Keys

    @property
    def action(self):
        self._action = IActionChains(self.driver)
        return self._action

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def title(self):
        return self.driver.title

    @property
    def window_handles(self):
        return self.driver.window_handles

    @property
    def switch_to(self):
        return self.driver.switch_to

    @property
    def current_window_handle(self):
        return self.driver.current_window_handle

    def get_cookie(self, name):
        self.driver.get_cookie(name)

    def get_cookies(self):
        self.driver.get_cookies()

    def switch_to_window(self, window):
        """
        切换窗口
        Args:
            window: 窗口句柄，通过此类的current_window_handle属性获取
        Returns:
        """
        self.driver.switch_to.window(window)
        return True

    def switch_to_last_window(self):
        """
        切换到最后一个window
        Returns:
            True
        """
        current_win_handle = self.current_window_handle
        if self.current_window_handle == self.window_handles[-1]:
            return
        self.driver.switch_to.window(self.window_handles[-1])

    @contextmanager
    def switch_frame(self, frame):
        """切换frame上下文管理器"""
        self.driver.switch_to.frame(frame)
        yield
        self.driver.switch_to.default_content()  # 切回主文档

    @timeout_decorate(dec_timeout=30, ignore_exception=True)
    def get(self, url, time_sleep=1):
        """
        打开url
        Args:
            url: url路径
            time_sleep: 睡眠时间
        """
        try:
            self.driver.get(url=url)
            time.sleep(time_sleep)
        except:
            self.switch_to.window(self.window_handles[-1])
            self.driver.get(url=url)
        return True

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_elements(self, by=By.ID, value=None, switch_last_window=True):
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_elements(by, value)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def execute_script(self, script, switch_last_window=True, timeout=None, *args):
        """
        脚本方式执行接口
        Args:
            script: 脚本名（接口名）
            *args: 命令参数（字典方式）
            timeout: 命令执行超时，单位: 秒
        Returns:
            执行结果
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.execute_script(script, *args)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_element_by_id(self, id, switch_last_window=True, timeout=None):
        """
        通过id查找元素
        Args:
            id: 元素id属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_element_by_id(id)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_elements_by_id(self, id, switch_last_window=True, timeout=None):
        """
        通过id查找元素集合
        Args:
            id: 元素id属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_elements_by_id(id)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_element_by_xpath(self, xpath, switch_last_window=True, timeout=None):
        """
        通过xpath查找元素
        Args:
            xpath: xpath 路径
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_element_by_xpath(xpath)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_elements_by_xpath(self, xpath, switch_last_window=True, timeout=None):
        """
        通过xpath查找元素集合
        Args:
            xpath: xpath 路径
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_elements_by_xpath(xpath)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_element_by_css_selector(self, css_selector, switch_last_window=True, timeout=None):
        """
        通过css选择器查找元素
        Args:
            css_selector: css selector 路径
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        Usage:
            elements = element.find_elements_by_css_selector(‘.foo’)
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_element_by_css_selector(css_selector)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_elements_by_css_selector(self, css_selector, switch_last_window=True, timeout=None):
        """
        通过css选择器查找元素集合
        Args:
            css_selector: css selector 路径
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        Usage:
            elements = element.find_elements_by_css_selector(‘.foo’)
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_elements_by_css_selector(css_selector)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_element_by_partial_link_text(self, link_text, switch_last_window=True, timeout=None):
        """
        通过部分可见链接文本查找元素
        Args:
            link_text: 超链接部分文本
            timeout: 命令执行超时，单位: 秒
        Returns:
            超链接元素实例，执行点击会跳转超链接
        Usage:
            elements = element.find_elements_by_css_selector(‘.foo’)
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_element_by_partial_link_text(link_text)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_elements_by_partial_link_text(self, link_text, switch_last_window=True, timeout=None):
        """
        通过部分可见超链接文本查找元素集合
        Args:
            link_text: 超链接部分文本
            timeout: 命令执行超时，单位: 秒
        Returns:
            超链接元素实例列表，执行点击会跳转超链接
        Usage:
            elements = element.find_elements_by_css_selector(‘.foo’)
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_elements_by_partial_link_text(link_text)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_element_by_link_text(self, text, switch_last_window=True, timeout=None):
        """
        通过部分可见链接文本查找元素
        Args:
            text: 超链接文本
            timeout: 命令执行超时，单位: 秒
        Returns:
            超链接元素实例，执行点击会跳转超链接
        Usage:
            elements = driver.find_element_by_link_text(‘Sign In’)
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_element_by_link_text(text)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_elements_by_link_text(self, text, switch_last_window=True, timeout=None):
        """
        通过部分可见超链接文本查找元素集合
        Args:
            text: 超链接文本
            timeout: 命令执行超时，单位: 秒
        Returns:
            超链接元素实例列表，执行点击会跳转超链接
        Usage:
            elements = driver.find_elements_by_link_text(‘Sign In’)
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_elements_by_link_text(text)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_element_by_tag_name(self, name, switch_last_window=True, timeout=None):
        """
        通过tag name查找元素
        Args:
            name: tag名
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        Usage:
            elements = element.find_element_by_tag_name("div")
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_element_by_tag_name(name)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_elements_by_tag_name(self, name, switch_last_window=True, timeout=None):
        """
        通过tag name查找元素集合
        Args:
            name: tag名
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例集合
        Usage:
            elements = element.find_elements_by_tag_name("div")
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_elements_by_tag_name(name)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_element_by_name(self, name, switch_last_window=True, timeout=None):
        """
        通过元素name属性查找元素
        Args:
            name: 元素name属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_element_by_name(name)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_elements_by_name(self, name, switch_last_window=True, timeout=None):
        """
        通过元素name属性查找元素集合
        Args:
            name: 元素name属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_elements_by_name(name)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_element_by_class_name(self, name, switch_last_window=True, timeout=None):
        """
        通过元素class属性查找元素
        Args:
            name: 元素class属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_element_by_class_name(name)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_elements_by_class_name(self, name, switch_last_window=True, timeout=None):
        """
        通过元素class属性查找元素集合
        Args:
            name: 元素class属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_elements_by_class_name(name)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def find_element(self, by=By.ID, value=None, switch_last_window=True, timeout=None):
        """
        查找元素
        Args:
            by: 查找方式（By.ID, By.TAG_NAME, By.CLASS_NAME...）
            value:属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        if switch_last_window:
            self.switch_to_last_window()
        return self.driver.find_element(by, value)

    def reset_mouse_position(self):
        """
        重置鼠标位置，将鼠标位置置为(0,0)
        """
        body_ele = self.driver.find_element_by_tag_name('body')
        with self.action as action:
            action.move_to_element(body_ele)
            action.move_by_offset(-body_ele.size['width'] / 2 + 1, -body_ele.size['height'] / 2 + 1)

    def forward(self):
        """定向到浏览历史记录往后一个，即浏览器上方向右箭头"""
        self.driver.forward()

    def back(self):
        """定向到浏览历史记录往前一个，即浏览器上方向左箭头"""
        self.driver.back()

    def close(self):
        """关闭当前窗口"""
        ws = self.window_handles
        self.driver.close()
        self.driver.switch_to.window(self.window_handles[-1])

    def close_last_window(self):
        """关闭最后一个窗口"""
        if len(self.window_handles) == 1:   # 只有一个窗口，不关闭
            return True
        else:
            self.switch_to.window(self.window_handles[-1])
            self.close()
            self.switch_to.window(self.window_handles[-1])
            return True

    def leave_one_window(self):
        """
        只剩下一个窗口
        Returns:
            True
        """
        while len(self.window_handles) != 1:
            self.close_last_window()
        return True

    def quit(self):
        """关闭所有窗口"""
        self.driver.quit()

    def fullscreen_window(self):
        """当前窗口全屏"""
        self.driver.fullscreen_window()

    def maximize_window(self):
        """当前窗口最大化"""
        self.driver.maximize_window()

    def minimize_window(self):
        """当前窗口最小化"""
        self.driver.minimize_window()

    def refresh(self):
        """刷新当前页面"""
        self.driver.refresh()

    def tap(self, position,  time_sleep=1, timeout=None):
        """
        按坐标点击操作
        Args:
            position: 坐标元素点(x,y)
            time_sleep: 点击后睡眠时间
            timeout: 命令执行超时，单位: 秒
        """
        if isinstance(position, dict):
            position = (position['x'], position['y'])

        # 先移动到body元素，将鼠标定位至(0,0)像素点
        self.reset_mouse_position()

        with self.action as action:
            action.move_by_offset(position[0], position[1])     # 移动至点击位置
            action.click()
        time.sleep(time_sleep)
        return True

    def tap_ele_by_position(self, ele, time_sleep=1):
        """
        点击元素位置坐标
        Args:
            ele: 元素实例
            time_sleep: 点击后等待时间
        Returns:
            True: 点击成功, False: 点击失败
        """
        location = ele.location
        size = ele.size
        pos = (int(location['x'] + size['width'] / 2), int(location['y'] + size['height'] / 2))
        self.tap(pos)
        time.sleep(time_sleep)
        return True

    @timeout_decorate(dec_timeout=2, ignore_exception=True)
    def click_from_position(self, x_rate, y_rate, sleep_time=2):
        """通过坐标点击
        Args:
            x_rate: 若x_rate大于1，则表示绝对坐标点，否者为位置比例
            y_rate: 若y_rate大于1，则表示绝对坐标点，否者为位置比例
            duration: 按下持续时间 单位: 毫秒
            sleep_time: 点击后睡眠时间 单位: 秒
        """
        if x_rate > 1 and y_rate > 1:
            pos = (x_rate, y_rate)
        else:
            size = self.get_window_size()
            width = size.get('width')
            height = size.get('height')
            pos = (int(x_rate if x_rate > 1 else width * x_rate), int(y_rate if y_rate > 1 else height * y_rate))

        self.tap(pos)
        time.sleep(sleep_time)

    # def swipe(self, start_x, start_y, end_x, end_y, duration=None, timeout=None):
    #     """
    #     滑动操作
    #     Args:
    #         start_x: 起始x轴像素位置
    #         start_y: 起始y轴像素位置
    #         end_x: 结束x轴像素位置
    #         end_y: 结束y轴像素位置
    #         duration: 滑动时长, 单位秒
    #         timeout: 命令执行超时，单位: 秒
    #     """
    #     self._reset_mouse_position()
    #     with self.action as action:
    #         action.move_by_offset(start_x, start_y)
    #         action.click_and_hold()
    #         action.move_by_offset(end_x, end_y)
    #         action.release()

    # 截图
    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def get_screenshot_as_file(self, filename, timeout=None):
        """
        获取屏幕截图
        Args:
            filename: 存储文件名,要求png格式的.如："./screenshot.png"
            timeout: 命令执行超时，单位: 秒
        Returns:
            True: 截图成功，False: 截图失败
        """
        return self.driver.get_screenshot_as_file(filename)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def get_window_size(self, window_handle='current', timeout=None):
        """
        获取窗口尺寸
        Args:
            window_handle:窗口
            timeout: 命令执行超时，单位: 秒
        Returns:
            宽和高的字典, eg: {'width':768, 'height':1024}
        """
        return self.driver.get_window_size(window_handle)

    def get_window_height(self):
        """
        获取当前窗口纵坐向分辨率
        Returns:
            当前窗口纵坐向分辨率
        """
        return self.get_window_size().get("height", None)

    def get_window_width(self):
        """
        获取当前窗口横坐向分辨率
        Returns:
            当前窗口横坐向分辨率
        """
        return self.get_window_size().get("width", None)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def set_window_size(self, width, height, window_handle='current', timeout=None):
        """
        设置window尺寸
        Args:
            width: 宽
            height: 高
            window_handle:窗口句柄
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.set_window_size(width, height, window_handle)

    @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def get_window_position(self, window_handle='current', timeout=None):
        """
        获取窗口位置,左上方的坐标点
        Args:
            window_handle: 窗口句柄
            timeout: 命令执行超时，单位: 秒
        Returns:
            窗口位置
        """
        return self.driver.get_window_position(window_handle)

    def scroll_windows(self, offset_x, offset_y):
        """
        滑动Window窗口
        Args:
            offset_x: x坐标滑动偏移, 正数向右，负数向左
            offset_y: y坐标滑动偏移， 正数向下，负数向上
        Returns:
            执行结果
        """
        return self.driver.execute_script("window.scrollBy({}, {});".format(int(offset_x), int(offset_y)))

    def scroll_element(self, ele, offset_x, offset_y):
        """
        滑动元素
        Args:
            ele: 滑动元素
            offset_x: x坐标滑动偏移, 正数向右，负数向左
            offset_y: y坐标滑动偏移， 正数向下，负数向上
        Returns:
            执行结果
        """
        return self.driver.execute_script("arguments[0].scrollBy({}, {});".format(int(offset_x), int(offset_y)), ele)

    def drag_and_drop(self, origin_el, destination_el):
        """
        拖一个元素到另外一个元素上
        Args:
            origin_el: 源元素实例
            destination_el:  目标元素
        """
        with self.action as action:
            action.drag_and_drop(origin_el, destination_el)
        return True

    def long_press(self, ele, seconds=1):
        """
        元素长按事件
        Args:
            ele: 事件码
            seconds: 按压时间
        """
        with self.action as action:
            action.click_and_hold(ele)
            action.pause(seconds)
            action.reset_actions(ele)
        return True

    def move_to_element(self, ele):
        """
        光标移动到元素上
        Args:
            ele: 元素对象
        Returns:
            True
        """
        with self.action as action:
            action.move_to_element(ele)
        time.sleep(0.5)
        return True

    def click_by_id(self, id, timeout=5, time_sleep=1, *args, **kwargs):
        """
       通过id查找元素, 并点击
       Args:
           id: 元素id属性值
           timeout: 命令执行超时，单位: 秒
       Returns:
           True: 元素找到，并执行点击动作
           False: 元素没有找到
       """
        return self.click_by_ele(By.ID, id, timeout=timeout, time_sleep=time_sleep, *args, **kwargs)

    def click_by_xpath(self, xpath, timeout=5, time_sleep=1, *args, **kwargs):
        """
        通过xpath查找元素， 并点击
        Args:
            xpath: xpath 路径
            timeout: 命令执行超时，单位: 秒
        Returns:
            True: 元素找到，并执行点击动作
            False: 元素没有找到
        """
        return self.click_by_ele(By.XPATH, xpath, timeout=timeout, time_sleep=time_sleep, *args, **kwargs)

    def click_by_class(self, class_name, timeout=5, time_sleep=1, *args, **kwargs):
        """
        通过class查找元素， 并点击
        Args:
            class_name: class名
            timeout: 命令执行超时，单位: 秒
        Returns:
            True: 元素找到，并执行点击动作
            False: 元素没有找到
        """
        return self.click_by_ele(By.CLASS_NAME, class_name, timeout=timeout, time_sleep=time_sleep, *args, **kwargs)

    def click_by_partial_link_text(self, partial_link_text, timeout=5, time_sleep=1, *args, **kwargs):
        """
        通过class查找元素， 并点击
        Args:
            partial_link_text: partial_link_text文本
            timeout: 命令执行超时，单位: 秒
        Returns:
            True: 元素找到，并执行点击动作
            False: 元素没有找到
        """
        return self.click_by_ele(By.PARTIAL_LINK_TEXT, partial_link_text, timeout=timeout, time_sleep=time_sleep, *args, **kwargs)

    def click_by_link_text(self, link_text, timeout=5, time_sleep=1, *args, **kwargs):
        """
        通过link_text查找元素， 并点击
        Args:
            link_text: 链接文本名
            timeout: 命令执行超时，单位: 秒
        Returns:
            True: 元素找到，并执行点击动作
            False: 元素没有找到
        """
        return self.click_by_ele(By.LINK_TEXT, link_text, timeout=timeout, time_sleep=time_sleep, *args, **kwargs)

    def click_by_ele(self,  by, by_value, timeout=5, time_sleep=1, *args, **kwargs):
        """
        点击元素
        Args:
            by: 查找类型,参见selenium.webdriver.common.by.By类
            by_value: 查找表达式
            timeout: 查找超时
            time_sleep: 点击元素后，等待时间
        Returns:
            True: 点击成功, False: 点击失败
        """
        desc = kwargs.get("desc", "")
        if desc:
            try:
                g_logger.info("点击{}...".format(desc))
                self.find_element(by, by_value, timeout=timeout).click()
                g_logger.info("点击{} 结束".format(desc))
            except Exception as e:
                return g_logger.error("点击{} 超时".format(desc))

        else:
            try:
                self.find_element(by, by_value, timeout=timeout).click()
            except Exception as e:
                return False

        time.sleep(time_sleep)
        return True

    def swipe_find_ele_by_xpath(self, xpath, direct="up", rate=0.4, timeout=30):
        """
        滑动手机，并通过xpath路径查找元素
        Args:
            xpath: xpath 路径
            direct: 滑动方向
            rate: 滑动幅度，屏幕占比，默认0.5
            timeout: 超时
        Returns:
            元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        direct = direct.lower()
        if direct not in DIRECTIONS:
            raise ValueError("params: {} not in {}".format(direct, DIRECTIONS))
        func = self.__getattribute__("{}_swipe_find_ele_by_xpath".format(direct))
        return func(xpath, rate=abs(rate), timeout=timeout)

    def up_swipe_find_ele_by_xpath(self, xpath, rate=0.5, timeout=30):
        """
        向上滑动手机，并通过xpath路径查找元素
        Args:
            xpath: xpath 路径
            rate: 滑动幅度，屏幕占比，默认0.5
            timeout: 超时
        Returns:
            元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        return self.swipe_timeout_find_ele_by_xpath(xpath, x_rate=0, y_rate=-rate, timeout=timeout)

    def down_swipe_find_ele_by_xpath(self, xpath, rate=0.5, timeout=30):
        """
        向下滑动手机，并通过xpath路径查找元素
        Args:
           xpath: xpath 路径
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        return self.swipe_timeout_find_ele_by_xpath(xpath, x_rate=0, y_rate=rate, timeout=timeout)

    # @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def left_swipe_find_ele_by_xpath(self, xpath, rate=0.4, timeout=30):
        """
        向左滑动手机，并通过xpath路径查找元素
        Args:
           xpath: xpath 路径
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        return self.swipe_timeout_find_ele_by_xpath(xpath, x_rate=-rate, y_rate=0, timeout=timeout)

    # @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def right_swipe_find_ele_by_xpath(self, xpath, rate=0.5, timeout=30):
        """
        向右滑动手机，并通过xpath路径查找元素
        Args:
           xpath: xpath 路径
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        return self.swipe_timeout_find_ele_by_xpath(xpath, x_rate=rate, y_rate=0, timeout=timeout)

    def swipe_timeout_find_ele_by_xpath(self, xpath, x_rate=0.0, y_rate=0.0, timeout=30):
        """
        滑动手机，并通过xpath路径查找元素超时函数
        Args:
           xpath: xpath 路径
           x_start: x轴起始位置
           x_end: x轴结束位置
           y_start: y轴结束位置
           y_end: y轴结束位置
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        x_offset = int(self.get_window_width()) * x_rate
        y_offset = int(self.get_window_width()) * y_rate
        time_start = time.time()
        while time.time() - time_start < timeout:
            try:
                ele = self.find_element_by_xpath(xpath, timeout=2)
                return ele
            except:
                try:
                    self.scroll_windows(x_offset, y_offset)
                except:
                    g_logger.info("swipe_timeout_find_ele_by_xpath滑动屏幕超时")
                    return None
                time.sleep(2)
        return None

    # @timeout_decorate(dec_timeout=5, ignore_exception=True)
    def swipe_find_ele_by_id(self, eid, direct="down", rate=0.5, timeout=30):
        """
        滑动手机，并通过元素id查找元素
        Args:
            eid: id 路径
            direct: 滑动方向
            rate: 滑动幅度，屏幕占比，默认0.5
            timeout: 超时
        Returns:
            元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        direct = direct.lower()
        if direct not in DIRECTIONS:
            raise ValueError("params: {} not in {}".format(direct, DIRECTIONS))
        func = self.__getattribute__("{}_swipe_find_ele_by_id".format(direct))
        return func(eid, rate=abs(rate), timeout=timeout)

    def up_swipe_find_ele_by_id(self, eid, rate=0.3, timeout=30):
        """
        向下滑动元素，并通过元素id查找元素
        Args:
           eid: 元素id
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        return self.swipe_timeout_find_ele_by_id(eid, x_rate=0, y_rate=-rate, timeout=timeout)

    def down_swipe_find_ele_by_id(self, eid, rate=0.5, timeout=30):
        """
        向下滑动手机，并通过元素id查找元素
        Args:
           eid: 元素id
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        return self.swipe_timeout_find_ele_by_id(eid, x_rate=0, y_rate=rate, timeout=timeout)

    def left_swipe_find_ele_by_id(self, eid, rate=0.5, timeout=30):
        """
        向左滑动手机，并通过元素id查找元素
        Args:
           eid: 元素id
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        return self.swipe_timeout_find_ele_by_id(eid, rate, timeout)

    def right_swipe_find_ele_by_id(self, eid, rate=0.5, timeout=30):
        """
        向右滑动手机，并通过元素id查找元素
        Args:
           eid: 元素id
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        return self.swipe_timeout_find_ele_by_id(eid, x_rate=rate, timeout=timeout)

    def swipe_timeout_find_ele_by_id(self, eid, x_rate=0.0, y_rate=0.0, timeout=30):
        x_offset = int(self.get_window_width()) * x_rate
        y_offset = int(self.get_window_width()) * y_rate
        time_start = time.time()
        while True:
            try:
                ele = self.find_element_by_id(eid, timeout=2)
                return ele
            except:
                if time.time() - time_start < timeout:
                    try:
                        self.scroll_windows(x_offset, y_offset)
                    except:
                        g_logger.info("swipe_timeout_find_ele_by_id滑动屏幕超时")
                        return None
                    time.sleep(2)
                    continue
                else:
                    break

        raise TimeoutError("run find_element_by_xpath({}) timeout!".format(eid))

    def swipe_down_find_ele(self, xpath=None, id=None, rate=0.3, timeout=60):
        """
        向下滑动查找元素
        Args:
            xpath: 元素xpath
            id: 元素id
            rate: 滑动比例
            timeout: 超时
        Returns:
            True: 进入游戏详情页成功
            False: 进入失败
         """
        if id is None and xpath is None:
            g_logger.warning("向下滑动查找元素，需要传入id或xpath一个")
            return None
        height = self.get_window_height()
        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                if id:
                    ele = self.find_element_by_id(id, timeout=3)
                    return ele
                else:
                    ele = self.find_element_by_xpath(xpath, timeout=3)
                    return ele
            except:
                self.scroll_windows(offset_x=0, offset_y=height*rate)
                time.sleep(3)
                continue
        else:
            g_logger.warning("向下滑动查找元素，未找到")
            return None

    @staticmethod
    def check_ele_on_ele(ele1, ele2):
        """
        检测两个元素是否重叠
        Args:
            ele1: 元素实例1
            ele2: 元素实例2

        Returns:
            True: 检查元素成功， False: 检查失败
        """
        e1_location = ele1.location
        e1_size = ele1.size
        e2_location = ele2.location
        e2_size = ele2.size
        x1, y1, w1, h1 = e1_location['x'], e1_location['y'], e1_size['width'], e1_size['height']
        x2, y2, w2, h2 = e2_location['x'], e2_location['y'], e2_size['width'], e2_size['height']
        return abs(x1 - x2) < (w1 + w2) / 2 and abs(y1 - y2) < (h1 + h2) / 2

    def check_ele_on_bottom(self, ele):
        """
        检测元素是否在底部
        Args:
            ele: 元素实例
        Returns:
        """
        if not self._window_size:
            size = self.get_window_size()
            self._window_size = {'width': size.get('width'), 'height': size.get('height')}
        try:
            return ele.location['y'] + ele.size['height'] == self._window_size['height']
        except:
            return False

    def check_ele_is_side(self, ele, side_type="down"):
        """
        检测元素处于边界
        Args:
            ele: 元素实例
            side_type: 边界类型，取值："down","up","left", "right"
        Returns:
            True: 处于边界，False: 不处于边界
        """
        size = self.get_window_size()
        width = size.get('width')
        height = size.get('height')
        x, y = ele.location['x'], ele.location['y']
        ele_w, ele_h = ele.size['width'], ele.size['height']
        bounds = {"down": y + ele_h < width, "up": y == 0, "left": x == 0, "right": x + ele_w < height}
        return bounds.get(side_type, None)

    # def get_texts_between_xpath(self, find_xpath, start_xpath, end_xpath, rate=0.3, timeout=120):
    #     """
    #     获取文本信息，从两个元素之间
    #     Args:
    #         find_xpath: 带查找文本的元素xpath
    #         start_xpath: 开始标志元素xpath
    #         end_xpath:  结束标志元素xpath
    #         rate: 滑动比例
    #         timeout: 超时
    #
    #     Returns:
    #         list: 查找到的文本列表，False: 查找失败
    #     """
    #     if not self.swipe_down_find_ele(xpath=start_xpath, timeout=timeout):
    #         g_logger.warning("查找开始元素失败")
    #         return False
    #
    #     find_text = []
    #     size = self.get_window_size()
    #     width = size.get('width')
    #     height = size.get('height')
    #     x = width / 2
    #     y_start = height * (1 + rate) / 2
    #     y_end = height * (1 - rate) / 2
    #     time_start = time.time()
    #     while timeout > time.time() - time_start:
    #         eles = self.find_elements_by_xpath(find_xpath, timeout=3)
    #         if eles:
    #             find_text.extend([ele.get_attribute("text") for ele in eles])
    #         try:
    #             self.find_element_by_xpath(end_xpath, timeout=3)
    #             break
    #         except:
    #             self.swipe(x, y_start, x, y_end)
    #             time.sleep(2)
    #     else:
    #         g_logger.warning("查找结束元素超时")
    #         return False
    #
    #     find_order_list = list(set(find_text))
    #     find_order_list.sort(key=find_text.index)
    #     g_logger.info("查找的的文本：{}".format(",".join(find_order_list)))
    #     return find_order_list

    def click_textview_text(self, text, xpath=None, id=None, swipe=False, timeout=5):
        """
        点击Textview控件的text
        Args:
            text: 待查找的文本
            timeout: 查找超时时间
            swipe: 是否向下滑动查找
        Returns:
            True: 找到此text的TextView,并执行了点击操作，False: 未找到元素
        """
        if swipe:
            ele = self.swipe_down_find_ele(xpath=xpath, id=id)
        else:
            if xpath:
                ele = self.find_element_by_xpath(xpath)
            elif id:
                ele = self.find_element_by_id(id)
            else:
                ele = None

        if ele and ele.get_attribute("text") == text:
            ele.click()
            g_logger.info("点击文本:{} 成功".format(text))
            time.sleep(2)
            return True
        else:
            return False

    def swipe_ele_down_by_class(self, class_name, rate=0.3):
        """
        滑动元素，使用class方式查找
        Args:
            class_name: class名
        Returns:
            True: 滑动成功, False: 滑动失败
        """
        # element = self.driver.find_element_by_class_name(class_name)
        # y_scroll = int(element.size['height'] * rate)
        # actions = IActionChains(self.driver)
        # actions.drag_and_drop_by_offset(element, 0, y_scroll)
        # actions.perform()
        # time.sleep(0.5)
        self.swipe_ele_down(By.CLASS_NAME, class_name)

    def swipe_ele_down(self, by, value, rate=0.3):
        """
        滑动元素，使用class方式查找
        Args:
            by: by类型
            value: 查找表达式
        Returns:
            True: 滑动成功, False: 滑动失败
        """
        element = self.find_element(by, value)
        y_scroll = int(element.size['height'] * rate)
        with self.action as action:
            action.drag_and_drop_by_offset(element, 0, y_scroll)
        time.sleep(0.5)

    def swipe_ele_by_xpath(self, xpath, width=0, height=0):
        """
        滑动元素
        Args:
            xpath: xpath表达式
            width: 横向滑动像素值
            height: 纵向滑动像素值
        Returns:
            True: 滑动成功, False: 滑动失败
        """
        ele = self.get_ele_by_xpath(xpath, timeout=3)
        if not ele:
            return g_logger.error("滑动元素：查找元素失败")
        with self.action as action:
            action.click_and_hold(ele)
            action.move_by_offset(xoffset=width, yoffset=height)
            action.release()
        time.sleep(0.5)
        return True

    def swipe_ele_down_by_class_find_ele(self, swipe_class, find_type="xpath", find_text=None, timeout=30):
        """
        通过class查找元素并向下滑动，再查找元素
        Args:
            swipe_class: 滑动元素的class名
            find_type: 查找元素的类型，包含：xpath，id, name, class_name，tag_name，link_ext, partial_link_text, css_selector
            find_text: 查找表达式如[//div[@class='modal']]
        Returns:
            ele
        """
        return self.swipe_ele_down_find_ele(By.CLASS_NAME, swipe_class, find_type=find_type, find_text=find_text, timeout=timeout)

    def swipe_ele_down_by_xpath_find_ele(self, swipe_xpath, find_type="xpath", find_text=None, timeout=30):
        """
        通过class查找元素并向下滑动，再查找元素
        Args:
            swipe_xpath: 滑动元素的xpath路径表达式
            find_type: 查找元素的类型，包含：xpath，id, name, class_name，tag_name，link_ext, partial_link_text, css_selector
            find_text: 查找表达式如[//div[@class='modal']]
        Returns:
            ele
        """
        return self.swipe_ele_down_find_ele(By.XPATH, swipe_xpath, find_type=find_type, find_text=find_text, timeout=timeout)

    def swipe_ele_down_find_ele(self, swipe_by, swipe_value, find_type="xpath", find_text=None, timeout=30):
        """
        通过class查找元素并向下滑动，再查找元素
        Args:
            swipe_by: swipe查找类型,参见selenium.webdriver.common.by.By类
            swipe_value: swipe元素查找表达式
            find_type: 查找元素的类型，包含：xpath，id, name, class_name，tag_name，link_ext, partial_link_text, css_selector
            find_text: 查找表达式如[//div[@class='modal']]
        Returns:
            ele
        """
        try:
            func = self.__getattribute__("find_element_by_{}".format(find_type))
        except:
            g_logger.error("find_type参数不正确，传值范围：xpath，id, name, class_name，tag_name，link_ext, partial_link_text, css_selector")
            return None
        if find_text is None:
            g_logger.error("参数find_text需要指定对应查找规则")
            return None

        time_start = time.time()
        try:
            while time.time() - time_start < timeout:
                try:
                    ele = func(find_text, timeout=3)
                    if not ele.is_displayed():
                        self.swipe_ele_down(swipe_by, swipe_value)
                        continue
                    return ele
                except Exception as e:
                    self.swipe_ele_down(swipe_by, swipe_value)
        except Exception as e:
            g_logger.error("向下滑动查找元素[find_type:{}, find_text:{}]产生异常，异常信息：{}".format(find_type, find_text, str(e)))
        return None

    def check_ele_text_by_xpath(self, xpath, text=None, desc="", timeout=5):
        """
        使用xpath方式检测元素text信息
        Args:
            xpath: 元素xpath路径
            text: 文本信息
            desc: 检测描述
            timeout: 检测超时时间
        Returns:
            True: 检测成功, False: 检测失败
        """
        return self.check_ele_text(By.XPATH, xpath, text=text, desc=desc, timeout=timeout)

    def check_ele_text_by_id(self, id, text=None, desc="", timeout=5):
        """
        使用xpath方式检测元素text信息
        Args:
            id: 元素xpath路径
            text: 文本信息
            desc: 检测描述
            timeout: 检测超时时间
        Returns:
            True: 检测成功, False: 检测失败
        """
        return self.check_ele_text(By.ID, id, text=text, desc=desc, timeout=timeout)

    def check_ele_text(self, by, by_value, text=None, desc="", timeout=5):
        """
        检测元素text信息
        Args:
            by: 查找类型，参见selenium.webdriver.common.by.By类
            by_value: 查找表达式信息
            text: 文本信息
            desc: 检测描述
            timeout: 检测超时时间
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            ele = self.find_element(by, by_value, timeout=timeout)
            return self.check_ele_text_by_ele(ele, text=text, desc=desc, timeout=timeout)
        except:
            return g_logger.error("查找{}元素失败".format(desc))

    @classmethod
    def check_ele_text_by_ele(cls, ele, text=None, desc="", timeout=5):
        """
        通过元素实例来检测元素text信息
        Args:
            ele: 元素对象
            text: 文本信息
            desc: 检测描述
            timeout: 检测超时时间
        Returns:
            True: 检测成功, False: 检测失败
        """
        if text:
            if text not in ele.text:
                return g_logger.error("{}匹配失败, 期望值[{}], 实际值[{}]".format(desc, text, ele.text))
            else:
                return g_logger.info("{}匹配成功, 期望值[{}], 实际值[{}]".format(desc, text, ele.text))
        else:
            return g_logger.info("不匹配，{}元素文本: {}".format(desc, ele.text))

    def check_ele_by_xpath(self, xpath, timeout=5):
        """
        通过xpath检测元素是否存在
        Args:
            xpath: xpath
            timeout: 检测超时时间
        Returns:
            True: 检测成功, False:检测失败
        """
        return self.check_ele_display(By.XPATH, xpath)

    def check_ele_by_id(self, id, timeout=5):
        """
        通过id检测元素是否存在,且显示出来
        Args:
            id: id
            timeout: 检测超时时间
        Returns:
            True: 检测成功, False:检测失败
        """
        return self.check_ele_display(By.ID, id)

    def check_ele_display(self, by, value, timeout=5):
        """
        检测元素是否显示出来
        Args:
            by: 查找类型,参见selenium.webdriver.common.by.By类
            value: 查找表达式
            timeout: 查找超时
        Returns:
            True: 查找成功, False: 查找失败
        """
        try:
            ele = self.find_element(by, value, timeout=timeout)
            if ele.is_displayed():
                return True
            return False
        except Exception as e:
            return False

    def get_ele_by_xpath(self, xpath, timeout=5):
        """
        获取元素，通过xpath
        Args:
            xpath: 元素xpath表达式
            timeout: 查找元素超时
        Returns:
            ele: 查找到的元素, None:未找到元素
        """
        try:
            ele = self.find_element_by_xpath(xpath, timeout=timeout)
            return ele
        except Exception as e:
            return None

    def get_ele_by_tag_name(self, tag_name, timeout=5):
        """
        获取元素，Tag名
        Args:
            tag_name: 元素tag名
            timeout: 查找元素超时
        Returns:
            ele: 查找到的元素, None:未找到元素
        """
        try:
            ele = self.find_element_by_tag_name(tag_name, timeout=timeout)
            return ele
        except Exception as e:
            return None

    def get_ele_by_id(self, id, timeout=5):
        """
        通过id获取元素
        Args:
            id: 元素xpath表达式
            timeout: 查找元素超时
        Returns:
            ele: 查找到的元素, None:未找到元素
        """
        try:
            ele = self.find_element_by_id(id, timeout=timeout)
            return ele
        except:
            return None

    def get_ele_by_class(self, cls, timeout=5):
        """
        通过class获取元素
        Args:
            cls: 元素class表达式
            timeout: 查找元素超时
        Returns:
            ele: 查找到的元素, None:未找到元素
        """
        try:
            ele = self.find_element_by_class_name(cls, timeout=timeout)
            return ele
        except:
            return None

    def get_ele_by_link_text(self, link_text, timeout=5):
        """
        通过链接文本获取元素
        Args:
            link_text: 元素link_text表达式
            timeout: 查找元素超时
        Returns:
            ele: 查找到的元素, None:未找到元素
        """
        try:
            ele = self.find_element_by_link_text(link_text, timeout=timeout)
            return ele
        except:
            return None

    def get_ele_by_partial_link_text(self, partial_link_text, timeout=5):
        """
        通过部分链接文本获取元素
        Args:
            partial_link_text: 元素partial_link_text表达式
            timeout: 查找元素超时
        Returns:
            ele: 查找到的元素, None:未找到元素
        """
        try:
            ele = self.find_element_by_partial_link_text(partial_link_text, timeout=timeout)
            return ele
        except:
            return None

    def get_ele_by_css_selector(self, css_selector, timeout=5):
        """
        通过css选择器获取元素
        Args:
            css_selector: 元素css_selector表达式
            timeout: 查找元素超时
        Returns:
            ele: 查找到的元素, None:未找到元素
        """
        try:
            ele = self.find_element_by_css_selector(css_selector, timeout=timeout)
            return ele
        except:
            return None


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://gamelive.iqiyi.com/cate/game")
    time.sleep(2)
    ele = driver.find_element_by_xpath("//div[@class='_ok lottery-close']")
    windows_size = ele.location
    ele.click()
    time.sleep(0.5)

    # room_ele = driver.find_element_by_id("room")
    # first_room = room_ele.find_element_by_class_name("item")
    # location = first_room.location
    # size = first_room.size
    #
    # action = webdriver.common.action_chains.ActionChains(driver)

    # element = driver.find_element_by_tag_name('body')
    # s_x, s_y = element.size['width'], element.size['height']
    # action.move_to_element(element)
    # action.move_by_offset(-s_x/2, -s_y/2)

    # action.move_by_offset(location['x'] + int(size['width']/2), location['y'] + int(size['height']/2))
    # action.click()

    # action.click_and_hold(first_room)
    # action.move_by_offset(0, 300)
    # action.release()
    # action.perform()
    #
    # time.sleep(2)
    # print(first_room.get_attribute("innerHTML"))
    driver.quit()



