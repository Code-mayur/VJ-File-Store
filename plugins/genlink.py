# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re
import requests
from pyrogram import filters, Client, enums
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, UsernameInvalid, UsernameNotModified
from config import ADMINS, LOG_CHANNEL, PUBLIC_FILE_STORE, WEBSITE_URL, WEBSITE_URL_MODE
from plugins.database import unpack_new_file_id
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from plugins.users_api import get_user, get_short_link
import re
import os
import json
import base64
import logging

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)




async def allowed(_, __, message):
    if PUBLIC_FILE_STORE:
        return True
    if message.from_user and message.from_user.id in ADMINS:
        return True
    return False

def upload_image_requests(image_path):
    """Upload image to the server."""
    upload_url = "https://envs.sh"  # Make sure this URL is correct and functional
    try:
        with open(image_path, 'rb') as file:
            files = {'file': file}
            # Adding timeout for the request (e.g., 30 seconds)
            response = requests.post(upload_url, files=files, timeout=30)
            
            # Logging the response status and content
            logger.info(f"Upload response status: {response.status_code}")
            logger.debug(f"Upload response content: {response.text}")

            if response.status_code == 200:
                return response.text.strip()  # Ensure this returns the actual URL
            else:
                raise Exception(f"Upload failed with status code {response.status_code}")
    except requests.exceptions.Timeout:
        logger.error("Upload timed out.")
        return None
    except Exception as e:
        logger.error(f"Error during upload: {e}")
        return None


# Handle Photo uploads
@Client.on_message(filters.private & filters.photo)
async def handle_photo(bot, message):
    try:
        # Download the photo to the local system
        photo_path = await message.download()
        if not photo_path:
            raise Exception("Failed to download photo.")

        # Inform the user that the upload process is starting
        uploading_message = await message.reply_text("Uploading photo...")

        # Upload the photo to the external server
        photo_url = upload_image_requests(photo_path)

        # If the upload fails, raise an error
        if not photo_url:
            raise Exception("Failed to upload photo to the server. Please try again later.")

        # Edit the message to show the hosted photo URL and options
        await uploading_message.edit_text(
            text=f"**Photo hosted successfully. Here's the link:**\n\n"
                 f"Tap link to copy: <code>{photo_url}</code>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="Open Link", url=photo_url),
                InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={photo_url}")
            ]])
        )

        # Clean up: remove the downloaded photo file from local storage
        os.remove(photo_path)

    except Exception as e:
        # Log the error details for debugging
        logger.error(f"Error handling photo: {e}")
        await message.reply_text(f"An error occurred while processing the photo: {e}")



        
# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.create(allowed) & (filters.document | filters.video | filters.audio))
async def handle_media(bot, message):
    try:
        username = (await bot.get_me()).username
        file_type = message.media
        file_id, ref = unpack_new_file_id((getattr(message, file_type.value)).file_id)
        string = 'file_'
        string += file_id
        outstr = base64.urlsafe_b64encode(string.encode("ascii")).decode().strip("=")
        user_id = message.from_user.id
        user = await get_user(user_id)

        # Generate the file link
        if WEBSITE_URL_MODE:
            share_link = f"{WEBSITE_URL}?Tech_VJ={outstr}"
        else:
            share_link = f"https://t.me/{username}?start={outstr}"

        if user["base_site"] and user["shortener_api"]:
            short_link = await get_short_link(user, share_link)
            button_text = "ʜᴇʀᴇ's ᴛʜᴇ sʜᴏʀᴛ ʟɪɴᴋ"
            button_link = short_link
        else:
            button_text = "ʀᴇᴛʀɪᴇᴠᴇ ᴏʀ ɢᴇᴛ ғɪʟᴇ"
            button_link = share_link

        # Reply with the link
        reply_text = (
            "**⭕ ғɪʟᴇ sᴛᴏʀᴇᴅ ғᴏʀ ʀᴇᴛʀɪᴇᴠɪɴɢ, ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ**\n"
            "**ᴄᴏɴᴛᴀɪɴs** - 1 **ғɪʟᴇ**\n\n"
            "ʟᴏɴɢ ᴘʀᴇss ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴄᴏᴘʏ ᴏʀ sʜᴀʀᴇ ᴛʜᴇ ʟɪɴᴋ"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button_text, url=button_link)]
        ])

        await message.reply(reply_text, reply_markup=keyboard)

    except Exception as e:
        logger.error(f"Error handling media: {e}")
        await message.reply_text(f"An error occurred while processing the media: {e}")
        



# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command(['batch', 'pbatch']) & filters.create(allowed))
async def gen_link_batch(bot, message):
    username = (await bot.get_me()).username
    if " " not in message.text:
        return await message.reply("Use correct format.\nExample /batch https://t.me/vj_botz/10 https://t.me/vj_botz/20.")
    links = message.text.strip().split(" ")
    if len(links) != 3:
        return await message.reply("Use correct format.\nExample /batch https://t.me/vj_botz/10 https://t.me/vj_botz/20.")
    cmd, first, last = links
    regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
    match = regex.match(first)
    if not match:
        return await message.reply('Invalid link')
    f_chat_id = match.group(4)
    f_msg_id = int(match.group(5))
    if f_chat_id.isnumeric():
        f_chat_id = int(("-100" + f_chat_id))

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
    match = regex.match(last)
    if not match:
        return await message.reply('Invalid link')
    l_chat_id = match.group(4)
    l_msg_id = int(match.group(5))
    if l_chat_id.isnumeric():
        l_chat_id = int(("-100" + l_chat_id))

    if f_chat_id != l_chat_id:
        return await message.reply("Chat ids not matched.")
    try:
        chat_id = (await bot.get_chat(f_chat_id)).id
    except ChannelInvalid:
        return await message.reply('This may be a private channel / group. Make me an admin over there to index the files.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        return await message.reply(f'Errors - {e}')

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
    sts = await message.reply("**ɢᴇɴᴇʀᴀᴛɪɴɢ ʟɪɴᴋ ғᴏʀ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ**.\n**ᴛʜɪs ᴍᴀʏ ᴛᴀᴋᴇ ᴛɪᴍᴇ ᴅᴇᴘᴇɴᴅɪɴɢ ᴜᴘᴏɴ ɴᴜᴍʙᴇʀ ᴏғ ᴍᴇssᴀɢᴇs**")

    FRMT = "**ɢᴇɴᴇʀᴀᴛɪɴɢ ʟɪɴᴋ...**\n**ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs:** {total}\n**ᴅᴏɴᴇ:** {current}\n**ʀᴇᴍᴀɪɴɪɴɢ:** {rem}\n**sᴛᴀᴛᴜs:** {sts}"

    outlist = []

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

    # file store without db channel
    og_msg = 0
    tot = 0
    async for msg in bot.iter_messages(f_chat_id, l_msg_id, f_msg_id):
        tot += 1
        if msg.empty or msg.service:
            continue
        if not msg.media:
            # only media messages supported.
            continue
        try:
            file_type = msg.media
            file = getattr(msg, file_type.value)
            caption = getattr(msg, 'caption', '')
            if caption:
                caption = caption.html
            if file:
                file = {
                    "file_id": file.file_id,
                    "caption": caption,
                    "title": getattr(file, "file_name", ""),
                    "size": file.file_size,
                    "protect": cmd.lower().strip() == "/pbatch",
                }

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

                og_msg +=1
                outlist.append(file)
        except:
            pass
        if not og_msg % 20:
            try:
                await sts.edit(FRMT.format(total=l_msg_id-f_msg_id, current=tot, rem=((l_msg_id-f_msg_id) - tot), sts="Saving Messages"))
            except:
                pass
    with open(f"batchmode_{message.from_user.id}.json", "w+") as out:
        json.dump(outlist, out)
    post = await bot.send_document(LOG_CHANNEL, f"batchmode_{message.from_user.id}.json", file_name="Batch.json", caption="⚠️Generated for filestore.")
    os.remove(f"batchmode_{message.from_user.id}.json")
    file_id, ref = unpack_new_file_id(post.document.file_id)
    user_id = message.from_user.id
    user = await get_user(user_id)
    if WEBSITE_URL_MODE == True:
        share_link = f"{WEBSITE_URL}?Tech_VJ=BATCH-{file_id}"
    else:
        share_link = f"https://t.me/{username}?start=BATCH-{file_id}"
    if user["base_site"] and user["shortener_api"] != None:
        short_link = await get_short_link(user, share_link)
        await sts.edit(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\nContains `{og_msg}` files.\n\n🖇️ sʜᴏʀᴛ ʟɪɴᴋ :- {short_link}</b>")
    else:
        await sts.edit(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\nContains `{og_msg}` files.\n\n🔗 ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ :- {share_link}</b>")
        
# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
