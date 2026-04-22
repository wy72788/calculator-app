# calculator_kivy
# 手机计算器 - Kivy版本

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex

# 设置窗口大小（开发测试用，打包到手机后自动全屏）
Window.size = (400, 600)


class CalculatorDisplay(Label):
    """计算器显示屏 - 继承自Label"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '50sp'
        self.size_hint_y = 0.25
        self.text = '0'
        self.color = (1, 1, 1, 1)  # 白色文字
        self.valign = 'bottom'
        self.halign = 'right'
        self.padding = (10, 10)
    
    def on_size(self, *args):
        """当控件大小改变时，更新文字位置"""
        self.text_size = (self.width, self.height)


class CalculatorButton(Button):
    """自定义计算器按钮 - 继承自Button"""
    def __init__(self, text, bg_color, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = '24sp'
        self.background_color = bg_color
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.border_radius = [20]
        
        # 绑定按下和释放事件实现悬停效果
        self.bind(on_press=self.on_press_button)
        self.bind(on_release=self.on_release_button)
    
    def on_press_button(self, instance):
        """按下时变暗"""
        instance.background_color = (
            instance.background_color[0] * 0.8,
            instance.background_color[1] * 0.8,
            instance.background_color[2] * 0.8,
            1
        )
    
    def on_release_button(self, instance):
        """释放时恢复原色"""
        instance.background_color = self.original_color
    
    def set_original_color(self, color):
        """保存原始颜色"""
        self.original_color = color


class CalculatorLayout(GridLayout):
    """计算器主布局 - 继承自GridLayout"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.spacing = 2
        self.padding = 2
        
        # 状态变量
        self.expression = ""      # 存储表达式
        self.new_input = True     # 是否新输入
        self.result_shown = False # 是否刚显示结果
        
        # 颜色定义（十六进制转RGB）
        self.colors = {
            'display': get_color_from_hex('#1e1e1e'),
            'button': get_color_from_hex('#3c3f41'),
            'operator': get_color_from_hex('#ff9500'),
            'clear': get_color_from_hex('#a33b2c'),
            'equal': get_color_from_hex('#ff9500'),
            'bg': get_color_from_hex('#2d2d2d'),
        }
        
        # 创建界面
        self.create_display()
        self.create_buttons()
    
    def create_display(self):
        """创建显示屏"""
        self.display = CalculatorDisplay()
        self.add_widget(self.display)
    
    def create_buttons(self):
        """创建按钮区域"""
        buttons_grid = GridLayout(
            cols=4,
            spacing=2,
            size_hint_y=0.75
        )
        
        # 按钮定义（文本, 背景色键）
        buttons = [
            ('C', 'clear'), ('±', 'button'), ('%', 'button'), ('÷', 'operator'),
            ('7', 'button'), ('8', 'button'), ('9', 'button'), ('×', 'operator'),
            ('4', 'button'), ('5', 'button'), ('6', 'button'), ('-', 'operator'),
            ('1', 'button'), ('2', 'button'), ('3', 'button'), ('+', 'operator'),
            ('0', 'button'), ('.', 'button'), ('=', 'equal'),
        ]
        
        for text, color_key in buttons:
            # 获取颜色
            bg_color = self.colors[color_key]
            
            # 创建按钮
            btn = CalculatorButton(text, bg_color)
            btn.set_original_color(bg_color)
            
            # 绑定点击事件
            btn.bind(on_release=self.on_button_click)
            
            # 0按钮特殊处理（跨列）
            if text == '0':
                buttons_grid.add_widget(btn)
                # 添加一个空占位符来保持布局
                placeholder = Button(
                    background_color=(0, 0, 0, 0),
                    background_normal='',
                    disabled=True
                )
                buttons_grid.add_widget(placeholder)
            else:
                buttons_grid.add_widget(btn)
        
        self.add_widget(buttons_grid)
    
    def on_button_click(self, instance):
        """按钮点击事件处理"""
        value = instance.text
        
        # 处理不同类型的按钮
        if value == 'C':
            self.clear()
        elif value == '=':
            self.calculate()
        elif value == '±':
            self.negate()
        elif value == '%':
            self.percent()
        else:
            self.add_to_expression(value)
    
    def add_to_expression(self, value):
        """添加到表达式"""
        # 如果刚显示结果，开始新输入
        if self.result_shown:
            self.expression = ""
            self.result_shown = False
        
        if self.new_input:
            self.expression = ""
            self.new_input = False
        
        # 防止连续输入运算符
        if value in ['+', '-', '×', '÷'] and self.expression and self.expression[-1] in ['+', '-', '×', '÷']:
            # 替换最后一个运算符
            self.expression = self.expression[:-1] + value
        else:
            self.expression += value
        
        self.update_display()
    
    def calculate(self):
        """计算表达式结果"""
        try:
            if not self.expression:
                return
            
            # 替换运算符
            expr = self.expression.replace('×', '*').replace('÷', '/')
            
            # 计算
            result = eval(expr)
            
            # 格式化结果
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            # 更新显示
            self.display.text = str(result)
            self.expression = str(result)
            self.new_input = True
            self.result_shown = True
            
        except Exception as e:
            self.display.text = "错误"
            self.expression = ""
            self.new_input = True
            self.result_shown = True
    
    def clear(self):
        """清空"""
        self.expression = ""
        self.display.text = "0"
        self.new_input = True
        self.result_shown = False
    
    def negate(self):
        """取反"""
        try:
            if self.expression:
                num = float(self.expression)
                result = -num
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)
                self.display.text = str(result)
                self.new_input = True
                self.result_shown = True
        except:
            pass
    
    def percent(self):
        """百分比"""
        try:
            if self.expression:
                num = float(self.expression)
                result = num / 100
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)
                self.display.text = str(result)
                self.new_input = True
                self.result_shown = True
        except:
            pass
    
    def update_display(self):
        """更新显示屏"""
        if self.expression:
            self.display.text = self.expression
        else:
            self.display.text = "0"


class CalculatorApp(App):
    """主应用程序类"""
    
    def build(self):
        """构建应用界面"""
        # 设置应用标题
        self.title = "计算器"
        
        # 设置窗口背景色
        from kivy.core.window import Window
        Window.clearcolor = get_color_from_hex('#2d2d2d')
        
        # 返回主布局
        return CalculatorLayout()
    
    def on_start(self):
        """应用启动时调用"""
        print("计算器已启动")


# 程序入口
if __name__ == '__main__':
    CalculatorApp().run()