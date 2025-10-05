import tkinter as tk
from tkinter import  ttk, scrolledtext, messagebox, filedialog, simpledialog
from openai import OpenAI
import datetime
import os
import json


class ChatApp:
    user_name = "蜡笔小新"
    client = OpenAI(api_key="sk-630c9f1c175e432ba610e94c602d7d4c", base_url="https://api.deepseek.com")
    # 2. 定义选项列表
    select_options = [
        "情绪持续低落，对什么都提不起兴趣怎么办？",
        "学习压力大，无法集中注意力，很焦虑。",
        "和父母沟通困难，总吵架，感觉不被理解。",
        "在学校没有朋友，感到孤独和被排挤。",
        "控制不住刷手机，明知影响学习却停不下来。",
        "经常无缘无故感到心慌、紧张，身体不适。",
        "对未来迷茫，不知道自己想做什么，没目标。",
        "很在意别人看法，自卑，害怕当众发言。",
        "晚上睡不着，白天没精神，作息紊乱。",
        "与同学比较后，总觉得自己很差，很痛苦。"
    ]
    selected_option = ""
    chat_history = []

    def __init__(self, root):
        self.root = root
        self.root.title("情绪魔方")
        self.root.geometry("980x760")
        self.root.resizable(True, True)

        # 设置样式
        self.setup_styles()

        # 创建界面
        self.create_interface()

    def setup_styles(self):
        """定义样式颜色"""
        self.colors = {
            'primary': '#3498DB',
            'secondary': '#2C3E50',
            'success': '#27AE60',
            'danger': '#E74C3C',
            'warning': '#F39C12',
            'light': '#ECF0F1',
            'dark': '#34495E',
            'background': '#1A252F'
        }

    def create_interface(self):
        """创建主界面"""
        # 主容器
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 标题
        title_frame = self.create_title_frame(main_container)
        title_frame.pack(fill=tk.X, pady=(0, 10))

        # 内容区域
        content_frame = tk.Frame(main_container, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧控制面板
        control_frame = self.create_control_panel(content_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # 右侧聊天区域
        chat_frame = self.create_chat_area(content_frame)
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_title_frame(self, parent):
        """创建标题框架"""
        frame = tk.Frame(parent, bg=self.colors['dark'], relief=tk.RAISED, bd=2)

        title = tk.Label(
            frame,
            text="💬 欢迎来到情绪魔方，请输入或选择你的问题",
            font=("Arial", 20, "bold"),
            bg=self.colors['dark'],
            fg='white',
            pady=5
        )
        title.pack()

        return frame

    def create_control_panel(self, parent):
        """创建控制面板"""
        frame = tk.Frame(parent, bg=self.colors['dark'], relief=tk.RAISED, bd=2, width=200)
        frame.pack_propagate(False)  # 保持固定宽度

        # 用户信息
        user_frame = tk.Frame(frame, bg=self.colors['dark'])
        user_frame.pack(fill=tk.X, padx=10, pady=10)

        user_icon = tk.Label(
            user_frame,
            text="👤",
            font=("Arial", 24),
            bg=self.colors['dark'],
            fg='white'
        )
        user_icon.pack()

        user_name = tk.Label(
            user_frame,
            text=self.user_name,
            font=("Arial", 12, "bold"),
            bg=self.colors['dark'],
            fg='white'
        )
        user_name.pack(pady=5)

        # 功能按钮
        buttons_frame = tk.Frame(frame, bg=self.colors['dark'])
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)

        buttons = [
            ("🎨 用户登录", self.user_login),
            ("💾 保存聊天", self.save_chat),
            ("📥 加载聊天", self.load_chat),
            ("🧹 清空聊天", self.clear_chat),
            ("ℹ️  关于", self.show_about)
        ]

        for text, command in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                font=("Arial", 10),
                bg=self.colors['primary'],
                fg='white',
                relief=tk.FLAT,
                bd=0,
                pady=8
            )
            btn.pack(fill=tk.X, pady=2)

        return frame

    def create_chat_area(self, parent):
        """创建聊天区域"""
        chat_frame = tk.Frame(parent, bg=self.colors['background'])

        # 聊天显示区域
        display_frame = tk.Frame(chat_frame, bg=self.colors['light'], relief=tk.SUNKEN, bd=2)
        display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.chat_display = scrolledtext.ScrolledText(
            display_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg='white',
            fg=self.colors['dark'],
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.chat_display.config(state=tk.DISABLED)

        # 输入区域
        input_frame = tk.Frame(chat_frame, bg=self.colors['light'], relief=tk.SUNKEN, bd=2)
        input_frame.pack(fill=tk.X)

        # 输入框
        self.input_text = tk.Text(
            input_frame,
            wrap=tk.WORD,
            height=2,
            font=("Arial", 11),
            bg='white',
            fg=self.colors['dark'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 预设问题选择框
        self.selected_option = tk.StringVar()
        combo_box = ttk.Combobox(
            chat_frame,
            font=("Arial", 11),
            textvariable=self.selected_option,
            values=self.select_options,
            state="readonly"  # 设置为只读，用户不能自己输入
        )

        combo_box.pack(fill=tk.X)
        combo_box.set("请选择")
        combo_box.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # 按钮区域
        button_frame = tk.Frame(chat_frame, bg=self.colors['light'])
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        self.send_button = tk.Button(
            button_frame,
            text="发送 📤",
            command=self.send_message,
            font=("Arial", 11, "bold"),
            bg=self.colors['success'],
            fg='white',
            relief=tk.RAISED,
            bd=2,
            width=8,
            pady=8
        )
        self.send_button.pack(fill=tk.X, pady=2)

        # 绑定快捷键
        self.input_text.bind('<Control-Return>', lambda e: self.send_message())

        # 添加欢迎消息
        self.add_message("系统", "你好！" + self.user_name + ", 欢迎来到情绪魔方!")

        return chat_frame

    def send_message(self):
        """发送消息"""
        message = self.input_text.get("1.0", tk.END).strip()

        if not message:
            messagebox.showwarning("输入为空", "请输入消息内容")
            return

        self.add_message(self.user_name, message)
        self.input_text.delete("1.0", tk.END)
        self.send_to_ai(message)

    def add_message(self, sender, message):
        """添加消息"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        self.chat_display.config(state=tk.NORMAL)

        # 根据发送者设置不同的样式
        if sender == "系统":
            prefix = f"[{timestamp}] ⚙️  {sender}: "
            tag_prefix = "system"
        elif sender == "情绪导师":
            prefix = f"[{timestamp}] 🤖 {sender}: "
            tag_prefix = "ai"
        else:
            prefix = f"[{timestamp}] 👤 {sender}: "
            tag_prefix = "user"

        self.chat_display.insert(tk.END, prefix, f"{tag_prefix}_tag")
        self.chat_display.insert(tk.END, f"{message}\n\n", f"{tag_prefix}_message")

        # 配置样式
        self.chat_display.tag_config("user_tag", foreground=self.colors['primary'], font=("Arial", 10, "bold"))
        self.chat_display.tag_config("user_message", foreground=self.colors['dark'])

        self.chat_display.tag_config("ai_tag", foreground=self.colors['success'], font=("Arial", 10, "bold"))
        self.chat_display.tag_config("ai_message", foreground=self.colors['dark'])

        self.chat_display.tag_config("system_tag", foreground=self.colors['warning'], font=("Arial", 10, "bold"))
        self.chat_display.tag_config("system_message", foreground=self.colors['dark'])

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

        # 保存到历史
        self.chat_history.append({
            "sender": sender,
            "message": message,
            "timestamp": timestamp
        })

    def send_to_ai(self, user_message):
        response = self.client.chat.completions.create(model="deepseek-chat", messages=[
            {"role": "system", "content": "你是一位陪聊，请自然地回复用户，并尝试使其心情变好。"},
            {"role": "user","content": "（若用户在接下来的内容中表现出自残、自杀、暴力倾向或无法控制情绪等情况，请为其提供专业帮助渠道，若无请忽略括号内的内容）" + user_message},
        ],stream=False)
        answer = response.choices[0].message.content
        self.add_message("情绪导师", answer)

    def user_login(self):
        """用户登录"""
        # 弹出输入对话框
        name = simpledialog.askstring("输入名字", "请输入您的名字:", initialvalue="蜡笔小新")  # 可选：默认值
        if name:
            self.user_name = name
            self.add_message("系统", "你好！" + self.user_name + ", 欢迎来到情绪魔方")

    # 5. 绑定事件：当选择改变时自动触发（可选，但很实用）
    def on_combobox_select(self, event):
        selection = self.selected_option.get()
        self.input_text.insert("1.0", selection)

    def save_chat(self):
        """保存聊天记录"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.chat_history, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", "聊天记录已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")

    def load_chat(self):
        """加载聊天记录"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    history = json.load(f)

                # 清空当前显示
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.delete("1.0", tk.END)

                # 加载历史消息
                for item in history:
                    self.add_message(item['sender'], item['message'])

                messagebox.showinfo("成功", "聊天记录已加载！")
        except Exception as e:
            messagebox.showerror("错误", f"加载失败: {e}")

    def clear_chat(self):
        """清空聊天记录"""
        if messagebox.askyesno("确认", "确定要清空所有聊天记录吗？"):
            self.chat_history = []
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.add_message("系统", "聊天记录已清空")

    def show_about(self):
        """显示关于信息"""
        about_text = """
            情绪魔方：专注于为青少年提供心理咨询服务，由AI给出专业回答
            功能特点:
            ✅ 无需外部依赖
            ✅ 美观的现代界面
            ✅ 支持用户自己输入问题
            ✅ 支持预设问题一键导入           
            ✅ 聊天记录保存
            ✅ 聊天记录加载
            ✅ 聊天记录清空
            
            使用说明:
            1. 在下方输入问题或选择预设问题
            2. 点击发送
            3. 使用左侧面板管理聊天
        """
        messagebox.showinfo("关于", about_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()