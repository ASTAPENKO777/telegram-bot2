from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters


user_states = {}
user_languages = {}

# Функція для команди /start
async def start(update: Update, context):
    user_id = update.message.from_user.id
    if user_id not in user_states:
        user_states[user_id] = "menu"
        user_languages[user_id] = "uk" 
    await show_main_menu(update)


async def show_main_menu(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")
    # Меню відповідно до мови
    if lang == "uk":
        keyboard = [
            ["📍 Місце розташування", "💰 Ціни"],
            ["📞 Зв'язатись з менеджером", "🏞️ Місця поблизу"],
            ["🌐 Ми в соцмережах", "🌐 Наш сайт"],
            ["🛖 Огляд садиби", "Чан!"],
            ["🌍 Змінити мову"]
        ]
        message = "Ось моє меню. Оберіть потрібний розділ:"
    else:
        keyboard = [
            ["📍 Location", "💰 Prices"],
            ["📞 Contact the manager", "🏞️ Nearby places"],
            ["🌐 Social Media", "🌐 Our website"],
            ["🛖 Cottage overview", "Bath!"],
            ["🌍 Change Language"]
        ]
        message = "Here is my menu. Choose a section:"
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(message, reply_markup=reply_markup)

async def show_location(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")
    
    # Повідомлення з кнопкою, яка веде до Google Maps
    message = (
        "Наші садиби знаходиться в унікальному місці, яке ви точно полюбите! Натисніть кнопку, щоб переглянути карту та побачити, де ми вас чекаємо😊"
        if lang == "uk"
        else "Our manor is located in a unique location that you will definitely love! Click the button to view the map and see where we are waiting for you😊"
    )

    # Текст кнопки залежно від мови
    button_text = "Відкрити на карті🗺️" if lang == "uk" else "Open on map🗺️"

    # Створення кнопки для відкриття карти
    keyboard = [
        [InlineKeyboardButton(button_text, url="https://maps.app.goo.gl/fErdpGampLsAe1dD9")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup)


async def show_prices(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")
    
    # Фотографії з підписами
    photos = [
        ("https://cf.bstatic.com/xdata/images/hotel/max1024x768/435837164.jpg?k=a1d3f3add1532926bb2992e57f612ce02b8e331f0d66a45aadb72c28306b546d&o=&hp=1", 
         "Будинок: 12-ть осіб на 4 номери, номер 4-х місний 1200грн/день, номер 2-х місний 800грн/день" if lang == "uk" else "House: for 12 people, 4 rooms, 4-person room 1200 UAH/day, 2-person room 800 UAH/day"),
        
        ("https://static3.karpaty.info/data/img/5626/out30.jpg", 
         "Будинок: на 8 осіб від 3000 грн/день" if lang == "uk" else "House: for 8 people from 3000 UAH/day"),
        
        ("https://lh3.googleusercontent.com/places/AAcXr8qvilBEZyBCXH93K7MvV-RsrddEGFuVLDoN8L40HPn03cI4FwznO7a5AA7y-r_VBqs26dpyYR7HqP6yfNxsW-EuCIyS8juEw3o=s1600-w480", 
         "Чан 1500грн/дві години, кожна наступна година +300грн" if lang == "uk" else "Hot tub 1500 UAH/two hours, each additional hour +300 UAH")
    ]
    
    # Відправляємо фото з підписами
    for photo, caption in photos:
        await update.message.reply_photo(photo=photo, caption=caption)

    # Текст, який відправляється в кінці
    message = "За додатковою інформацією переходіть | Огляд Садиби |" if lang == "uk" else "For more information, go to | Manor Overview |"

    # Клавіатура "Назад"
    back_button = "↩️ Назад" if lang == "uk" else "↩️ Back"
    keyboard = [[back_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Відправка текстового повідомлення після фотографій
    await update.message.reply_text(message, reply_markup=reply_markup)


    
async def show_contact(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")
    
    # Текст повідомлення
    message = (
        "Контакти:\n- Київстар: +380962812270\n- Vodafone: +380662526155\n- E-mail: lisova.chany@gmail.com"
        if lang == "uk"
        else "Contacts:\n- Kyivstar: +380962812270\n- Vodafone: +380662526155\n- E-mail: lisova.chany@gmail.com"
    )

    # Створення клавіатури з кнопками для Telegram і WhatsApp
    contact_keyboard = [
        [InlineKeyboardButton("Telegram", url="https://t.me/Vasyl_Astapenko")],
        [InlineKeyboardButton("WhatsApp", url="https://wa.me/qr/DW5RV3NAQ27YO1")],
    ]

    # Переклад кнопки "Назад" залежно від мови
    back_button = "↩️ Назад" if lang == "uk" else "↩️ Back"
    back_keyboard = [[back_button]] 
    
    # Створення розмітки клавіатури для контактів
    contact_markup = InlineKeyboardMarkup(contact_keyboard)
    # Створення розмітки клавіатури для кнопки "Назад"
    back_markup = ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True)

    # Відправлення повідомлення з контактами та кнопками для Telegram і WhatsApp
    await update.message.reply_text(message, parse_mode='Markdown', reply_markup=contact_markup)
    
    # Додамо кнопку "Назад"
    await update.message.reply_text("Натисніть 'Назад', щоб повернутися в головне меню." if lang == "uk" else "Press 'Back' to return to the main menu.", reply_markup=back_markup)



# Функція для соцмереж
async def show_social_media(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")
    
    if lang == "uk":
        message = "Ми в соцмережах:"
        button1 = InlineKeyboardButton("Instagram", url="https://www.instagram.com/lisovahatina.chan?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==")
        button2 = InlineKeyboardButton("Facebook", url="https://www.facebook.com/lisovahatuna")
        button3 = InlineKeyboardButton("TikTok", url="https://www.tiktok.com/@lisovahatinachan?is_from_webapp=1&sender_device=pc")
    else:
        message = "We are on social media:"
        button1 = InlineKeyboardButton("Instagram", url="https://www.instagram.com/lisovahatina.chan?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==")
        button2 = InlineKeyboardButton("Facebook", url="https://www.facebook.com/lisovahatuna")
        button3 = InlineKeyboardButton("TikTok", url="https://www.tiktok.com/@lisovahatinachan?is_from_webapp=1&sender_device=pc")
    
    # Клавіатура для соцмереж
    social_media_keyboard = [[button1], [button2], [button3]]
    
    # Відправка повідомлення з соцмережами без кнопки "Назад"
    await update.message.reply_text(message, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(social_media_keyboard))

# Функція для зміни мови
async def change_language(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")
    # Відображення вибору мови
    keyboard = [
        ["Українська", "English"]
    ]
    message = (
        "Оберіть мову:" if lang == "uk"
        else "Choose a language:"
    )
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(message, reply_markup=reply_markup)

# Функція для обробки текстових повідомлень
async def handle_message(update: Update, context):
    user_id = update.message.from_user.id
    text = update.message.text.strip().lower() 
    lang = user_languages.get(user_id, "uk")
    
    print(f"Отримано повідомлення від користувача: {text}") 
    
    # Перевірка вибору мови
    if text == "українська" or text == "english":
        user_languages[user_id] = "uk" if text == "українська" else "en"
        await show_main_menu(update)
        return
    
    # Обробка вибору меню
    if text == "📍 місце розташування" or text == "📍 location":
        await show_location(update)
        return
    elif text == "💰 ціни" or text == "💰 prices":
        await show_prices(update)
        return
    elif text == "📞 зв'язатись з менеджером" or text == "📞 contact the manager":
        await show_contact(update)
        return
    elif text == "🏞️ місця поблизу" or text == "🏞️ nearby places":
        await show_nearby_places(update)
        return
    elif text == "🌐 ми в соцмережах" or text == "🌐 social media":
        await show_social_media(update)
        return
    elif text == "🌐 наш сайт" or text == "🌐 our website":
        await show_website(update)
        return
    elif text == "🛖 огляд садиби" or text == "🛖 cottage overview":
        await show_cottage_overview(update)
        return
    elif text == "чан!" or text == "bath!":
        await show_bath(update)
        return
    elif text == "🌍 змінити мову" or text == "🌍 change language":
        await change_language(update)
        return
    elif text == "↩️ назад" or text == "↩️ back":  
        await show_main_menu(update)
    return
    
    # Випадок, коли введення не розпізнане
    response = "Невідомий вибір. Спробуйте ще раз." if lang == "uk" else "Unknown choice. Please try again."
    await update.message.reply_text(response, parse_mode='Markdown')


async def show_nearby_places(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")
    
    # Основне повідомлення
    message = (
        "Фотогалерея🌸" if lang == "uk" else "Photo Gallery🌸"
    )
    keyboard = [["↩️ Назад" if lang == "uk" else "↩️ Back"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Відправляємо основне повідомлення
    await update.message.reply_text(message, reply_markup=reply_markup)

    # Список фото з підписами
    photos = [
        (
            "https://karpatytravel.net/wp-content/uploads/2020/08/ozero-sinevir-3.jpg", 
            "Синевирське озеро вважається найцікавішим об'єктом Національного природного парку «Синевир» і є однією з візитних карток Українських Карпат. Воно розташоване на висоті 989 метрів над рівнем моря, має середню площу 4—5 гектарів, його середня глибина становить 8—10 м, максимальна — 22—24 м. (34-км від садиби)"
            if lang == "uk" else 
            "Synevyr Lake is considered the most fascinating feature of the Synevyr National Nature Park and one of the iconic landmarks of the Ukrainian Carpathians. It is located at an altitude of 989 meters above sea level, with an average area of 4–5 hectares. Its average depth is 8–10 meters, and the maximum depth reaches 22–24 meters. (34 km from the manor)"
        ),
        (
            "https://tourinform.org.ua/wp-content/uploads/2019/12/kriselka.jpg",
            "Підйомник в Пилипці - це двомісна крісельна канатна дорога довжиною 1650 метрів з фіксованими кріслами. Цей підйомник доставляє туристів з гірськолижним або велосипедним спорядженням на гору Гемба (полонина Боржава). Також на курорті є швидкісний бугельний підйомник «Боржавські полонини» довжиною 1,5 кілометри. Всього на курорті є 7 підйомників, включаючи 6 бугельних витягів. (24-км від садиби)"
            if lang == "uk" else 
            "The chairlift in Pylypets is a two-seater cable car, 1650 meters long, with fixed seats. This lift takes tourists with ski or bicycle equipment to Mount Gemba (Borzhava Plateau). There are also high-speed rope tows, including the 'Borzhava Meadows' lift, 1.5 kilometers long. In total, the resort offers 7 lifts, including 6 rope tows. (24 km from the manor)"
        ),
        (
            "https://myukraine.org.ua/wp-content/uploads/2017/04/vodospad-shypit-1-min-min.jpg",
            "Водоспад Шипіт розташований на північних схилах Полонини Боржави, біля села Пилипець. Це один з семи природних чудес України, який причаровує своєю красою в будь-яку пору року. (24-км від садиби)"
            if lang == "uk" else 
            "The Shypit Waterfall is located on the northern slopes of the Borzhava Polonyna near the village of Pylypets. It is one of the seven natural wonders of Ukraine, enchanting with its beauty at any time of the year. (24 km from the manor)"
        ),
        (
            "https://rdzs.org/wp-content/uploads/manual/EC785D.jpeg",
            "Закинуте село 'Кужбеї'(піший маршрут від садиби) відоме своєю прекрасною природою та пагорбами, приховує безліч захоплюючих історій про забуті місця в цій польовій області. Одним із таких місць є покинуте село Кужбеї, яке з часом перетворилося на тиху й самотню місцевість. Проте, колись це було чудове село, заряджене енергією та історичним багатством. (3-км від садиби)"
            if lang == "uk" else 
            "'Kuzhbei' abandoned village (hiking trail from the manor) is known for its beautiful nature and hills, hiding many fascinating stories about forgotten places in this rural area. One of these places is the abandoned village of Kuzhbei, which over time has turned into a quiet and lonely area. However, it was once a wonderful village, charged with energy and historical richness. (3 km from the manor)"
        ),
        (
            "https://tourinform.org.ua/wp-content/uploads/2021/05/geizer.jpg",
            "Гейзер мінеральної води у Вучковому знаходиться на березі гірського потоку в урочищі Петровець на під'їзді до Міжгір'я з боку Хуста. Вода у джерелі солона, з високим вмістом заліза. Тривалість виверження – близько 10 хвилин, а періодичність – 1-2 години. (17-км від садиби)"
            if lang == "uk" else 
            "The mineral water geyser in Vuchkove is located on the bank of a mountain stream in the Petrovets tract, approaching Mizhhirya from Khust. The water in the spring is salty, with high iron content. The eruption lasts about 10 minutes and occurs every 1–2 hours. (17 km from the manor)"
        ),
        (
            "https://lowcost.ua/wp-content/uploads/2020/07/minvoda.jpeg",
            "Село Келечин відоме своїми мінеральними джерелами, які багаті на корисні речовини. Біля дороги ви знайдете джерела, які легко доступні для всіх відвідувачів. (15-км від садиби)"
            if lang == "uk" else 
            "The village of Kelechyn is famous for its mineral springs, which are rich in beneficial substances. Near the road, you will find springs that are easily accessible to all visitors. (15 km from the manor)"
        )
    ]
    
    # Надсилаємо фотографії з підписами
    for photo, caption in photos:
        await update.message.reply_photo(photo=photo, caption=caption)



async def show_website(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")

    # Повідомлення про сайт
    message = (
        "Ласкаво просимо на сайт нашої садиби відпочинку! Тут ви знайдете всю необхідну інформацію про комфортний відпочинок серед природи. Ознайомтесь з варіантами проживання, цінами та спеціальними пропозиціями. Забронюйте свій ідеальний відпочинок вже зараз😊"
        if lang == "uk" else
        "Welcome to the website of our holiday cottage! Here you will find all the necessary information about a comfortable vacation amidst nature. Explore accommodation options, prices, and special offers. Book your perfect holiday now😊"
    )

    # Кнопка для переходу на сайт
    website_button = [
        [InlineKeyboardButton("Перейти на САЙТ" if lang == "uk" else "Visit WEBSITE", url="https://forest-hut.com/")]
    ]
    reply_markup = InlineKeyboardMarkup(website_button)

    # Відправка повідомлення з кнопкою
    await update.message.reply_text(message, reply_markup=reply_markup)

    

async def show_cottage_overview(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")

    # Опис для огляду садиби на двох мовах
    if lang == "uk":
        message = (
            "Ласкаво просимо до нашої садиби! 🏡\n\n"
            "Ми пропонуємо комфортне проживання серед прекрасної природи Карпат. У нас ви знайдете:"
            "\n- Затишні номери з усіма зручностями."
            "\n- Просторі території для відпочинку на свіжому повітрі."
            "\n- Дружню атмосферу, яка дозволить вам повністю відновити сили."
            "\n\nТакож ви можете насолоджуватися красивими краєвидами навколо садиби і вирушити в подорож по Карпатах. 😊"
        )
        caption_first_photo = (
            "12-місний котедж: ідеальний для великих компаній! "
            "У котеджі є 4 номери: 2 двомісних та 2 чотиримісних. Комфорт та простір для вашого відпочинку!"
        )
        caption_second_photo = "8-місний котедж: зручний і затишний варіант для невеликої компанії або сім'ї."
        caption_third_photo = "№1 Сімейний чотирьох-місний номер 1200грн/доб."
        caption_fourth_photo = "№2 Сімейний чотирьох-місний номер 1200грн/доб."
        caption_fifth_photo = "№3 Двох-місний номер 800грн/доб."
        caption_sixth_photo = "№4 Двох-місний номер 800грн/доб."
    else:
        message = (
            "Welcome to our cottage! 🏡\n\n"
            "We offer comfortable accommodation amidst the beautiful Carpathian nature. Here you will find:"
            "\n- Cozy rooms with all amenities."
            "\n- Spacious outdoor areas for relaxation."
            "\n- A friendly atmosphere that will allow you to fully restore your energy."
            "\n\nYou can also enjoy the beautiful views around the cottage and embark on a journey through the Carpathians. 😊"
        )
        caption_first_photo = (
            "12-person cottage: perfect for large groups! The cottage has 4 rooms: 2 double rooms and 2 quadruple rooms. "
            "Comfort and space for your relaxation!"
        )
        caption_second_photo = "8-person cottage: a convenient and cozy option for a small company or family."
        caption_third_photo = "№1 Family quadruple room 1200 UAH/day."
        caption_fourth_photo = "№2 Family quadruple room 1200 UAH/day."
        caption_fifth_photo = "№3 Double room 800 UAH/day."
        caption_sixth_photo = "№4 Double room 800 UAH/day."

    # Фотографії садиби
    photo_files = [
        ("https://cf.bstatic.com/xdata/images/hotel/max1024x768/435837164.jpg?k=a1d3f3add1532926bb2992e57f612ce02b8e331f0d66a45aadb72c28306b546d&o=&hp=1", caption_first_photo), 
        ("https://cf.bstatic.com/xdata/images/hotel/max1024x768/435837112.jpg?k=c72e730a476a4d8dd5848beea931d81c946bc77855a59e16dcfba522ec7b608c&o=&hp=1", caption_second_photo),
        ("https://cf.bstatic.com/xdata/images/hotel/max1024x768/618905039.jpg?k=9c75913133a959b72cdb2ac8a3e111a952c50e37d48634b922215ac3093c8711&o=&hp=1", caption_third_photo),  
        ("https://cf.bstatic.com/xdata/images/hotel/max1024x768/618454228.jpg?k=a73dfb1305a063a34cda22a07722e5359c421d612aae5a76f5dbc362ee8b9f6c&o=&hp=1", caption_fourth_photo), 
        ("https://cf.bstatic.com/xdata/images/hotel/max1024x768/618454210.jpg?k=8d237ddd759d7ad80117e01aa01187f2c874a6d7abce033dcaaad3c0897219ae&o=&hp=1", caption_fifth_photo),  
        ("https://cf.bstatic.com/xdata/images/hotel/max1024x768/618900587.jpg?k=6afb899983636d99bbf89f07344516c2eefd7abb541a1d2fc75befcadae21547&o=&hp=1", caption_sixth_photo), 
    ]
    
    # Відправка текстового опису
    await update.message.reply_text(message)

    # Відправка фотографій з підписами
    for photo_path, caption in photo_files:
        await update.message.reply_photo(photo_path, caption=caption)

    # Переклад кнопки "Назад" залежно від мови
    back_button = "↩️ Назад" if lang == "uk" else "↩️ Back"
    keyboard = [[back_button]]  
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Відправка кнопки "Назад"
    await update.message.reply_text("Натисніть 'Назад' для повернення." if lang == "uk" else "Press 'Back' to return.", reply_markup=reply_markup)

 
# Функція для чану з фото та описом
async def show_bath(update: Update):
    user_id = update.message.from_user.id
    lang = user_languages.get(user_id, "uk")

    # Опис
    if lang == "uk":
        message = (
            "Оздоровчий ЧАН з гірськими травами на 8 осіб — 1500 грн за 2 години процедури. Кожна наступна година +300 грн.\n\n"
            "Фотогалерея🌸:\n"
        )
        back_button = "↩️ Назад"
    else:
        message = (
            "Wellness CHAN with mountain herbs for 8 people — 1500 UAH for a 2-hour procedure. Each subsequent hour + 300 UAH.\n\n"
            "Photo Gallery🌸:\n"
        )
        back_button = "↩️ Back"

    photo_files = [
        "https://th.bing.com/th/id/OIP.LiD9qDalkkZ-lDLI-TBKEAHaIJ?rs=1&pid=ImgDetMain", 
        "https://svitkarpat.com/wp-content/uploads/2025/01/photo_2024-01-11_10-31-43-optimized.jpg?ver=1736479209",  
        "https://forest-hut.com/wp-content/uploads/forest-hut-2019-12-14.jpg", 
        "https://static1.karpaty.info/data/img/5626/out38.jpg",  
        "https://forest-hut.com/wp-content/uploads/forest-hut-2019-12-6.jpg"  
    ]

    await update.message.reply_text(message)

    for photo_path in photo_files:
        await update.message.reply_photo(photo_path)

    keyboard = [[back_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if lang == "uk":
        await update.message.reply_text("Натисніть 'Назад' для повернення.", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Press 'Back' to return.", reply_markup=reply_markup)


if __name__ == "__main__":
    TOKEN = "" # Вставте свій API токен
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущено...")
    app.run_polling()
