# -*- coding: UTF-8 -*-

"""
File Name:      base_api
Author:         zhangwei04
Create Date:    2018/1/16
"""
import time
from framework.utils.appium.remote import AppiumRemote
from framework.utils.func import timeout_decorate, ping_back
from framework.exception.exception import ParamaterError
from framework.logger.logger import g_logger

DIRECTIONS = {"up", "down", "left", "right"}


class BaseApi(object):
    """Appium Server 基本通讯API"""
    def __init__(self):
        # self.driver = AppiumRemote()
        self.driver = None
        self._window_size = None

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def execute_script(self, script, timeout=None, *args):
        """
        脚本方式执行接口
        Args:
            script: 脚本名（接口名）
            *args: 命令参数（字典方式）
            timeout: 命令执行超时，单位: 秒
        Returns:
            执行结果
        """
        return self.driver.execute_script(script, *args)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_element_by_ios_uiautomation(self, uia_string, timeout=None):
        """
        通过ios uiautomation方式查找元素
        Args:
            uia_string:uiautomation 字符串
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        return self.driver.find_element_by_ios_uiautomation(uia_string)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_elements_by_ios_uiautomation(self, uia_string, timeout=None):
        """
        通过IOS uiautomation方式查找元素集合
        Args:
            uia_string:uiautomation 字符串
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        return self.driver.find_elements_by_ios_uiautomation(uia_string)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_element_by_android_uiautomator(self, uia_string, timeout=None):
        """
        通过Android uiautomator方式查找元素
        Args:
            uia_string: uiautomator 字符串
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        return self.driver.find_element_by_android_uiautomator(uia_string)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_elements_by_android_uiautomator(self, uia_string, timeout=None):
        """
        通过Android uiautomator方式查找元素集合
        Args:
            uia_string: uiautomator 字符串
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        return self.driver.find_elements_by_android_uiautomator(uia_string)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_element_by_accessibility_id(self, id, timeout=None):
        """
        通过content-desc属性查找元素
        Args:
            id: 元素content-desc属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        return self.driver.find_element_by_accessibility_id(id)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_elements_by_accessibility_id(self, id, timeout=None):
        """
        通过content-desc属性查找元素集合
        Args:
            id: 元素content-desc属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        return self.driver.find_elements_by_accessibility_id(id)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_element_by_id(self, id, timeout=None) -> object:
        """
        通过id查找元素
        Args:
            id: 元素id属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        return self.driver.find_element_by_id(id)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_elements_by_id(self, id, timeout=None):
        """
        通过id查找元素集合
        Args:
            id: 元素id属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        return self.driver.find_elements_by_id(id)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_element_by_xpath(self, xpath, timeout=None):
        """
        通过xpath查找元素
        Args:
            xpath: xpath 路径
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        return self.driver.find_element_by_xpath(xpath)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_elements_by_xpath(self, xpath, timeout=None):
        """
        通过xpath查找元素集合
        Args:
            xpath: xpath 路径
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        return self.driver.find_elements_by_xpath(xpath)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_element_by_name(self, name, timeout=None):
        """
        通过元素name属性查找元素
        Args:
            name: 元素name属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        return self.driver.find_element_by_name(name)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_elements_by_name(self, name, timeout=None):
        """
        通过元素name属性查找元素集合
        Args:
            name: 元素name属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        return self.driver.find_elements_by_name(name)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_element_by_class_name(self, name, timeout=None):
        """
        通过元素class属性查找元素
        Args:
            name: 元素class属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        return self.driver.find_element_by_class_name(name)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_elements_by_class_name(self, name, timeout=None):
        """
        通过元素class属性查找元素集合
        Args:
            name: 元素class属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例列表
        """
        return self.find_elements_by_class_name(name)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def find_element(self, by, value, timeout=None):
        """
        查找元素
        Args:
            by: 查找方式（By.ID, By.TAG_NAME, By.CLASS_NAME...）
            value:属性值
            timeout: 命令执行超时，单位: 秒
        Returns:
            元素实例
        """
        return self.driver.find_element(by, value)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def is_app_installed(self, bundle_id, timeout=None):
        """
        检测app是否安装
        Args:
            bundle_id: 已经安装app的bundle id
            timeout: 命令执行超时，单位: 秒
        Returns:
            True: 已经安装，False: 没有安装
        """
        return self.driver.is_app_installed(bundle_id)

    @timeout_decorate(dec_timeout=2, ignore_exception=True)
    def tap(self, positions, duration=None, timeout=None):
        """
        按坐标点击操作
        Args:
            positions: 坐标元组列表 eg: [(x,y)]
            duration: 按压时间，单位ms
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.tap(positions, duration)

    def screen_tap(self, conf_ele, duration=None, timeout=None):
        """
        按坐标点击操作
        Args:
            positions: 坐标元组列表 eg: [(x,y)]
            duration: 按压时间，单位ms
            timeout: 命令执行超时，单位: 秒
        """
        size = self.get_window_size()
        width = size.get('width')
        height = size.get('height')
        x_axis = getattr(conf_ele, "x_{}".format(width))
        y_axis = getattr(conf_ele, "y_{}".format(height))
        # if height == 1794:
        #     y_axis = conf_ele.y_1794
        # elif height == 1920:
        #     y_axis = conf_ele.y_1920
        # elif height == 2118:
        #     y_axis = conf_ele.y_2118
        # else:
        #     raise ParamaterError("没有配置此分辨率")
        #
        # if width == 540:
        #     x_axis = conf_ele.x_540
        # elif width == 720:
        #     x_axis = conf_ele.x_720
        # elif width == 1080:
        #     x_axis = conf_ele.x_1080
        # else:
        #     raise ParamaterError("没有配置此分辨率")

        self.driver.tap([(x_axis, y_axis)], duration=duration)

    @timeout_decorate(dec_timeout=2, ignore_exception=True)
    def click_from_position(self, x_rate, y_rate, duration=50, sleep_time=2):
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

        self.driver.tap([pos], duration)
        time.sleep(sleep_time)

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def swipe(self, start_x, start_y, end_x, end_y, duration=None, timeout=None):
        """
        滑动操作
        Args:
            start_x: 起始x轴像素位置
            start_y: 起始y轴像素位置
            end_x: 结束x轴像素位置
            end_y: 结束y轴像素位置
            duration: 滑动时长, 单位秒
            timeout: 命令执行超时，单位: 秒
        """
        if duration:
            duration = int(duration) * 1000  # 单位统一
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def flick(self, start_x, start_y, end_x, end_y, timeout=None):
        """
        快速滑动
        Args:
            start_x: 起始x轴像素位置
            start_y: 起始y轴像素位置
            end_x: 结束x轴像素位置
            end_y: 结束y轴像素位置
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.flick(start_x, start_y, end_x, end_y)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def set_text(self, element, value, timeout=None):
        """
        设置文本框内容，Android可用
        Args:
            element: 元素实例
            value: 文本值
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.set_text(element, value)

    # ios可用
    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def set_value(self, element, value, timeout=None):
        """
        设置文本框内容，IOS可用
        Args:
            element: 元素实例
            value: 文本值
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.set_value(element, value)

    # 截图
    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def get_screenshot_as_file(self, filename, timeout=None):
        """
        获取屏幕截图
        Args:
            filename: 存储文件名
            timeout: 命令执行超时，单位: 秒
        Returns:
            True: 截图成功，False: 截图失败
        """
        return self.driver.get_screenshot_as_file(filename)

    # 获取手机屏幕分辨率
    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def get_window_size(self, window_handle='current', timeout=None):
        """
        获取窗口尺寸
        Args:
            window_handle:窗口
            timeout: 命令执行超时，单位: 秒
        Returns:
            宽和高的字典, eg: {'width':768, 'height':1024}
        """
        if not self._window_size:
            self._window_size = self.driver.get_window_size(window_handle)
        return self._window_size
        # return self.driver.get_window_size(window_handle)

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

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
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

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def get_window_position(self, window_handle='current', timeout=None):
        """
        获取窗口位置
        Args:
            window_handle: 窗口句柄
            timeout: 命令执行超时，单位: 秒
        Returns:
            窗口位置
        """
        return self.driver.get_window_position(window_handle)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def scroll(self, origin_el, destination_el, timeout=None):
        """
        滑动元素
        Args:
            origin_el:源元素控件对象
            destination_el:目标元素控件对象
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.scroll(origin_el, destination_el)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def drag_and_drop(self, origin_el, destination_el, timeout=None):
        """
        拖一个元素到另外一个元素上
        Args:
            origin_el: 源元素实例
            destination_el:  目标元素
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.drag_and_drop(origin_el, destination_el)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def pinch(self, element=None, percent=200, steps=50, timeout=None):
        """
        缩小元素
        Args:
            element:元素实例
            percent: 缩小百分比
            steps: 缩小的步骤
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.pinch(element, percent, steps)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def zoom(self, element=None, percent=200, steps=50, timeout=None):
        """
        放大元素
        Args:
            element: 元素实例
            percent: 放大百分比
            steps: 放大步骤
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.zoom(element, percent, steps)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def reset(self, timeout=None):
        """
        重置APP，并会清空APP数据
        Args:
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.reset()

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def hide_keyboard(self, key_name=None, key=None, strategy=None, timeout=None):
        """
        隐藏设备上的软件键盘。在IOS中，使用'key_name'按下一个特定键，Android中不使用任何参数
        Args:
            key_name: 特定键名
            key: 特定键元素实例
            strategy: 关键盘使用策略，如'tapOutside'
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.hide_keyboard(key_name, key, strategy)

    # 针对 Selendroid
    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def keyevent(self, keycode, metastate=None, timeout=None):
        """
        发送一个键盘事件，仅支持Android，事件码参考链接: http://developer.android.com/reference/android/view/KeyEvent.html
        Args:
            keycode: 事件码
            metastate: 发送秘钥代码的原信息
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.keyevent(keycode, metastate)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def press_keycode(self, keycode, metastate=None, timeout=None):
        """
        发送一个键盘事件，仅支持Android，事件码参考链接: http://developer.android.com/reference/android/view/KeyEvent.html
        Args:
            keycode: 事件码
            metastate: 发送秘钥代码的原信息
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.press_keycode(keycode, metastate)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def long_press_keycode(self, keycode, metastate=None, timeout=None):
        """
        长按键盘事件，仅支持Android，事件码参考链接: http://developer.android.com/reference/android/view/KeyEvent.html
        Args:
            keycode: 事件码
            metastate: 发送秘钥代码的原信息
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.long_press_keycode(keycode, metastate)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def push_file(self, path, base64data, timeout=None):
        """
        发送一个以Base64编码方式的数据流到设备指定path的文件中
        Args:
            path: 设备上文件路径
            base64data: 以Base64方式编码的数据流
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.push_file(path, base64data)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def pull_file(self, path, timeout=None):
        """
        将设备中文件内容以Base64编码方式pull出来
        Args:
            path: 设备上文件路径
            timeout: 命令执行超时，单位: 秒

        Returns:
            Base64编码方式的数据流
        """
        return self.driver.pull_file(path)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def pull_folder(self, path, timeout=None):
        """
        在设备path减速文件夹。返回压缩并编码为base64方式的文件夹内容
        Args:
            path: 设备上的目标路径
            timeout: 命令执行超时，单位: 秒
        Returns:
            编码为base64方式的数据流
        """
        return self.driver.pull_folder(path)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def background_app(self, seconds, timeout=None):
        """
        将app调至后台一定时间
        Args:
            seconds: 放置后台的时间，单位: 秒
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.background_app(seconds)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def install_app(self, app_path, timeout=None):
        """
        安装app到设备上
        Args:
            app_path: app路径
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.install_app(app_path)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def remove_app(self, app_id, timeout=None):
        """
        移除设备上的app
        Args:
            app_id: app的bundle_id
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.remove_app(app_id)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def launch_app(self, timeout=None):
        """
        打开app，设备配置文件配置的app
        Args:
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.launch_app()

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def close_app(self, timeout=None):
        """
        关闭app，设备配置文件配置的app
        Args:
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.close_app()

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def start_activity(self, app_package, app_activity, timeout=None, **opts):
        """打开任意一个activity，如果activity依赖其他的app，则打开启动这app再打开此activity，仅支持Android
        Args:
            app_package: app包名（非apk文件名）
            app_activity: 待启动的activity
            timeout: 命令执行超时，单位: 秒
            **opts: 其他可选操作操作
                - app_wait_package - 等待安装包完成
                - app_wait_activity - 等待activity启动完成
                - intent_action - 指定将要启动的intent操作
                - intent_category - 将要启动的intent类型
                - intent_flags - 发送intent的标志
                - optional_intent_arguments - intent操作参数
                - dont_stop_app_on_reset - app reset是否停止此activity
        """
        self.driver.start_activity(app_package, app_activity, **opts)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def current_activity(self, timeout=None):
        """
        获取当前的activity名称
        Args:
            timeout: 命令执行超时，单位: 秒

        Returns:
            当前的activity名称
        """
        return self.driver.current_activity()

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def lock(self, seconds, timeout=None):
        """
        锁定手机，仅支持iOS
        Args:
            seconds: 锁定时间
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.lock(seconds)
    # 暂未实现
    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    # def shake(self, timeout=None):
    #     """
    #     震动设备
    #     Args:
    #         timeout: 命令执行超时，单位: 秒
    #
    #     Returns:
    #
    #     """
    #     self.driver.shake()

    # 打开通知栏(api18以上)
    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def open_notifications(self, timeout=None):
        """
        打开通知栏
        Args:
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.open_notifications()

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def network_connection(self, timeout=None):
        """
        获取网络连接信息
        Args:
            timeout: 命令执行超时，单位: 秒

        Returns:
            返回网络连接类型
        """
        return self.driver.network_connection()

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def set_network_connection(self, connection_type, timeout=None):
        """
        设置网络连接
        Args:
            connection_type: 网络连接类型
                取值范围: 
                Value              | Data | Wifi | Airplane Mode
                -------------------------------------------------
                0 (None)           | 0    | 0    | 0
                1 (Airplane Mode)  | 0    | 0    | 1
                2 (Wifi only)      | 0    | 1    | 0
                4 (Data only)      | 1    | 0    | 0
                6 (All network on) | 1    | 1    | 0
            timeout: 命令执行超时，单位: 秒
        """
        return self.driver.set_network_connection(connection_type)

    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def toggle_location_services(self, timeout=None):
        """
        切换位置服务，仅支持Android
        Args:
            timeout: 命令执行超时，单位: 秒
        """
        self.driver.toggle_location_services()

    @ping_back
    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def click_by_id(self, id, timeout=10, time_sleep=2, *args, **kwargs):
        """
       通过id查找元素, 并点击
       Args:
           id: 元素id属性值
           timeout: 命令执行超时，单位: 秒
       Returns:
           True: 元素找到，并执行点击动作
           False: 元素没有找到
       """
        desc = kwargs.get("desc", "")
        if desc:
            try:
                g_logger.info("{}...".format(desc))
                ele = self.find_element_by_id(id, timeout=timeout)
                ele.click()
                time.sleep(time_sleep)
                g_logger.info("{} 结束".format(desc))
            except Exception as e:
                return g_logger.error("{} 超时".format(desc))
        else:
            try:
                self.find_element_by_id(id, timeout=timeout).click()
                time.sleep(time_sleep)
            except Exception as e:
                return False
        return True

    @ping_back
    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def click_by_xpath(self, xpath, timeout=10, time_sleep=2, *args, **kwargs):
        """
        通过xpath查找元素， 并点击
        Args:
            xpath: xpath 路径
            timeout: 命令执行超时，单位: 秒
        Returns:
            True: 元素找到，并执行点击动作
            False: 元素没有找到
        """
        desc = kwargs.get("desc", "")
        if desc:
            try:
                g_logger.info("{}...".format(desc))
                ele = self.find_element_by_xpath(xpath, timeout=timeout)
                # g_logger.info("元素位置：{} 尺寸{}".format(ele.location, ele.size))
                ele.click()
                time.sleep(time_sleep)
                g_logger.info("{} 结束".format(desc))
            except Exception as e:
                return g_logger.error("{} 超时".format(desc))
        else:
            try:
                self.find_element_by_xpath(xpath, timeout=timeout).click()
                time.sleep(time_sleep)
            except Exception as e:
                return False
        return True

    @ping_back
    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def set_text_by_id(self, id, text, timeout=None, *args, **kwargs):
        """
       通过id查找元素, 并设置文本
       Args:
           id: 元素id属性值
           timeout: 命令执行超时，单位: 秒
           text: 设置的文本
       Returns:
           True: 元素找到，并执行点击动作
           False: 元素没有找到
       """
        try:
            self.find_element_by_id(id, timeout=timeout).set_text(text)
        except:
            return False
        return True

    @ping_back
    @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def set_text_by_xpath(self, xpath, text, timeout=None, *args, **kwargs):
        """
        通过xpath查找元素， 并设置文本
        Args:
            xpath: xpath 路径
            timeout: 命令执行超时，单位: 秒
            text: 设置的文本
        Returns:
            True: 元素找到，并执行点击动作
            False: 元素没有找到
        """
        try:
            self.find_element_by_xpath(xpath, timeout=timeout).set_text(text)
        except:
            return False
        return True

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def swipe_find_ele_by_xpath(self, xpath, direct="up", rate=0.4, timeout=60):
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
        return func(xpath, rate=rate, timeout=timeout)

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def up_swipe_find_ele_by_xpath(self, xpath, rate=0.5, timeout=60):
        """
        向上滑动手机，并通过xpath路径查找元素
        Args:
            xpath: xpath 路径
            rate: 滑动幅度，屏幕占比，默认0.5
            timeout: 超时
        Returns:
            元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        start_rate = (1 + rate) / 2
        end_rate = (1 - rate) / 2
        return self.swipe_timeout_find_ele_by_xpath(xpath, 0.5, start_rate, 0.5, end_rate, timeout)

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def down_swipe_find_ele_by_xpath(self, xpath, rate=0.5, timeout=60):
        """
        向下滑动手机，并通过xpath路径查找元素
        Args:
           xpath: xpath 路径
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        start_rate = (1 - rate) / 2
        end_rate = (1 + rate) / 2
        return self.swipe_timeout_find_ele_by_xpath(xpath, 0.5, start_rate, 0.5, end_rate, timeout)

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def left_swipe_find_ele_by_xpath(self, xpath, rate=0.4, timeout=60):
        """
        向左滑动手机，并通过xpath路径查找元素
        Args:
           xpath: xpath 路径
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        start_rate = (1 + rate) / 2
        end_rate = (1 - rate) / 2
        return self.swipe_timeout_find_ele_by_xpath(xpath, start_rate, 0.5, end_rate, 0.5, timeout)

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def right_swipe_find_ele_by_xpath(self, xpath, rate=0.5, timeout=60):
        """
        向右滑动手机，并通过xpath路径查找元素
        Args:
           xpath: xpath 路径
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        start_rate = (1 - rate) / 2
        end_rate = (1 + rate) / 2
        return self.swipe_timeout_find_ele_by_xpath(xpath, start_rate, 0.5, end_rate, 0.5, timeout)

    def swipe_timeout_find_ele_by_xpath(self, xpath, x_start, y_start, x_end, y_end, timeout):
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
        size = self.get_window_size()
        width = size.get('width')
        height = size.get('height')

        time_start = time.time()
        while time.time() - time_start < timeout:
            try:
                ele = self.find_element_by_xpath(xpath, timeout=2)
                return ele
            except:
                try:
                    self.swipe(width * float(x_start) if float(x_start) < 1 else float(x_start),
                               height * float(y_start) if float(y_start) < 1 else float(y_start),
                               width * float(x_end) if float(x_end) < 1 else float(x_end),
                               height * float(y_end) if float(y_end) < 1 else float(y_end))
                except:
                    g_logger.info("swipe_timeout_find_ele_by_xpath滑动屏幕超时")
                    return None
                time.sleep(2)
        return None

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def swipe_find_ele_by_id(self, eid, direct="down", rate=0.5, timeout=60):
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
        return func(eid, rate=rate, timeout=timeout)

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def up_swipe_find_ele_by_id(self, eid, rate=0.5, timeout=60):
        """
        向上滑动手机，并通过元素id查找元素
        Args:
           eid: 元素id
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        start_rate = (1 + rate) / 2
        end_rate = (1 - rate) / 2
        return self.swipe_timeout_find_ele_by_id(eid, 0.5, start_rate, 0.5, end_rate, timeout)

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def down_swipe_find_ele_by_id(self, eid, rate=0.5, timeout=60):
        """
        向下滑动手机，并通过元素id查找元素
        Args:
           eid: 元素id
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        start_rate = (1 - rate) / 2
        end_rate = (1 + rate) / 2
        return self.swipe_timeout_find_ele_by_id(eid, 0.5, start_rate, 0.5, end_rate, timeout)

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def left_swipe_find_ele_by_id(self, eid, rate=0.5, timeout=60):
        """
        向左滑动手机，并通过元素id查找元素
        Args:
           eid: 元素id
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        start_rate = (1 + rate) / 2
        end_rate = (1 - rate) / 2
        return self.swipe_timeout_find_ele_by_id(eid, start_rate, 0.5, end_rate, 0.5, timeout)

    # @timeout_decorate(dec_timeout=60, ignore_exception=True)
    def right_swipe_find_ele_by_id(self, eid, rate=0.5, timeout=60):
        """
        向右滑动手机，并通过元素id查找元素
        Args:
           eid: 元素id
           rate: 滑动幅度，屏幕占比，默认0.5
           timeout: 超时
        Returns:
           元素被找到，返回元素对象，元素没有找到，抛出TimeoutError异常
        """
        start_rate = (1 - rate) / 2
        end_rate = (1 + rate) / 2
        return self.swipe_timeout_find_ele_by_id(eid, start_rate, 0.5, end_rate, 0.5, timeout)

    def swipe_timeout_find_ele_by_id(self, eid, x_start, x_end, y_start, y_end, timeout):
        size = self.get_window_size()
        width = size.get('width')
        height = size.get('height')

        time_start = time.time()
        while True:
            try:
                ele = self.find_element_by_id(eid, timeout=2)
                return ele
            except:
                if time.time() - time_start < timeout:
                    try:
                        self.swipe(width * float(x_start) if float(x_start) < 1 else float(x_start),
                                   height * float(y_start) if float(y_start) < 1 else float(y_start),
                                   width * float(x_end) if float(x_end) < 1 else float(x_end),
                                   height * float(y_end) if float(y_end) < 1 else float(y_end))
                    except:
                        g_logger.info("swipe_timeout_find_ele_by_id滑动屏幕超时")
                        return None
                    time.sleep(2)
                    continue
                else:
                    break

        raise TimeoutError("run find_element_by_xpath({}) timeout!".format(eid))

    def swipe_down_find_ele(self, xpath=None, id=None, rate=0.3, timeout=120):
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
        size = self.get_window_size()
        width = size.get('width')
        height = size.get('height')
        time_start = time.time()
        x = width / 2
        y_start = height * (1 + rate) / 2
        y_end = height * (1 - rate) / 2
        while timeout > time.time() - time_start:
            try:
                if id:
                    ele = self.find_element_by_id(id, timeout=3)
                    return ele
                else:
                    ele = self.find_element_by_xpath(xpath, timeout=3)
                    return ele
            except:
                self.swipe(x, y_start, x, y_end)
                time.sleep(3)
                continue
        else:
            g_logger.warning("向下滑动查找元素，未找到")
            return None

    def swipe_ele(self, swipe_xpath=None, swipe_id=None, rate=0.5, direction="up", timeout=10):
        try:
            start_x, start_y, end_x, end_y = self.get_ele_swpie_coordinate(swipe_xpath=swipe_xpath, swipe_id=swipe_id, rate=rate, direction=direction, timeout=timeout)
        except:
            g_logger.error("没有找到定位坐标的滑动元素")
            return False
        self.swipe(int(start_x), int(start_y), int(end_x), int(end_y))
        time.sleep(3)
        return True

    def swipe_ele_find_ele(self, swipe_xpath=None, find_xpath=None, swipe_id=None, find_id=None, rate=0.5, direction="up", stable_ele=False, stable_time=20, timeout=30):
        """
        通过滑动元素方式查找元素
        Args:
            swipe_xpath: 滑动的元素的xpath
            find_xpath: 查找元素的xpath
            swipe_id: 滑动的元素的id
            find_id: 查找元素的id
            rate: 滑动幅度（比例）
            direction: 滑动方向 up,down,left,right
            stable_ele: 是否稳定查找元素
            stable_time: 稳定元素超时时间
            timeout: 元素查找超时参数

        Returns:
            ele: 滑动找到元素， None：未找到元素或者参数错误
        """
        # 确认目标元素查找方式
        if find_xpath:
            look_style = "xpath"
        elif find_id:
            look_style = "id"
        else:
            g_logger.error("没有找到find_xpath或者find_id参数, 请输入一个参数")
            return None
        # 查找滑动的元素
        try:
            start_x, start_y, end_x, end_y = self.get_ele_swpie_coordinate(swipe_xpath=swipe_xpath, swipe_id=swipe_id, rate=rate, direction=direction, timeout=10)
        except:
            g_logger.error("没有找到定位坐标的滑动元素")
            return None
        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                if look_style == "xpath":
                    if stable_ele:
                        self.stable_element(xpath=find_xpath, timeout=stable_time)
                    ele = self.find_element_by_xpath(find_xpath, timeout=2)
                else:
                    if stable_ele:
                        self.stable_element(id=find_id, timeout=stable_time)
                    ele = self.find_element_by_id(find_id, timeout=2)
                time.sleep(2)
                return ele
            except Exception as e:
                self.swipe(int(start_x), int(start_y), int(end_x), int(end_y))
                time.sleep(1)

        return None

    def stable_element(self, xpath=None, id=None, timeout=30):
        """
        确认元素是稳定的，返回元素
        Args:
            xpath: 查找元素的xpath
            id: 查找元素的id
            timeout: 超时
        Returns:
            ele: 元素， False: 查找失败
        """
        if not xpath and not id:
            g_logger.error("函数：_stable_element，请输入xpath或者id")
            return False
        last_location = None
        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                if xpath:
                    ele = self.find_element_by_xpath(xpath, timeout=5)
                else:
                    ele = self.find_element_by_id(id, timeout=5)
                if ele.location == last_location:
                    return ele
                else:
                    last_location = ele.location
                time.sleep(3)
            except:
                pass
        return False

    def get_ele_swpie_coordinate(self, swipe_xpath=None, swipe_id=None, rate=0.5, direction="up", timeout=30):
        """
        获取待滑动元素的坐标位置
        Args:
            swipe_xpath: 查找滑动元素的xpath
            swipe_id: 查找滑动元素的id
            rate: 滑动比例
            direction: 滑动方向
            timeout: 超时
        Exception:
            未找到滑动元素
        Returns:
            元素边界坐标
        """
        if swipe_xpath:
            swipe_ele = self.find_element_by_xpath(swipe_xpath, timeout=timeout)
        elif swipe_id:
            swipe_ele = self.find_element_by_id(swipe_id, timeout=timeout)
        else:
            g_logger.error("没有找到swipe_xpath或者swipe_id参数, 请输入一个参数")
            return None
        x, y = swipe_ele.location['x'], swipe_ele.location['y']
        width, height = swipe_ele.size['width'], swipe_ele.size['height']
        start_x = x + width / 2 if direction in ("up", "down") else x + width * (1 + rate) / 2 if direction == "left" else x + width * (1 - rate) / 2
        end_x = x + width / 2 if direction in ("up", "down") else x + width * (1 + rate) / 2 if direction == "right" else x + width * (1 - rate) / 2
        start_y = y + height / 2 if direction in ("left", "right") else y + height * (1 + rate) / 2 if direction == "up" else y + height * (1 - rate) / 2
        end_y = y + height / 2 if direction in ("left", "right") else y + height * (1 + rate) / 2 if direction == "down" else y + height * (1 - rate) / 2

        return start_x, start_y, end_x, end_y

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

    def swipe_screen(self, rate=0.4, direction='up', duration=1, sleep_time=2):
        """
        滑动屏幕
        Args:
            rate: 滑动比例
            direction: 滑动方向，取值: "up", "down", "left", "right"
            duration: 滑动时长, 秒
            sleep_time: 滑动后等待时间
        """
        if not self._window_size:
            size = self.get_window_size()
            self._window_size = {'width': size.get('width'), 'height': size.get('height')}
        width = self._window_size.get('width')
        height = self._window_size.get('height')
        start_x = width / 2 if direction in ("up", "down") else width * (1 + rate) / 2 if direction == "left" else width * (1 - rate) / 2
        end_x = width / 2 if direction in ("up", "down") else width * (1 + rate) / 2 if direction == "right" else width * (1 - rate) / 2
        start_y = height / 2 if direction in ("left", "right") else height * (1 + rate) / 2 if direction == "up" else height * (1 - rate) / 2
        end_y = height / 2 if direction in ("left", "right") else height * (1 + rate) / 2 if direction == "down" else height * (1 - rate) / 2

        self.swipe(int(start_x), int(start_y), int(end_x), int(end_y), duration=duration)
        if sleep_time:
            time.sleep(sleep_time)
        return True

    def get_texts_between_xpath(self, find_xpath, start_xpath, end_xpath, rate=0.3, timeout=120):
        """
        获取文本信息，从两个元素之间
        Args:
            find_xpath: 带查找文本的元素xpath
            start_xpath: 开始标志元素xpath
            end_xpath:  结束标志元素xpath
            rate: 滑动比例
            timeout: 超时

        Returns:
            list: 查找到的文本列表，False: 查找失败
        """
        if not self.swipe_down_find_ele(xpath=start_xpath, timeout=timeout):
            g_logger.warning("查找开始元素失败")
            return False

        find_text = []
        size = self.get_window_size()
        width = size.get('width')
        height = size.get('height')
        x = width / 2
        y_start = height * (1 + rate) / 2
        y_end = height * (1 - rate) / 2
        time_start = time.time()
        while timeout > time.time() - time_start:
            eles = self.find_elements_by_xpath(find_xpath, timeout=3)
            if eles:
                find_text.extend([ele.get_attribute("text") for ele in eles])
            try:
                self.find_element_by_xpath(end_xpath, timeout=3)
                break
            except:
                self.swipe(x, y_start, x, y_end)
                time.sleep(2)
        else:
            g_logger.warning("查找结束元素超时")
            return False

        find_order_list = list(set(find_text))
        find_order_list.sort(key=find_text.index)
        g_logger.info("查找的的文本：{}".format(",".join(find_order_list)))
        return find_order_list

    def swipe_down_find_text_by_xpath(self, xpaths, rate=0.3, timeout=120):
        return self.swipe_down_xpath_find_eles(xpaths=xpaths, rate=rate, attr='text', timeout=timeout)

    def swipe_down_xpath_find_eles(self, xpaths=None, rate=0.3, attr=None, timeout=120):
        """
        向下滑动查找
        Args:
            xpaths: 待查找xpath列表
            rate: 向下滑动比例
            attr: 查找的元素属性
            timeout: 查找超时
        Returns:
            eles: 查找的元素实例或者实例属性列表
        """
        size = self.get_window_size()
        width = size.get('width')
        height = size.get('height')
        time_start = time.time()
        x = width / 2
        y_start = height * (1 + rate) / 2
        y_end = height * (1 - rate) / 2
        if isinstance(xpaths, str):
            xpath_list = [xpaths]
        else:
            xpath_list = list(xpaths)
        find_xpaths = []
        eles = []
        while timeout > time.time() - time_start:
            for xpath in xpath_list:
                try:
                    ele = self.find_element_by_xpath(xpath, timeout=2)
                    find_xpaths.append(xpath)
                    if attr:
                        eles.append(ele.get_attribute(attr))
                except:
                    pass
            while find_xpaths:
                xpath_list.remove(find_xpaths.pop())
            if not xpath_list:
                break
            self.swipe(x, y_start, x, y_end)
            time.sleep(2)
        g_logger.info("查找到的元素列表：{}".format(",".join(eles)))
        return eles

    def click_textview_text(self, text, swipe=False, timeout=5):
        """
        点击Textview控件的text
        Args:
            text: 待查找的文本
            timeout: 查找超时时间
            swipe: 是否向下滑动查找
        Returns:
            True: 找到此text的TextView,并执行了点击操作，False: 未找到元素
        """
        ele = self.check_textview_text(text, swipe=swipe, timeout=timeout)
        if ele:
            ele.click()
            g_logger.info("点击文本:{} 成功".format(text))
            time.sleep(2)
            return True
        else:
            return False

    def check_textview_texts(self, texts, swipe=False, timeout=10, all=False):
        """
        向下滑动检测多文本
        Args:
            texts: 检测的文本列表
            swipe:
            timeout:
        Returns:
        """
        if isinstance(texts, str):
            text_list = [texts]
        elif isinstance(texts, (tuple, set)):
            text_list = list(texts)
        else:
            text_list = texts.copy()
        time.sleep(3)
        size = self.get_window_size()
        width = size.get('width')
        height = size.get('height')
        order_text = []
        if swipe:
            size = self.get_window_size()
            width = size.get('width')
            height = size.get('height')

        time_start = time.time()
        while time.time() - time_start < timeout:
            find_text = []
            for text in text_list:
                try:
                    ele = self.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(text), timeout=2)
                    find_text.append(text)
                    order_text.append(text)
                    if not all:
                        return ele
                except:
                    pass

            while find_text:
                text_list.remove(find_text.pop())
            if not text_list:
                return order_text

            if swipe:
                self.swipe(width / 2, height * 6 / 10, width / 2, height * 3 / 10)
                time.sleep(2)
        return False

    def check_textview_text(self, text, swipe=False, timeout=5):
        """
        检测Textview控件的text
        Args:
            text: 待查找的文本
            timeout: 查找超时时间
            swipe: 是否向下滑动查找
        Returns:
            ele: 找到此text的TextView,返回元素实例，False: 未找到
        """
        if swipe:
            size = self.get_window_size()
            width = size.get('width')
            height = size.get('height')

        time_start = time.time()
        while time.time() - time_start < timeout:
            try:
                ele = self.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(text), timeout=2)
                return ele
            except:
                if swipe:
                    self.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
                    time.sleep(2)
        return False

    def get_ele_coordinate(self, ele):
        """
        获取元素坐标
        Args:
            ele: 元素实例
        Returns:
            元素左上、右下坐标位置
        """
        x, y = ele.location['x'], ele.location['y']
        ele_w, ele_h = ele.size['width'], ele.size['height']
        return x, y, x+ele_w, y+ele_h



