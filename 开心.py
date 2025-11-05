import tkinter as tk
import random
import math

# ---------- 分享链接（可在微信中打开） ----------
# LOCAL_HTML_PATH 仅在本机可直接打开（file://），
# PUBLIC_HTML_URL 在你把 `开心.html` 上传到 Gist 或 GitHub Pages 后替换为公网 HTTPS 链接，微信可直接打开。
LOCAL_HTML_PATH = r"file:///d:/a/Test/Python/开心.html"
PUBLIC_HTML_URL = "https://your-public-url.example/kaixin.html"  # 上传后替换为真实链接

def print_share_links():
    """打印分享用的本地和公网链接（可在命令行运行或由程序调用）。"""
    print("本地文件（仅本机可打开）：", LOCAL_HTML_PATH)
    print("公网访问链接（微信打开）：", PUBLIC_HTML_URL)

# 调度与卡片参数
SPAWN_INTERVAL_MS = 80
CARD_WIDTH = 200
CARD_HEIGHT = 100
TEXT_FONT = ("楷体", 14)

# 外观参数
LAST_CARD_TEXT = "訾家乐❤谢苗苗"
TRANSPARENT_COLOR = "#00ff00"  # 用于窗口透明的遮罩色（Windows 支持）
CARD_RADIUS = 14
BORDER_COLOR = "white"
BORDER_WIDTH = 6
PADDING = 8
SHADOW_COLOR = "#000000"
SHADOW_OFFSET_X = 6
SHADOW_OFFSET_Y = 6
SHADOW_ALPHA = 0.18
TOP_EXTRA_MARGIN = 30  # 扩大卡片顶部留白
SHADOW_LAYERS = 4      # 多层阴影以更柔和
SHADOW_SPREAD = 5      # 每层向外扩散的像素，稍微扩大


def generate_heart_points(num_points=200):
    points = []
    for i in range(num_points):
        t = (i / num_points) * 2 * math.pi
        x = 16 * (math.sin(t) ** 3)
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        points.append((x, y))
    return points

def _hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

def _blend_hex(c1, c2, t):
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return _rgb_to_hex(r, g, b)


def draw_round_rect(canvas, x1, y1, x2, y2, r, fill, outline, width, border=True):
    # 限制圆角半径在合法范围
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    # 填充主体
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill, outline="")
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill, outline="")
    # 四角扇形填充
    canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, style='pieslice', fill=fill, outline="")
    canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, style='pieslice', fill=fill, outline="")
    canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, style='pieslice', fill=fill, outline="")
    canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, style='pieslice', fill=fill, outline="")
    if border:
        # 白色外边框（直线 + 四角弧线）
        canvas.create_line(x1 + r, y1, x2 - r, y1, fill=outline, width=width)
        canvas.create_line(x1 + r, y2, x2 - r, y2, fill=outline, width=width)
        canvas.create_line(x1, y1 + r, x1, y2 - r, fill=outline, width=width)
        canvas.create_line(x2, y1 + r, x2, y2 - r, fill=outline, width=width)
        canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, style='arc', outline=outline, width=width)
        canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, style='arc', outline=outline, width=width)
        canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, style='arc', outline=outline, width=width)
        canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, style='arc', outline=outline, width=width)

def create_card(root, x, y, screen_width, screen_height, tip_override=None):
    # 使用 Toplevel，而不是为每个卡片创建新的 Tk 实例
    # 阴影窗口分组（2 个窗口模拟羽化，降低窗口数量以提升性能）
    shadow_groups = []
    alphas = [SHADOW_ALPHA] if SHADOW_LAYERS <= 1 else [SHADOW_ALPHA, max(0.06, SHADOW_ALPHA * 0.5)]
    for a in alphas:
        s = tk.Toplevel(root)
        s.overrideredirect(True)
        s.attributes('-topmost', True)
        try:
            s.configure(bg=TRANSPARENT_COLOR)
            s.attributes('-transparentcolor', TRANSPARENT_COLOR)
            s.attributes('-alpha', a)
        except Exception:
            pass
        shadow_groups.append(s)

    # 卡片窗口（在上层）
    win = tk.Toplevel(root)
    win.overrideredirect(True)
    win.attributes('-topmost', True)
    # 透明背景以实现圆角外观
    try:
        win.configure(bg=TRANSPARENT_COLOR)
        win.attributes('-transparentcolor', TRANSPARENT_COLOR)
    except Exception:
        # 某些平台不支持透明色，继续以矩形绘制
        pass

    scale = min(screen_width, screen_height) / 40
    pos_x = int(screen_width / 2 + x * scale - CARD_WIDTH / 2)
    pos_y = int(screen_height / 2 + y * scale - CARD_HEIGHT / 2)
    pos_x = max(0, min(pos_x, screen_width - CARD_WIDTH))
    pos_y = max(0, min(pos_y, screen_height - CARD_HEIGHT))
    # 布局：每组阴影使用其最大扩散尺寸
    mid = SHADOW_LAYERS // 2
    group_ranges = [(0, max(0, mid - 1)), (mid, SHADOW_LAYERS - 1)] if SHADOW_LAYERS > 1 else [(0, 0)]
    for idx, s in enumerate(shadow_groups):
        start, end = group_ranges[idx]
        max_pad = end * SHADOW_SPREAD
        sw = CARD_WIDTH + 2 * max_pad
        sh = CARD_HEIGHT + 2 * max_pad
        s.geometry(f"{sw}x{sh}+{pos_x + SHADOW_OFFSET_X - max_pad}+{pos_y + SHADOW_OFFSET_Y - max_pad}")
    win.geometry(f"{CARD_WIDTH}x{CARD_HEIGHT}+{pos_x}+{pos_y}")

    tips = [
        "多喝水哦~",
        "保持微笑呀",
        "每天都要元气满满",
        "记得吃水果，保持好心情，好好爱自己",
        "我想你了",
        "梦想成真",
        "期待下一次见面",
        "金榜题名",
        "顺顺利利，早点休息",
        "愿所有烦恼都消失",
        "别熬夜",
        "今天过得开心嘛",
        "天冷了，多穿衣服",
        "今日份好运已送达",
        "去点喜欢的歌吧",
        "记得做拉伸，保护颈椎",
        "深呼吸，放轻松",
        "把小事做好，日子会发光",
        "写下一个小目标",
        "喝杯热茶温暖一下",
        "阳光正好，笑一个",
        "你已经很棒了",
        "别和自己较劲",
        "休息五分钟，继续加油",
        "保持专注，效率翻倍",
        "整理桌面，心情也清爽",
        "适度运动，能量满满",
        "相信自己，万事可期",
        "顺风顺水，心想事成",
        "好运常在，福气满满",
        "努力的你很可爱",
        "发条消息给想念的人",
        "今天也要好好吃饭",
        "晚一点也没关系",
        "去窗边看看风景",
        "给自己一个拥抱",
        "把水杯再添满一次",
        "读两页书，充充电",
        "偶尔停下也很好",
        "写下感恩的三件事",
        "别忘了收藏这份温柔",
        "微小但持续的改变",
        "早点睡，做个好梦",
    ]
    bg_color = [
        "lightpink", "skyblue", "lightgreen", "lavender", "lightyellow",
        "plum", "coral", "bisque", "aquamarine", "mistyrose", "honeydew",
        "lavenderblush", "oldlace"
    ]

    tip = tip_override if tip_override is not None else random.choice(tips)
    bg = random.choice(bg_color)

    # 阴影绘制（按组绘制多层扩散）
    for idx, s in enumerate(shadow_groups):
        start, end = group_ranges[idx]
        max_pad = end * SHADOW_SPREAD
        sw = CARD_WIDTH + 2 * max_pad
        sh = CARD_HEIGHT + 2 * max_pad
        cv_s = tk.Canvas(s, width=sw, height=sh, bg=s['bg'], highlightthickness=0, bd=0)
        cv_s.pack(fill='both', expand=True)
        for i in range(start, end + 1):
            pad_i = i * SHADOW_SPREAD
            draw_round_rect(
                cv_s,
                BORDER_WIDTH / 2,
                BORDER_WIDTH / 2,
                sw - BORDER_WIDTH / 2,
                sh - BORDER_WIDTH / 2,
                CARD_RADIUS + pad_i,
                fill=SHADOW_COLOR,
                outline='',
                width=0,
                border=False,
            )

    # 用 Canvas 绘制圆角卡片与白色边框
    cv = tk.Canvas(win, width=CARD_WIDTH, height=CARD_HEIGHT,
                   bg=win['bg'], highlightthickness=0, bd=0)
    cv.pack(fill='both', expand=True)

    # 绘制圆角背景与白色边框
    draw_round_rect(
        cv,
        BORDER_WIDTH / 2,
        BORDER_WIDTH / 2,
        CARD_WIDTH - BORDER_WIDTH / 2,
        CARD_HEIGHT - BORDER_WIDTH / 2,
        CARD_RADIUS,
        fill=bg,
        outline=BORDER_COLOR,
        width=BORDER_WIDTH,
    )

    # 文本居中显示，设置宽度实现自动换行
    cv.create_text(
        CARD_WIDTH / 2,
        CARD_HEIGHT / 2,
        text=tip,
        font=TEXT_FONT,
        fill='black',
        width=CARD_WIDTH - 2 * PADDING,
        justify='center',
        anchor='center'
    )
    # 立即刷新布局，避免文字延迟显示
    win.update_idletasks()
    # 确保卡片在所有阴影之上
    try:
        win.lift()
    except Exception:
        pass


def main():
    # 单一根窗口 + after 调度，避免多线程和多个 mainloop 带来的卡顿与延迟
    root = tk.Tk()
    root.withdraw()  # 隐藏根窗口，只显示卡片

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    points = generate_heart_points(200)

    def spawn(i=0):
        if i >= len(points):
            return
        x, y = points[i]
        # 最后一张卡片显示自定义内容
        tip_override = LAST_CARD_TEXT if i == len(points) - 1 else None
        create_card(root, x, y, screen_width, screen_height, tip_override=tip_override)
        root.after(SPAWN_INTERVAL_MS, lambda: spawn(i + 1))

    spawn(0)
    root.mainloop()


if __name__ == "__main__":
    # 在运行前打印分享链接，便于复制到微信或上传替换 PUBLIC_HTML_URL
    try:
        print_share_links()
    except Exception:
        pass
    main()