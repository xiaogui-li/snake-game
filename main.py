#!/usr/bin/env python3
"""
贪吃蛇游戏 - Kivy 版本（支持打包 Android APK）
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.metrics import dp
import random


class SnakeGameWidget(Widget):
    """游戏画布组件"""
    grid_size = NumericProperty(25)
    cols = NumericProperty(24)
    rows = NumericProperty(24)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = []
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = None
        self.score = 0
        self.game_running = False
        self.game_paused = False
        self.speed = 0.1
        self.particles = []
        
        # 颜色
        self.colors = {
            'bg': (0.059, 0.059, 0.102, 1),  # #0f0f1a
            'grid': (0.145, 0.145, 0.22, 1),
            'snake_head': (0.306, 0.8, 0.639, 1),  # #4ecca3
            'snake_body': [(0.271, 0.69, 0.549, 1), (0.239, 0.604, 0.49, 1)],
            'food': (1, 0.42, 0.42, 1),  # #ff6b6b
            'food_glow': (1, 0.52, 0.52, 1),
        }
        
        # 动画
        self.food_pulse = 0
        self.snake_glow = 0
        
        # 绑定尺寸变化
        self.bind(size=self.on_size)
        
    def on_size(self, *args):
        """尺寸变化时重绘"""
        if not self.game_running:
            self.draw_welcome()
        
    def init_game(self):
        """初始化游戏"""
        start_x = self.cols // 2
        start_y = self.rows // 2
        self.snake = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.spawn_food()
        self.particles = []
        
    def spawn_food(self):
        """生成食物"""
        while True:
            x = random.randint(0, int(self.cols) - 1)
            y = random.randint(0, int(self.rows) - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
                
    def start_game(self):
        """开始游戏"""
        self.game_running = True
        self.game_paused = False
        self.init_game()
        Clock.schedule_interval(self.update, self.speed)
        
    def pause_game(self):
        """暂停/继续"""
        if not self.game_running:
            return False
        self.game_paused = not self.game_paused
        if self.game_paused:
            Clock.unschedule(self.update)
        else:
            Clock.schedule_interval(self.update, self.speed)
        return self.game_paused
        
    def restart_game(self):
        """重新开始"""
        self.game_running = False
        self.game_paused = False
        Clock.unschedule(self.update)
        self.draw_welcome()
        
    def stop_game(self):
        """停止游戏"""
        Clock.unschedule(self.update)
        
    def update(self, dt):
        """游戏更新"""
        if self.game_paused:
            return
            
        self.direction = self.next_direction
        
        head_x, head_y = self.snake[0]
        
        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)
            
        # 碰撞检测
        if (new_head[0] < 0 or new_head[0] >= self.cols or 
            new_head[1] < 0 or new_head[1] >= self.rows):
            self.game_over()
            return
            
        if new_head in self.snake:
            self.game_over()
            return
            
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 10
            self.create_particles(new_head[0], new_head[1])
            self.spawn_food()
            # 通知外部更新分数
            if hasattr(self.parent, 'update_score'):
                self.parent.update_score(self.score)
        else:
            self.snake.pop()
            
        # 更新动画
        self.food_pulse = (self.food_pulse + 0.15) % (3.14159 * 2)
        self.snake_glow = (self.snake_glow + 0.1) % (3.14159 * 2)
        
        self.draw()
        
    def create_particles(self, x, y):
        """创建粒子效果"""
        for _ in range(6):
            self.particles.append({
                'x': x + 0.5, 'y': y + 0.5,
                'vx': random.uniform(-0.3, 0.3),
                'vy': random.uniform(-0.3, 0.3),
                'life': 1.0,
            })
            
    def update_particles(self):
        """更新粒子"""
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.05
            if p['life'] <= 0:
                self.particles.remove(p)
                
    def draw(self):
        """绘制游戏"""
        self.canvas.clear()
        
        cell_w = self.width / self.cols
        cell_h = self.height / self.rows
        
        with self.canvas:
            # 背景
            Color(*self.colors['bg'])
            Rectangle(pos=self.pos, size=self.size)
            
            # 网格点
            Color(*self.colors['grid'])
            for x in range(0, int(self.cols), 2):
                for y in range(0, int(self.rows), 2):
                    Rectangle(
                        pos=(self.x + x * cell_w, self.y + y * cell_h),
                        size=(dp(2), dp(2))
                    )
            
            # 食物
            if self.food:
                x, y = self.food
                cx = self.x + x * cell_w + cell_w / 2
                cy = self.y + y * cell_h + cell_h / 2
                
                # 光晕
                pulse = 1 + 0.2 * (1 + (self.food_pulse % (3.14159 * 2)) / 3.14159 - 1)
                glow_size = cell_w * pulse
                Color(*self.colors['food_glow'])
                Line(
                    ellipse=[cx - glow_size/2, cy - glow_size/2, glow_size, glow_size],
                    width=2
                )
                
                # 食物本体
                Color(*self.colors['food'])
                Ellipse(
                    pos=(self.x + x * cell_w + 3, self.y + y * cell_h + 3),
                    size=(cell_w - 6, cell_h - 6)
                )
            
            # 蛇
            for i, (x, y) in enumerate(self.snake):
                if i == 0:
                    Color(*self.colors['snake_head'])
                    size = cell_w - 2
                    Ellipse(
                        pos=(self.x + x * cell_w + 1, self.y + y * cell_h + 1),
                        size=(size, size)
                    )
                else:
                    color_idx = min(i // 3, len(self.colors['snake_body']) - 1)
                    Color(*self.colors['snake_body'][color_idx])
                    size = cell_w - 4
                    Ellipse(
                        pos=(self.x + x * cell_w + 2, self.y + y * cell_h + 2),
                        size=(size, size)
                    )
            
            # 粒子
            self.update_particles()
            for p in self.particles:
                alpha = p['life']
                Color(1, 0.42, 0.42, alpha)
                size = dp(4) * p['life']
                Ellipse(
                    pos=(self.x + p['x'] * cell_w - size/2, 
                         self.y + p['y'] * cell_h - size/2),
                    size=(size, size)
                )
                
    def draw_welcome(self):
        """绘制欢迎画面"""
        self.canvas.clear()
        
        with self.canvas:
            Color(*self.colors['bg'])
            Rectangle(pos=self.pos, size=self.size)
            
    def draw_pause(self):
        """绘制暂停画面"""
        with self.canvas:
            Color(0, 0, 0, 0.5)
            Rectangle(pos=self.pos, size=self.size)
            
    def draw_game_over(self):
        """绘制游戏结束"""
        with self.canvas:
            Color(0.04, 0.04, 0.07, 0.9)
            Rectangle(pos=self.pos, size=self.size)
            
    def game_over(self):
        """游戏结束"""
        self.game_running = False
        Clock.unschedule(self.update)
        self.draw_game_over()
        if hasattr(self.parent, 'game_over'):
            self.parent.game_over(self.score)
            
    def on_touch_move(self, touch):
        """处理滑动控制"""
        if not self.game_running or self.game_paused:
            return
            
        if hasattr(touch, 'dx') and hasattr(touch, 'dy'):
            dx = touch.dx
            dy = touch.dy
            
            if abs(dx) > abs(dy):
                if dx > 0 and self.direction != "Left":
                    self.next_direction = "Right"
                elif dx < 0 and self.direction != "Right":
                    self.next_direction = "Left"
            else:
                if dy > 0 and self.direction != "Up":
                    self.next_direction = "Down"
                elif dy < 0 and self.direction != "Down":
                    self.next_direction = "Up"
                
    def set_difficulty(self, diff):
        """设置难度"""
        speeds = {
            'easy': 0.15,
            'normal': 0.1,
            'hard': 0.07,
            'insane': 0.05
        }
        self.speed = speeds.get(diff, 0.1)


class SnakeAppLayout(BoxLayout):
    """主应用布局"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        
        # 标题栏
        title = Label(
            text='🐍 贪吃蛇',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(50),
            color=(0.306, 0.8, 0.639, 1)
        )
        self.add_widget(title)
        
        # 分数显示
        self.score_layout = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(20)
        )
        
        self.score_label = Label(
            text='分数: 0',
            font_size=dp(20),
            color=(1, 1, 1, 1)
        )
        self.high_score_label = Label(
            text='最高分: 0',
            font_size=dp(16),
            color=(0.5, 0.5, 0.6, 1)
        )
        
        self.score_layout.add_widget(self.score_label)
        self.score_layout.add_widget(self.high_score_label)
        self.add_widget(self.score_layout)
        
        # 游戏区域
        self.game_widget = SnakeGameWidget()
        self.add_widget(self.game_widget)
        
        # 控制按钮
        control_layout = GridLayout(
            cols=4,
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        self.start_btn = Button(
            text='▶ 开始',
            background_color=(0.306, 0.8, 0.639, 1),
            background_normal=''
        )
        self.start_btn.bind(on_press=self.on_start)
        
        self.pause_btn = Button(
            text='⏸ 暂停',
            background_color=(0.2, 0.2, 0.3, 1),
            background_normal=''
        )
        self.pause_btn.bind(on_press=self.on_pause)
        self.pause_btn.disabled = True
        
        self.restart_btn = Button(
            text='↻ 重来',
            background_color=(0.2, 0.2, 0.3, 1),
            background_normal=''
        )
        self.restart_btn.bind(on_press=self.on_restart)
        
        control_layout.add_widget(self.start_btn)
        control_layout.add_widget(self.pause_btn)
        control_layout.add_widget(self.restart_btn)
        
        self.add_widget(control_layout)
        
        # 难度选择
        diff_layout = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            spacing=dp(5)
        )
        
        diff_layout.add_widget(Label(
            text='难度:',
            size_hint_x=None,
            width=dp(60),
            color=(0.7, 0.7, 0.8, 1)
        ))
        
        self.diff_group = []
        difficulties = [
            ('简单', 'easy', (0.306, 0.8, 0.639, 1)),
            ('普通', 'normal', (0.945, 0.769, 0.059, 1)),
            ('困难', 'hard', (0.902, 0.494, 0.133, 1)),
            ('地狱', 'insane', (0.906, 0.298, 0.235, 1))
        ]
        
        for text, value, color in difficulties:
            btn = ToggleButton(
                text=text,
                group='difficulty',
                background_color=color if value == 'normal' else (0.2, 0.2, 0.3, 1),
                background_normal='',
                state='down' if value == 'normal' else 'normal'
            )
            btn.bind(on_press=lambda x, v=value: self.on_difficulty(v))
            diff_layout.add_widget(btn)
            self.diff_group.append((btn, value, color))
            
        self.add_widget(diff_layout)
        
        # 最高分
        self.high_score = 0
        
        # 键盘绑定
        Window.bind(on_key_down=self.on_key_down)
        
    def on_start(self, instance):
        self.game_widget.start_game()
        self.start_btn.disabled = True
        self.start_btn.text = '进行中...'
        self.pause_btn.disabled = False
        
    def on_pause(self, instance):
        paused = self.game_widget.pause_game()
        instance.text = '▶ 继续' if paused else '⏸ 暂停'
        
    def on_restart(self, instance):
        self.game_widget.restart_game()
        self.start_btn.disabled = False
        self.start_btn.text = '▶ 开始'
        self.pause_btn.disabled = True
        self.pause_btn.text = '⏸ 暂停'
        self.score_label.text = '分数: 0'
        
    def on_difficulty(self, value):
        self.game_widget.set_difficulty(value)
        for btn, val, color in self.diff_group:
            if val == value:
                btn.background_color = color
            else:
                btn.background_color = (0.2, 0.2, 0.3, 1)
                
    def update_score(self, score):
        self.score_label.text = f'分数: {score}'
        
    def game_over(self, score):
        if score > self.high_score:
            self.high_score = score
            self.high_score_label.text = f'最高分: {score}'
        self.start_btn.disabled = False
        self.start_btn.text = '▶ 开始'
        self.pause_btn.disabled = True
        
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        """键盘控制"""
        if not self.game_widget.game_running:
            if key == 32:  # 空格
                self.on_start(None)
            return
            
        if key == 273 or key == 119:  # 上 / W
            if self.game_widget.direction != "Down":
                self.game_widget.next_direction = "Up"
        elif key == 274 or key == 115:  # 下 / S
            if self.game_widget.direction != "Up":
                self.game_widget.next_direction = "Down"
        elif key == 276 or key == 97:  # 左 / A
            if self.game_widget.direction != "Right":
                self.game_widget.next_direction = "Left"
        elif key == 275 or key == 100:  # 右 / D
            if self.game_widget.direction != "Left":
                self.game_widget.next_direction = "Right"
        elif key == 32:  # 空格
            self.on_pause(self.pause_btn)
        elif key == 114:  # R
            self.on_restart(None)


class SnakeApp(App):
    """Kivy 应用主类"""
    def build(self):
        Window.clearcolor = (0.059, 0.059, 0.102, 1)
        return SnakeAppLayout()


if __name__ == '__main__':
    SnakeApp().run()
