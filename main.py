from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import re
import random
import arabic_reshaper

Window.clearcolor = get_color_from_hex('#0d1117')


def fa(t):
    try:
        r = arabic_reshaper.reshape(t)[::-1]
        return re.sub(r'[0-9]+', lambda m: m.group(0)[::-1], r)
    except:
        return t


QUESTIONS = [
    {
        'label': 'نظرت درباره نویسنده چیه؟',
        'impact': 0,
        'happy': ['اگه آخرش خوشحال باشیم، آره!', 'بعضی وقتا فکر می‌کنم نویسنده منو دوست داره.'],
        'neutral': ['همه‌شونو؟ نه بابا!', 'نمی‌دونم. امیدوارم بدونه با زندگی ما بازی می‌کنه.'],
        'sad': ['دلم می‌خواد داد بزنم سر نویسنده!', 'چرا اینقدر سختم کرد؟'],
    },
    {
        'label': 'دوست داری چی تغییر کنه؟',
        'impact': 0,
        'happy': ['هیچی! همه‌چی خوبه.', 'دوست دارم آرش و بابام کنارم باشن.'],
        'neutral': ['کاش یکم راحت‌تر باشه.', 'کاش مجبور نباشم انتخاب کنم.'],
        'sad': ['کاش آدمایی که رفتن، هنوز بودن.', 'کاش زمان برمی‌گشت.'],
    },
    {
        'label': 'نظرت راجع به رفتن از خونه چیه؟',
        'impact': 0,
        'happy': ['دوست دارم! دنیا رو ببینم!', 'هیجان‌انگیزه!'],
        'neutral': ['دوست دارم، ولی نه دور از خانواده.', 'هم هیجان‌انگیزه هم ترسناک.'],
        'sad': ['فکر می‌کردم آزادیه...', 'دلم نمی‌خواد از بابام دور شم.'],
    },
    {
        'label': 'به کی اعتماد داری؟',
        'impact': 1,
        'happy': ['بابام و آرش!', 'به آدمی که بدون حرف می‌فهمه.'],
        'neutral': ['بابام... و آرش.', 'بابام چون همیشه بوده.'],
        'sad': ['نمی‌دونم...', 'اعتماد سخته...'],
    },
    {
        'label': 'اگه آرش و بابا همزمان بهت نیاز داشتن؟',
        'impact': -1,
        'happy': ['راهی پیدا می‌کنم هر دوتاشون رو نجات بدم!'],
        'neutral': ['چرا همچین سؤال بدی؟', 'هیچ‌کدوم رو انتخاب نمی‌کنم.'],
        'sad': ['تا آخر عمر سرزنش می‌کنم خودمو.', 'این سوال منو می‌شکنه...'],
    },
    {
        'label': 'از چی می‌ترسی؟',
        'impact': -1,
        'happy': ['الان؟ هیچی!'],
        'neutral': ['تنها موندن...', 'از دست دادن آدمام.'],
        'sad': ['اینکه دیگه اون ستاره‌ی قبل نباشم.', 'اینکه آرش نباشه.'],
    },
    {
        'label': 'خوشبختی یعنی چی؟',
        'impact': 1,
        'happy': ['خندیدن بدون نگرانی!', 'اینکه خودت باشی.'],
        'neutral': ['کنار آدمایی که دوست داری.', 'یه زندگی آروم.'],
        'sad': ['لحظه‌های کوچیک...', 'نمی‌دونم...'],
    },
    {
        'label': 'اگه یه روز دیگه فرصت داشتی؟',
        'impact': 0,
        'happy': ['هر دوتاشون رو کنار هم جمع می‌کردم!'],
        'neutral': ['آرش رو پیدا می‌کردم.', 'جایی که آرزو داشتم می‌رفتم.'],
        'sad': ['کنار بابام و آرش...'],
    },
    {
        'label': 'آرش چطور آدمیه؟',
        'impact': 1,
        'happy': ['بهترین چیز زندگیمه!', 'مهربونه.'],
        'neutral': ['دلم براش تنگ شده.', 'آدم خاصیه.'],
        'sad': ['می‌ترسم از دستش بدم.', 'کاش پیشم بود.'],
    },
    {
        'label': 'بابا کاوه چطوره؟',
        'impact': 1,
        'happy': ['دنیای منه!', 'بهترین پدر دنیا.'],
        'neutral': ['سخته ولی دلش پاکه.', 'هوامو داره.'],
        'sad': ['می‌ترسم از دستش بدم.', 'کاش بیشتر کنارش بودم.'],
    },
]


class ChatApp(App):
    def build(self):
        self.mood = 0
        root = BoxLayout(orientation='vertical', padding=10, spacing=6)
        
        title = Label(text=fa('ستاره'), font_size='22sp',
                      color=get_color_from_hex('#ffcc33'),
                      size_hint=(1, 0.07))
        root.add_widget(title)
        
        self.mood_label = Label(text=fa('مود: آروم'), font_size='13sp',
                                color=get_color_from_hex('#888888'),
                                size_hint=(1, 0.05))
        root.add_widget(self.mood_label)
        
        self.scroll = ScrollView(size_hint=(1, 0.5))
        self.chat = BoxLayout(orientation='vertical', size_hint_y=None, spacing=6)
        self.chat.bind(minimum_height=self.chat.setter('height'))
        self.scroll.add_widget(self.chat)
        root.add_widget(self.scroll)
        
        btn_scroll = ScrollView(size_hint=(1, 0.38))
        btns = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4)
        btns.bind(minimum_height=btns.setter('height'))
        
        for q in QUESTIONS:
            b = Button(text=fa(q['label']), font_size='13sp',
                       size_hint_y=None, height=45,
                       background_color=get_color_from_hex('#ffcc33'),
                       color=get_color_from_hex('#000000'),
                       background_normal='')
            b.bind(on_press=lambda x, qq=q: self.ask(qq))
            btns.add_widget(b)
        
        btn_scroll.add_widget(btns)
        root.add_widget(btn_scroll)
        
        self.add_msg('ستاره: سلام، یه سوال بزن.')
        return root
    
    def update_mood(self, impact):
        if impact > 0:
            if self.mood >= 0:
                self.mood = min(2, self.mood + 1)
            else:
                self.mood = 1
        elif impact < 0:
            if self.mood <= 0:
                self.mood = max(-2, self.mood - 1)
            else:
                self.mood = -1
        
        if self.mood >= 1:
            txt = 'مود: خوشحال'
        elif self.mood <= -1:
            txt = 'مود: غمگین'
        else:
            txt = 'مود: آروم'
        self.mood_label.text = fa(txt)
    
    def mood_state(self):
        if self.mood >= 1:
            return 'happy'
        if self.mood <= -1:
            return 'sad'
        return 'neutral'
    
    def ask(self, q):
        self.add_msg('تو: ' + q['label'])
        self.update_mood(q['impact'])
        st = self.mood_state()
        pool = q.get(st, q.get('neutral', ['...']))
        self.add_msg('ستاره: ' + random.choice(pool))
    
    def add_msg(self, text):
        lbl = Label(text=fa(text), font_size='14sp',
                    color=get_color_from_hex('#ffffff'),
                    size_hint_y=None, height=50)
        self.chat.add_widget(lbl)


ChatApp().run()
