
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

from pyrogram import Client, filters, enums
# from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pyrogram import Client, filters
import re
import math
import asyncio
from config import *
from lazydeveloper.helpers import  validate_query
# Initialize Pyrogram Client
from telethon import TelegramClient
from telethon.sessions import StringSession
from lazydeveloper.lazydb import db
# latest
from imdb import IMDb, Movie
imdb = IMDb() 
from fuzzywuzzy import process
from pyrogram.errors import MessageNotModified

user_files_data = {}
files_per_page = 10


# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    _, offset = query.data.split("_")

    try:
        offset = int(offset)
    except:
        offset = 0

    user_id = query.from_user.id

    # print(f"user id => {user_id}")
    files, n_offset, total = await get_api_results(user_id,  offset=offset, filter=True)
    # print(files)
    # print(n_offset)
    # print(total)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return

    btn = [
            [
                InlineKeyboardButton(
                    text=f"📂 {file[0]}",  # movie_name
                    url=file[1]           # target_url
                )
            ]
            for file in files
        ]


    if 0 < offset <= int(MAX_BTN):
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - int(MAX_BTN)

    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⋞ ʙᴀᴄᴋ", callback_data=f"next_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}", callback_data="pages"),
             InlineKeyboardButton("ɴᴇxᴛ ⋟", callback_data=f"next_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton(
                    "⋞ ʙᴀᴄᴋ", callback_data=f"next_{off_set}"),
                InlineKeyboardButton(
                    f"🗓 {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}", callback_data="pages"),
                InlineKeyboardButton(
                    "ɴᴇxᴛ ⋟", callback_data=f"next_{n_offset}")
            ],
        )
    btn.append([
        InlineKeyboardButton("How To Open Link ❓", url="https://t.me/FilmyflyLinkOpen")
    ])
    btn.append([
        InlineKeyboardButton("🪅Request", url="https://t.me/+Aa-zL92bgqQ4OTll"),
        InlineKeyboardButton("♻️Backup", url="https://t.me/AllTypeOfLinkss")
    ])
    btn.append([
        InlineKeyboardButton("18+  Channel 🔞", url="https://t.me/+jt0FTlngGCc3OWI1")
    ])
    try:
        reply_markup=InlineKeyboardMarkup(btn)
        await query.message.edit_reply_markup(reply_markup)
    except MessageNotModified:
        pass
    await query.answer("❤ Powered By @LazyDeveloperr ❤")

@Client.on_message(filters.group & filters.text & filters.incoming & ~filters.command(['start']))
async def message_handler(client, message):
      try:
         if message.text.startswith("/"):
               return

         print("\nMessage Received: " + message.text)

        # Validate and sanitize query
         args = message.text
         user_id = message.from_user.id
         txt = await message.reply(f"**⏳ Searching for links matching:** `{args}` 🔍")
         
         queryz = await validate_query(args)
         if not queryz:
               await message.reply("Please provide a valid search query.")
               return
         
         # print(f"Search Query: {queryz}")

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
         await asyncio.sleep(1)
         sessionstring = await db.get_session(OWNER_ID)
         if sessionstring is None:
            await txt.delete()
            # msstt h na - 😂 - isiliye copy krne aaye ho 😂 - kr lo - kr lo 
            return await message.reply(
               "Please visit again later. I’m waiting for my owner to initialize me. 😔\n\n"
               "If you know my owner, kindly ask him to initialize me. ❤️"
            )
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

         Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
         
         if not Lazyuserbot.is_connected():
            await Lazyuserbot.start()
         # await Lazyuserbot.start()

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

#================================================================================================================ 
#================================================================================================================ 
      #   Start search logic 1️⃣ // Hey this is LazyDeveloper, & I am writing this for developers ! 
#================================================================================================================ 
      #   This is advance search method for searching url in any message
      #   in you database channel, Ex; If any message contains the movie name 
      #   searched by user in db channel , and if that message has any link, then 
      #   bot will only extract the link from the messages 
#================================================================================================================ 
#================================================================================================================ 
         # search_results = []
         # try:
         #    # Search for messages containing the query term in the database channel
         #    async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz, limit=5):
         #       if search_msg.text:
         #             # Look for a URL in the first line
         #          match = re.match(r"(https?://[^\s]+)", search_msg.text)
         #          if match:
         #             search_results.append(match.group(1))  # Append the URL
         # except Exception as e:
         #       print(f"Error while searching messages: {e}")
         #       await message.reply("An error occurred while searching.")
         #       return

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

#================================================================================================================ 
#================================================================================================================ 
      #   Start search logic 2️⃣ // Hey this is LazyDeveloper, & I am writing this for developers ! 
#================================================================================================================
      #   This is super advance search method for searching url + Name in any message                            |🧧 CONTACT ME @LAZYDEVELOPERR
      #   in you database channel, Ex; If any message contains the movie name                                    |🧧 GITHUB @LAZYDEVELOPER
      #   (searched by user) in db channel , and if that message has any link, then                              |🧧 YOUTUBE @LAZYDEVELOPER
      #   bot will only extract the link and movie name from all the messages                                    |🧧 INSTAGRAM @LAZYDEVELOPER
      #   and print the movie name and link in group .                                                           |🧧 TELEGRAM @LAZYDEVELOPER
      #   ==> The bot will only extract the name which is found in => () <= this braces                          |
#================================================================================================================ 
                           #  WITH LOVE @LAZYDEVELOPER
#================================================================================================================ 
#================================================================================================================ 

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

         search_results = []  
         try:
            # Search for messages containing the query term in the database channel #limit=5
            async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz):
               if search_msg.text:
                  # Look for a URL in the first line
                  match = re.match(r"(https?://[^\s]+)", search_msg.text)
                  if match:
                     target_url = match.group(1).strip()  # Extract the URL

                     # Extract the movie name from text in parentheses ()
                     movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
                     movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"

                     # Append the result as a tuple of (movie_name, target_url)
                     search_results.append({"movie_name": movie_name, "target_url": target_url})
                     # print(search_results)
            
            if not search_results:
               miss_spelled = await lazydeveloperr_spell_check(queryz, message)
               print(f'miss_spelled : {miss_spelled}')
               if miss_spelled:
                  await txt.delete()
                  queryz = miss_spelled
                  # Search for messages containing the query term in the database channel #limit=5
                  async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz):
                    if search_msg.text:
                        # Look for a URL in the first line
                        match = re.match(r"(https?://[^\s]+)", search_msg.text)
                        if match:
                            target_url = match.group(1).strip()  # Extract the URL

                            # Extract the movie name from text in parentheses ()
                            movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
                            movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"

                            # Append the result as a tuple of (movie_name, target_url)
                            search_results.append({"movie_name": movie_name, "target_url": target_url})
                            # print(search_results)
                  
            user_files_data[user_id] = search_results
            print(f"Search results saved for user {user_id}: {search_results}")
         except Exception as e:
               print(f"Error while searching messages: {e}")
               await message.reply("An error occurred while searching.")
               return

         # Handle no results
         if search_results:
            await txt.delete()
            await display_files(message, user_id, queryz, offset=0)  # Display page 1
         else:
            no_result_text = (
                f"**No results found for '{queryz}'**\n\n"
                f"Try refining your query or checking spelling on "
                f"[Google](http://www.google.com/search?q={queryz.replace(' ', '%20')}%20Movie) 🔍."
            )
            
            link = f"http://www.google.com/search?q={queryz.replace(' ', '%20')}%20Movie"
            btn = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔎 Check On Google 🔍", url=link)]
            ])
            await txt.delete()
            await message.reply(no_result_text, reply_markup=btn, disable_web_page_preview=True)
            return

      except Exception as e:
         print(e)
         if txt:
               await txt.delete()
         await message.reply("I couldn't process your request. Please try again later.")
      finally:
         await asyncio.sleep(2)
         # tried to avoid overhead  - session load !
         await Lazyuserbot.disconnect()
         if not Lazyuserbot.is_connected():
               print("Session is disconnected successfully!")
         else:
               print("Session is still connected.")
               await Lazyuserbot.disconnect()
               print("⚠ Tried to disconnect session.\n If u r seeing this message again again then please report to  @LazyDeveloper ❤")
         return


# async def display_files(message, user_id, lazydevelopr_query, offset):
#     try:
#         files, offset, total_results = await get_api_results(user_id, offset=0, filter=True)
#         # print(f" got files => {files}")
#         # print(f" got offset => {offset}")
#         # print(f" got total_results => {total_results}")

#         # btn = []
#         btn = [
#             [
#                 # Use bracket notation
#                 InlineKeyboardButton(
#                     text=f"📂 {file['movie_name']}", url=file['target_url'])
#             ]
#             for file in files
#         ]
#         # btn = [
#         #         [
#         #             InlineKeyboardButton(
#         #                 text=f"📂 {file['movie_name'] if isinstance(file, dict) else file[0]}",
#         #                 url=file['target_url'] if isinstance(file, dict) else file[1]
#         #             )
#         #         ]
#         #         for file in files
#         #     ]
#         if offset != "":
#             btn.append(
#                 [InlineKeyboardButton(text=f"🗓 1/{math.ceil(int(total_results) / int(MAX_BTN))}", callback_data="pages"),
#                 InlineKeyboardButton(text="ɴᴇxᴛ ⋟", callback_data=f"next_{offset}")]
#             )
#         else:
#             btn.append(
#                 [InlineKeyboardButton(text="🗓 1/1", callback_data="pages")]
#             )
        
#         # 
#         btn.append([
#             [
#                InlineKeyboardButton(f"How To Open Link ❓", url=f"https://t.me/FilmyflyLinkOpen")
#             ],
#             [
#                InlineKeyboardButton(f"🪅Request", url=f"https://t.me/+Aa-zL92bgqQ4OTll"),
#                InlineKeyboardButton(f"♻️Backup", url=f"https://t.me/AllTypeOfLinkss")
#             ],
#             [
#                InlineKeyboardButton(f"18+  Channel 🔞", url=f"https://t.me/+jt0FTlngGCc3OWI1")
#             ]
#          ])
#         # Send the initial message to be edited on pagination
#         await message.reply_text(f"<blockquote><b>👻 Here is what i found for your query <code>{lazydevelopr_query}</code></b></blockquote>", reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
#     except Exception as e:
#         print(e)

async def display_files(message, user_id, lazydevelopr_query, offset):
    try:
        files, offset, total_results = await get_api_results(user_id, offset=0, filter=True)

        btn = [
            [
                InlineKeyboardButton(
                    text=f"📂 {file[0]}",  # movie_name
                    url=file[1]           # target_url
                )
            ]
            for file in files
        ]

        if offset != "":
            btn.append(
                [
                    InlineKeyboardButton(
                        text=f"🗓 1/{math.ceil(int(total_results) / int(MAX_BTN))}",
                        callback_data="pages"
                    ),
                    InlineKeyboardButton(
                        text="ɴᴇxᴛ ⋟", callback_data=f"next_{offset}"
                    )
                ]
            )
        else:
            btn.append([InlineKeyboardButton(text="🗓 1/1", callback_data="pages")])

        btn.append([
            InlineKeyboardButton("How To Open Link ❓", url="https://t.me/FilmyflyLinkOpen")
        ])
        btn.append([
            InlineKeyboardButton("🪅Request", url="https://t.me/+Aa-zL92bgqQ4OTll"),
            InlineKeyboardButton("♻️Backup", url="https://t.me/AllTypeOfLinkss")
        ])
        btn.append([
            InlineKeyboardButton("18+  Channel 🔞", url="https://t.me/+jt0FTlngGCc3OWI1")
        ])

        await message.reply_text(
            f"<blockquote><b>👻 Here is what i found for your query <code>{lazydevelopr_query}</code></b></blockquote>",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(e)

async def get_api_results(user_id, max_results=MAX_BTN, offset=0, filter=False):
    """For given query lazydeveloper returns (results, next_offset)"""
    files_data = user_files_data.get(user_id, [])
    total_results = len(files_data)
    next_offset = offset + max_results

    # Slice the files list according to the offset and max_results
    raw_files = files_data[offset:offset + max_results]

    # ✅ Force everything into tuple format (movie_name, target_url)
    files = []
    for f in raw_files:
        if isinstance(f, dict):
            files.append((f.get("movie_name", "Unknown"), f.get("target_url", "")))
        elif isinstance(f, (tuple, list)) and len(f) >= 2:
            files.append((f[0], f[1]))
        else:
            print(f"⚠ Unknown format in files_data: {f}")

    if next_offset > total_results:
        next_offset = ''

    return files, next_offset, total_results

# async def get_api_results(user_id,  max_results=MAX_BTN, offset=0, filter=False):
#     """For given query lazydeveloper returns (results, next_offset)"""
#     # user_id = chat_id
#     files_data = user_files_data.get(user_id, [])
#     print(files_data)
#     total_results = len(files_data)
#     print(total_results)
#     next_offset = offset + max_results
#     print(f"next_offset => {next_offset}")

#     # Slice the files list according to the offset and max_results
#     files = files_data[offset:offset + max_results]
#     print(f"files => {files}")
#     if next_offset > total_results:
#         next_offset = ''

#     return files, next_offset, total_results

async def lazydeveloperr_spell_check(wrong_name, msg):
    async def search_movie(wrong_name):
        search_results = imdb.search_movie(wrong_name)
        movie_list = [movie['title'] for movie in search_results]
        return movie_list
    user_id = msg.from_user.id
    movie_list = await search_movie(wrong_name)
    if not movie_list:
        return
    for _ in range(5):
        closest_match = process.extractOne(wrong_name, movie_list)
        if not closest_match or closest_match[1] <= 80:
            return 
        movie = closest_match[0]
    print(movie)
    return movie

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
