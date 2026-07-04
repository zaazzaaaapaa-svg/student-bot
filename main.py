import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import google.generativeai as genai

# 1. إعداد مفاتيح التشغيل (التوكن والـ API)
# بنخلي الكود يقرأهم من إعدادات الاستضافة للأمان الكامل
BOT_TOKEN = os.environ.get("BOT_TOKEN", "حط_توكن_بوت_فاذر_هنا")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "حط_مفتاح_جمناي_هنا")

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# قاموس لتخزين ذاكرة الشات لكل طالب بشكل منفصل
user_sessions = {}

def get_chat_session(user_id):
    """إنشاء أو استدعاء جلسة شات ذكاء اصطناعي مخصصة للمستخدم"""
    if user_id not in user_sessions:
        # توجيه خفي ومطور للذكاء الاصطناعي عشان يعرف هويته وطريقة رده الحماسية
        system_instruction = (
            "أنت 'مساعد الطالب'، بوت ذكي جداً، روش ومرح، تساعد الطلاب في كل المواد الدراسية. "
            "شغلتك تشرح وتبسط وتلخص وتجيب على الأسئلة والمسائل باللهجة العربية المفهومة وبطريقة حماسية "
            "تشجع الطالب على المذاكرة وتخليه يقفل المواد."
        )
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
        user_sessions[user_id] = model.start_chat(history=[])
    return user_sessions[user_id]

# ==========================================
# 2. أمر تشغيل البوت الأساسي /start
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    
    # تجهيز الأزرار الشفافة الاحترافية (Inline Buttons) تحت الرسالة الترحيبية
    markup = InlineKeyboardMarkup()
    btn_clear = InlineKeyboardButton(text="🔄 جلسة جديدة", callback_data="clear_chat")
    btn_help = InlineKeyboardButton(text="❓ طريقة الاستخدام", callback_data="help_info")
    btn_share = InlineKeyboardButton(text="🔗 شارك البوت", url=f"https://t.me/share/url?url=https://t.me/{bot.get_me().username}")
    
    # ترتيب الأزرار: أول سطر زرار الجلسة والمساعدة، والسطر الثاني زرار المشاركة
    markup.row(btn_clear, btn_help)
    markup.row(btn_share)
    
    welcome_text = (
        "🔥 **يا هلا يا بطل! منور في مساعد الطالب** 🚀\n\n"
        "انسى بقى حيرة المذاكرة والزنقة قبل الامتحانات، من هنا ورايح أنا الـ Sidekick بتاعك في رحلتك الدراسية.\n\n"
        "💡 **أنا أقدر أساعدك في إيه؟**\n"
        "مفيش حاجة متقدرش تعملها! (حل مسائل، شروحات، تلخيص كتب ومحاضرات، بحث، وأي سؤال ييجي في بالك في أي مادة).\n\n"
        "🎒 ارمِ حمولك عليا واكتب سؤالك فوراً في الشات دلوقتي، ويلا بينا نقفل المواد! 👇"
    )
    bot.send_message(user_id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# ==========================================
# 3. أمر مسح الذاكرة /clear (جلسة جديدة)
# ==========================================
@bot.message_handler(commands=['clear'])
def clear_memory_command(message):
    process_clear(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "clear_chat")
def clear_memory_callback(call):
    process_clear(call.message.chat.id)
    bot.answer_callback_query(call.id, text="تم مسح الشات القديم!")

def process_clear(user_id):
    """تنفيذ مسح الذاكرة الفعلي وإعادة تصغير الجلسة"""
    if user_id in user_sessions:
        del user_sessions[user_id] # حذف الجلسة القديمة بالكامل
    
    confirm_text = (
        "🧼 **Done! الشات اتمسح وبقينا على الأبيض.**\n\n"
        "نسيت كل اللي فات وركزت معاك في الجديد. ارمِ سؤالك أو مادتك الجديدة وماتقلقش، كله تحت السيطرة! 🧠✨"
    )
    bot.send_message(user_id, confirm_text, parse_mode="Markdown")

# ==========================================
# 4. أمر المساعدة والدعم /help
# ==========================================
@bot.message_handler(commands=['help'])
def help_command(message):
    send_help_msg(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "help_info")
def help_callback(call):
    send_help_msg(call.message.chat.id)
    bot.answer_callback_query(call.id)

def send_help_msg(user_id):
    help_text = (
        "❓ **طريقة استخدام البوت الاحترافية:**\n\n"
        "1️⃣ **اسأل مباشرة:** البوت شغال بنظام الشات المفتوح، اكتب سؤالك، اكتب مسألة، أو اطلب تلخيص مادة فوراً وهيرد عليك.\n"
        "2️⃣ **تغيير الموضوع:** لو خلصت مذاكرة مادة وعاوز تدخل في مادة تانية، دوس على زرار `🔄 جلسة جديدة` أو ابعت أمر `/clear` عشان البوت ما يتلخبطش بكلامك القديم.\n"
        "3️⃣ **الأوامر السريعة:** تقدر تضغط على زر المنيو (القائمة) تحت عشان تختار الأوامر بسرعة.\n\n"
        "💪 البوت معمول عشان يسهل عليك، لو عندك أي استفسار ابدأ كلمني علطول!"
    )
    bot.send_message(user_id, help_text, parse_mode="Markdown")

# ==========================================
# 5. استقبال رسائل الطلاب وإرسالها للذكاء الاصطناعي
# ==========================================
@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
    user_id = message.chat.id
    student_query = message.text
    
    # إرسال حركة "جاري الكتابة..." عشان الطالب يطمن إن البوت شغال
    bot.send_chat_action(user_id, 'typing')
    
    try:
        # استدعاء الجلسة الخاصة بالطالب وإرسال سؤاله لها
        chat = get_chat_session(user_id)
        response = chat.send_message(student_query)
        
        # الرد بالإجابة الذكية
        bot.reply_to(message, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, "عذراً يا بطل، حصل ضغط صغير على السيرفر. جرب تبعت سؤالك تاني أو دوس /clear!")
