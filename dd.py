import os
import asyncio
import aiohttp
import random
import discord
from discord.ext import commands
import time
import json
import uuid
import base64
import tls_client
from discord import ButtonStyle, SelectOption
from discord.ui import Button, View, Select


prefix = input("Nhập prefix cho bot: ")
bot_token = input("Nhập token bot: ")
admin_id = int(input("Nhập ID admin ban đầu: "))


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)


start_time = time.time()


CONFIG_FILE = "config.json"
ERROR_FILE = "error.txt"
DEFAULT_CONFIG = {
    "admins": [admin_id],
    "message_file": "nhaychet.txt"
}


gif_list = [
    'https://i.pinimg.com/originals/f5/f2/74/f5f27448c036af645c27467c789ad759.gif',
    'https://i.pinimg.com/originals/e3/8b/75/e38b75f9ceb27f5f032f5656158dde55.gif',
    'https://i.pinimg.com/originals/05/38/99/0538996a830a8ac87ee38b21ace44c10.gif',
    'https://i.pinimg.com/originals/ef/aa/c5/efaac5ba7fa5111bb8fd33525274f009.gif',
    'https://images-ext-1.discordapp.net/external/8wOKFrUpEVTbowSuRztMmuyT50jjKfmZNNeYYu4KBTo/https/i.imgur.com/h37sC9T.mp4',
    'https://images-ext-1.discordapp.net/external/0utoF0MizcVHhL76uVIkJ0B2qZWOin2C5vfdPBmyEqk/https/i.imgur.com/RSsJj2x.mp4',
    'https://images-ext-1.discordapp.net/external/zAHEfElUS89jO5hMDC0Ie_fblXlqJizUfDzJwf5uVpA/https/i.imgur.com/V0vQ0Zh.mp4',
    'https://images-ext-1.discordapp.net/external/P5CgM06-Vf7nrjZPMsSvrhprHPLSsrVqOgBkr0aerys/https/i.imgur.com/ldX0qPY.mp4',
]


def log_error(message):
    with open(ERROR_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    log_error("File config.json rỗng, sử dụng cấu hình mặc định.")
                    return DEFAULT_CONFIG
        except json.JSONDecodeError:
            log_error("File config.json không hợp lệ, sử dụng cấu hình mặc định.")
            return DEFAULT_CONFIG
    else:
        log_error("File config.json không tồn tại, sử dụng cấu hình mặc định.")
        return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        log_error(f"Lỗi khi lưu config.json: {str(e)[:50]}...")

config = load_config()


def check_admin():
    async def predicate(ctx):
        return ctx.author.id in config["admins"]
    return commands.check(predicate)


class MenuView(View):
    def __init__(self, author_name, author_id):
        super().__init__(timeout=None)
        self.author_id = author_id
        self.add_item(Select(
            placeholder="Chọn lệnh...",
            options=[
                SelectOption(label="Treo", value="treo", description="Treo ngôn đa token discord"),
                SelectOption(label="Nhây", value="nhay", description="Treo nhây đa token discord"),
                SelectOption(label="Nhây 2C", value="nhay2c", description="Treo nhây 2 chữ đa token"),
                SelectOption(label="Fake", value="fake", description="Treo réo tag tên fake soạn"),
                SelectOption(label="Réo", value="reo", description="Treo chửi réo + réo tên"),
                SelectOption(label="Treo Ảnh", value="treoanh", description="Treo ngôn ảnh đa token"),
                SelectOption(label="Join", value="join", description="Join token tham gia sever"),
                SelectOption(label="Check Token", value="checktoken", description="Kiểm tra token sống/chết"),
                SelectOption(label="Set File", value="setfile", description="Set file ngôn"),
                SelectOption(label="Add Admin", value="addadmin", description="Thêm admin"),
                SelectOption(label="Remove Admin", value="removeadmin", description="Xóa admin"),
                SelectOption(label="List Admin", value="listadmin", description="Xem danh sách admin"),
                SelectOption(label="Uptime", value="uptime", description="Xem thời gian bot chạy"),
                SelectOption(label="Ping", value="ping", description="Kiểm tra độ trễ")
            ],
            custom_id=f"menu_select_{author_id}"
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author_id

# Lớp View cho sao chép token sống
class CopyTokensView(View):
    def __init__(self, valid_tokens):
        super().__init__(timeout=None)
        self.valid_tokens = valid_tokens

    @discord.ui.button(label="Sao chép Token Sống", style=ButtonStyle.green, custom_id="copy_tokens_button")
    async def copy_tokens_button(self, interaction: discord.Interaction, button: Button):
        tokens_text = "\n".join(self.valid_tokens)
        await interaction.response.send_message(f"```plaintext\n{tokens_text}\n```", ephemeral=True)


active_tasks = {}


async def validate_token(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": token}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                return response.status == 200
        except Exception as e:
            log_error(f"Lỗi kiểm tra token {token[:5]}...{token[-5:]}: {str(e)[:50]}...")
            return False


async def handle_response(response, channel_id, message, token):
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    try:
        if response.status == 200:
            return 0
        elif response.status == 429:
            retry_after = (await response.json()).get("retry_after", 1)
            log_error(f"Token {token_preview} bị giới hạn, chờ {retry_after}s")
            return retry_after
        elif response.status == 401:
            log_error(f"Token {token_preview} không hợp lệ!")
            return 0
        elif response.status in [500, 502, 408]:
            log_error(f"Lỗi server {response.status} - Token: {token_preview}")
            return 5
        else:
            log_error(f"Lỗi {response.status} - Token: {token_preview}")
            return 5
    except Exception as e:
        log_error(f"Lỗi xử lý phản hồi cho token {token_preview}: {str(e)[:50]}...")
        return 5


async def spam_message(thread, token, channel_id, message, delay, use_random_delay, min_delay, max_delay, semaphore, bold_text):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    message = message[:2000]
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    async with aiohttp.ClientSession() as session:
        first_success = False
        while True:
            try:
                async with semaphore:
                    message_to_send = f"**{message}**" if bold_text else message
                    async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                        retry_after = await handle_response(response, channel_id, message, token)
                        if retry_after:
                            await asyncio.sleep(retry_after)
                        else:
                            if not first_success:
                                await thread.send(f"Đã spam thành công! Gõ `{prefix}stop` để dừng.")
                                first_success = True
                            await asyncio.sleep(random.uniform(min_delay, max_delay) if use_random_delay else delay)
            except asyncio.CancelledError:
                break
            except Exception as e:
                log_error(f"Token {token_preview}: {str(e)[:50]}...")
                await asyncio.sleep(1)


async def spam_message_nhay(thread, token, channel_id, messages, delay, use_random_delay, min_delay, max_delay, mention_user, user_ids, semaphore, bold_text):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    mention_string = " ".join([f"<@{user_id}>" for user_id in user_ids]) if mention_user else ""
    async with aiohttp.ClientSession() as session:
        first_success = False
        while True:
            message = random.choice(messages).strip() if messages else ""
            try:
                async with semaphore:
                    message_to_send = f"**{mention_string} {message}**" if bold_text and mention_user else f"**{message}**" if bold_text else f"{mention_string} {message}" if mention_user else message
                    async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                        retry_after = await handle_response(response, channel_id, message, token)
                        if retry_after:
                            await asyncio.sleep(retry_after)
                        else:
                            if not first_success:
                                await thread.send(f"Đã spam thành công! Gõ `{prefix}stop` để dừng.")
                                first_success = True
                            await asyncio.sleep(random.uniform(min_delay, max_delay) if use_random_delay else delay)
            except asyncio.CancelledError:
                break
            except Exception as e:
                log_error(f"Token {token_preview}: {str(e)[:50]}...")
                await asyncio.sleep(1)


async def fake_typing_and_send_message(thread, token, channel_id, messages, delay, use_random_delay, min_delay, max_delay, mention_user, user_ids, semaphore, bold_text, name_to_call=None):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    mention_string = " ".join([f"<@{user_id}>" for user_id in user_ids]) if mention_user else ""
    async with aiohttp.ClientSession() as session:
        first_success = False
        while True:
            message = random.choice(messages).strip() if messages else ""
            if name_to_call:
                message = message.replace("{name}", name_to_call)
            try:
                async with session.post(typing_url, headers=headers):
                    for _ in message:
                        await asyncio.sleep(0.05)
                async with semaphore:
                    message_to_send = f"**{mention_string} {message}**" if bold_text and mention_user else f"**{message}**" if bold_text else f"{mention_string} {message}" if mention_user else message
                    async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                        retry_after = await handle_response(response, channel_id, message, token)
                        if retry_after:
                            await asyncio.sleep(retry_after)
                        else:
                            if not first_success:
                                await thread.send(f"Đã spam thành công! Gõ `{prefix}stop` để dừng.")
                                first_success = True
                            await asyncio.sleep(random.uniform(min_delay, max_delay) if use_random_delay else delay)
            except asyncio.CancelledError:
                break
            except Exception as e:
                log_error(f"Token {token_preview}: {str(e)[:50]}...")
                await asyncio.sleep(1)


async def spam_image(thread, token, channel_id, message, image_url, delay, use_random_delay, min_delay, max_delay, semaphore, bold_text):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    message = message[:2000]
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    async with aiohttp.ClientSession() as session:
        first_success = False
        while True:
            try:
                async with semaphore:
                    message_to_send = f"**{message}**" if bold_text else message
                    payload = {"content": message_to_send, "embeds": [{"image": {"url": image_url}}]}
                    async with session.post(url, json=payload, headers=headers) as response:
                        retry_after = await handle_response(response, channel_id, message, token)
                        if retry_after:
                            await asyncio.sleep(retry_after)
                        else:
                            if not first_success:
                                await thread.send(f"Đã spam thành công! Gõ `{prefix}stop` để dừng.")
                                first_success = True
                            await asyncio.sleep(random.uniform(min_delay, max_delay) if use_random_delay else delay)
            except asyncio.CancelledError:
                break
            except Exception as e:
                log_error(f"Token {token_preview}: {str(e)[:50]}...")
                await asyncio.sleep(1)



async def join_server(thread, token, invite_link):
    invite_code = re.search(r'(?:(?:http:\/\/|https:\/\/)?discord\.gg\/|discordapp\.com\/invite\/|discord\.com\/invite\/)?([a-zA-Z0-9-]+)', invite_link)
    invite_code = invite_code.group(1) if invite_code else invite_link
    session = tls_client.Session(client_identifier="chrome_137", random_tls_extension_order=True)
    device_id = str(uuid.uuid4())
    x_super_properties = base64.b64encode(json.dumps({
        "oc": "AndHa.WQi",
        "browser": "Android",
        "os": "Android",
        "osVersion": "10",
        "platform": "Aos",
        "client_version": "112.2",
        "native_build_number": "177",
        "client_build_number": "140025",
        "client_event_source": None,
        "device_vendor_id": str(uuid.uuid4()),
        "browser_channel_type": "stable",
        "browser_name": "Chrome",
        "browser_version": "137.0.0.0",
        "os_arch": "arm64",
        "referring_domain": False,
        "referring_page": "",
        "ref_err": None
    }).encode()).decode()
    user_agent = random.choice([
        f"Mozilla/5.0 (Linux; Android {ver}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36"
        for ver, device, chrome_ver in [
            ("10", "SM-A505F", "135.0.0.0"),
            ("11", "SM-G970F", "136.0.0.0"),
            ("12", "Pixel 6", "137.0.0.0"),
            ("13", "OnePlus 9", "138.0.0.0")
        ]
    ])
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Authorization": token,
        "Content-Type": "application/json",
        "Cookie": f"__dcfduid={''.join(random.choice('0123456789abcdef') for _ in range(32))}; "
                 f"__sdcfduid={''.join(random.choice('0123456789abcdef') for _ in range(96))}; "
                 f"__cfruid={''.join(random.choice('0123456789abcdef') for _ in range(40))}; "
                 f"_cfuvid={''.join(random.choice('0123456789ABCDEF') for _ in range(36))}-{random.randint(1000000000, 9999999999)}; "
                 f"locale={random.choice(['vi', 'en-US', 'en-GB'])}; "
                 f"cf_clearance={''.join(random.choice('0123456789abcdef') for _ in range(40))}-{int(time.time())}-0-1-{''.join(random.choice('0123456789abcdef') for _ in range(8))}",
        "Origin": "https://discord.com",
        "Referer": f"https://discord.com/invite/{invite_code}",
        "Sec-Ch-Ua": '"Chromium";v="137", "Not A;Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": user_agent,
        "X-Context-Properties": base64.b64encode(json.dumps({"location": "Accept Invite Page"}).encode()).decode(),
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": random.choice(["vi", "en-US", "en-GB"]),
        "X-Discord-Timezone": "Asia/Saigon",
        "X-Super-Properties": x_super_properties
    }
    try:
        async with session.get("https://discord.com/api/v9/experiments", headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if "fingerprint" in data:
                    headers["X-Fingerprint"] = data["fingerprint"]
    except Exception as e:
        log_error(f"Lỗi lấy fingerprint cho token {token[:5]}...{token[-5:]}: {str(e)[:50]}...")
    try:
        async with session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers, json={}) as response:
            return response
    except Exception as e:
        log_error(f"Lỗi khi tham gia server với token {token[:5]}...{token[-5:]}: {str(e)[:50]}...")
        return None


async def join_thread(thread, tokens, invite_link, delay, user_id):
    success = 0
    failed = 0
    captcha = 0
    retries = []
    token_preview = lambda t: t[:5] + "..." + t[-5:] if len(t) > 10 else t
    for token in tokens:
        if thread.id not in active_tasks or user_id not in active_tasks[thread.id]:
            break
        response = await join_server(thread, token, invite_link)
        if response:
            if response.status == 200:
                success += 1
            elif "retry_after" in await response.text():
                retry_after = (await response.json()).get("retry_after", 5)
                retries.append(token)
                log_error(f"Token {token_preview(token)} bị giới hạn, chờ {retry_after}s")
                await asyncio.sleep(retry_after)
                response = await join_server(thread, token, invite_link)
                if response and response.status == 200:
                    success += 1
                else:
                    failed += 1
                    log_error(f"Token {token_preview(token)} vẫn thất bại sau retry")
            elif "cloudflare" in (await response.text()).lower():
                retries.append(token)
                log_error(f"Token {token_preview(token)} bị Cloudflare block")
                await asyncio.sleep(random.uniform(5, 10))
                response = await join_server(thread, token, invite_link)
                if response and response.status == 200:
                    success += 1
                else:
                    failed += 1
                    log_error(f"Token {token_preview(token)} vẫn bị Cloudflare block")
            elif "captcha_key" in await response.text() or "captcha-required" in await response.text():
                captcha += 1
                log_error(f"Token {token_preview(token)} gặp Hcaptcha")
            elif 'You need to verify' in await response.text():
                failed += 1
                log_error(f"Token {token_preview(token)} chết")
            else:
                failed += 1
                error_text = (await response.text())[:50] + "..." if len(await response.text()) > 50 else await response.text()
                log_error(f"Token {token_preview(token)} lỗi: {response.status} - {error_text}")
        else:
            failed += 1
            log_error(f"Token {token_preview(token)} không kết nối được")
        await asyncio.sleep(random.uniform(1, 3))
    if thread.id in active_tasks and user_id in active_tasks[thread.id]:
        await thread.send(f"Đã tham gia server thành công: {success}\nThất bại: {failed}\nHcaptcha: {captcha}\nRetry: {len(retries)}\nGõ `{prefix}stop` để dừng.")


async def wait_for_message(user, channel, prompt):
    def check(m):
        return m.author.id == user.id and m.channel.id == channel.id
    try:
        msg = await bot.wait_for('message', check=check, timeout=60.0)
        return msg
    except asyncio.TimeoutError:
        await channel.send(f"Timeout khi đợi {prompt}!")
        return None


@bot.command()
async def menu(ctx):
    embed = discord.Embed(title="Danh Sách Lệnh", description="Chọn một lệnh bên dưới:", color=discord.Color.purple())
    embed.add_field(name="Lệnh", value="1. Treo\n2. Nhây\n3. Nhây 2C\n4. Fake\n5. Réo\n6. Treo Ảnh\n7. Join\n8. Check Token\n9. Set File\n10. Add Admin\n11. Remove Admin\n12. List Admin\n13. Uptime\n14. Ping", inline=False)
    view = MenuView(ctx.author.name, ctx.author.id)
    random_gif = random.choice(gif_list)
    await ctx.send(random_gif)
    await ctx.send(embed=embed, view=view)


@bot.command()
@check_admin()
async def checktoken(ctx):
    thread = await ctx.channel.create_thread(name=f"CheckToken - {ctx.author.name}", auto_archive_duration=60)
    await ctx.send(f"Đã tạo thread {thread.mention} để kiểm tra token!")
    await thread.send("Dán các token (1 dòng 1 token):")
    tokens_msg = await wait_for_message(ctx.author, thread, "tokens")
    if not tokens_msg:
        return
    tokens = [t.strip() for t in tokens_msg.content.splitlines() if t.strip()]
    if not tokens:
        await thread.send("Không có token nào được cung cấp!")
        return
    valid_tokens = []
    invalid_tokens = []
    for token in tokens:
        if await validate_token(token):
            valid_tokens.append(token)
        else:
            invalid_tokens.append(token)
            log_error(f"Token {token[:5]}...{token[-5:]} không hợp lệ")
    embed = discord.Embed(title="Kết Quả Kiểm Tra Token", color=discord.Color.blue())
    embed.add_field(name="Token Sống", value="\n".join([f"`{t}`" for t in valid_tokens]) or "Không có", inline=False)
    embed.add_field(name="Token Chết", value="\n".join([f"`{t}`" for t in invalid_tokens]) or "Không có", inline=False)
    view = CopyTokensView(valid_tokens) if valid_tokens else None
    await thread.send(embed=embed, view=view)


@bot.command()
@check_admin()
async def setfile(ctx):
    thread = await ctx.channel.create_thread(name=f"SetFile - {ctx.author.name}", auto_archive_duration=60)
    await ctx.send(f"Đã tạo thread {thread.mention} để đặt file tin nhắn!")
    await thread.send("Nhập tên file tin nhắn (.txt):")
    file_msg = await wait_for_message(ctx.author, thread, "tên file")
    if not file_msg:
        return
    file_name = file_msg.content.strip()
    if not file_name.endswith('.txt'):
        file_name += '.txt'
    if not os.path.exists(file_name):
        await thread.send(f"File `{file_name}` không tồn tại!")
        return
    config["message_file"] = file_name
    save_config(config)
    await thread.send(f"Đã đặt file tin nhắn: `{file_name}`")


@bot.command()
@check_admin()
async def addadmin(ctx):
    thread = await ctx.channel.create_thread(name=f"AddAdmin - {ctx.author.name}", auto_archive_duration=60)
    await ctx.send(f"Đã tạo thread {thread.mention} để thêm admin!")
    await thread.send("Tag người dùng để thêm làm admin:")
    msg = await wait_for_message(ctx.author, thread, "tag admin")
    if not msg:
        return
    if not msg.mentions:
        await thread.send("Vui lòng tag ít nhất một người dùng!")
        return
    for user in msg.mentions:
        if user.id not in config["admins"]:
            config["admins"].append(user.id)
            await thread.send(f"Đã thêm {user.mention} làm admin!")
        else:
            await thread.send(f"{user.mention} đã là admin!")
    save_config(config)


@bot.command()
@check_admin()
async def removeadmin(ctx):
    thread = await ctx.channel.create_thread(name=f"RemoveAdmin - {ctx.author.name}", auto_archive_duration=60)
    await ctx.send(f"Đã tạo thread {thread.mention} để xóa admin!")
    await thread.send("Tag người dùng để xóa khỏi admin:")
    msg = await wait_for_message(ctx.author, thread, "tag admin")
    if not msg:
        return
    if not msg.mentions:
        await thread.send("Vui lòng tag ít nhất một người dùng!")
        return
    for user in msg.mentions:
        if user.id in config["admins"]:
            config["admins"].remove(user.id)
            await thread.send(f"Đã xóa {user.mention} khỏi admin!")
        else:
            await thread.send(f"{user.mention} không phải là admin!")
    save_config(config)


@bot.command()
@check_admin()
async def listadmin(ctx):
    thread = await ctx.channel.create_thread(name=f"ListAdmin - {ctx.author.name}", auto_archive_duration=60)
    await ctx.send(f"Đã tạo thread {thread.mention} để xem danh sách admin!")
    admins = "\n".join([f"<@{admin_id}>" for admin_id in config["admins"]]) or "Không có admin"
    embed = discord.Embed(title="Danh Sách Admin", description=admins, color=discord.Color.green())
    await thread.send(embed=embed)


@bot.command()
async def uptime(ctx):
    thread = await ctx.channel.create_thread(name=f"Uptime - {ctx.author.name}", auto_archive_duration=60)
    await ctx.send(f"Đã tạo thread {thread.mention} để xem thời gian hoạt động!")
    uptime_seconds = time.time() - start_time
    hours, remainder = divmod(int(uptime_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    await thread.send(f"Bot đã chạy được: {hours}h {minutes}m {seconds}s")


@bot.command()
async def ping(ctx):
    thread = await ctx.channel.create_thread(name=f"Ping - {ctx.author.name}", auto_archive_duration=60)
    await ctx.send(f"Đã tạo thread {thread.mention} để kiểm tra độ trễ!")
    latency = bot.latency * 1000
    await thread.send(f"Độ trễ: {latency:.2f}ms")


@bot.command()
async def stop(ctx):
    task_id = f"{ctx.author.id}_{ctx.channel.id}"
    if task_id in active_tasks:
        for task in active_tasks[task_id]:
            task.cancel()
        del active_tasks[task_id]
        await ctx.send("Đã dừng lệnh!")
    else:
        await ctx.send("Không có lệnh nào đang chạy trong thread này!")


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if not interaction.data or "custom_id" not in interaction.data:
        return
    if interaction.data["custom_id"].startswith("menu_select_"):
        user_id = int(interaction.data["custom_id"].split("_")[-1])
        if interaction.user.id != user_id:
            await interaction.response.send_message("Bạn không có quyền sử dụng menu này!", ephemeral=True)
            return
        selected = interaction.data["values"][0]
        await interaction.response.send_message("Nhập tên cho thread (ví dụ: 20-3):", ephemeral=True)
        thread_name_msg = await wait_for_message(interaction.user, interaction.channel, "thread name")
        if not thread_name_msg:
            return
        thread_name = thread_name_msg.content.strip() or f"{selected.upper()} - {interaction.user.name}"
        thread = await interaction.channel.create_thread(name=thread_name, auto_archive_duration=60)
        await interaction.followup.send(f"Đã tạo thread {thread.mention} để chạy lệnh {selected}!", ephemeral=True)
        
        if selected in ["treo", "nhay", "nhay2c", "fake", "reo", "treoanh"]:
            await start_spam_command(interaction.user, thread, selected)
        elif selected == "join":
            await start_join_command(interaction.user, thread)
        elif selected == "checktoken":
            await thread.send("Dán các token (1 dòng 1 token):")
            await checktoken_command(interaction.user, thread)
        elif selected == "setfile":
            await thread.send("Nhập tên file tin nhắn (.txt):")
            await setfile_command(interaction.user, thread)
        elif selected == "addadmin":
            await thread.send("Tag người dùng để thêm làm admin:")
            await addadmin_command(interaction.user, thread)
        elif selected == "removeadmin":
            await thread.send("Tag người dùng để xóa khỏi admin:")
            await removeadmin_command(interaction.user, thread)
        elif selected == "listadmin":
            await listadmin_command(interaction.user, thread)
        elif selected == "uptime":
            await uptime_command(interaction.user, thread)
        elif selected == "ping":
            await ping_command(interaction.user, thread)


async def start_spam_command(user, thread, command):
    if user.id not in config["admins"]:
        await thread.send("Bạn không có quyền sử dụng lệnh này!")
        return
    
    semaphore = asyncio.Semaphore(3)
    task_id = f"{user.id}_{thread.id}"
    active_tasks[task_id] = []

    async def collect_inputs():
        inputs = {}
        await thread.send("Nhập ID kênh (cách nhau bởi dấu phẩy):")
        channel_ids_msg = await wait_for_message(user, thread, "ID kênh")
        if not channel_ids_msg:
            return None
        inputs["channel_ids"] = [cid.strip() for cid in channel_ids_msg.content.split(',') if cid.strip().isdigit()]
        if not inputs["channel_ids"]:
            await thread.send("Không có ID kênh hợp lệ!")
            return None
        
        if command in ["nhay", "nhay2c", "fake"]:
            await thread.send("Bạn muốn tag người dùng? (y/n):")
            inputs["mention_user"] = (await wait_for_message(user, thread, "tag người dùng")).content.lower() == 'y'
            if inputs["mention_user"]:
                await thread.send("Nhập ID người dùng (cách nhau bởi dấu phẩy):")
                inputs["user_ids"] = (await wait_for_message(user, thread, "ID người dùng")).content.split(',')
                inputs["user_ids"] = [uid.strip() for uid in inputs["user_ids"] if uid.strip().isdigit()]
            else:
                inputs["user_ids"] = []
        elif command == "reo":
            await thread.send("Nhập tên cần réo:")
            inputs["name_to_call"] = (await wait_for_message(user, thread, "tên réo")).content.strip()
            await thread.send("Bạn muốn tag người dùng? (y/n):")
            inputs["mention_user"] = (await wait_for_message(user, thread, "tag người dùng")).content.lower() == 'y'
            if inputs["mention_user"]:
                await thread.send("Nhập ID người dùng (cách nhau bởi dấu phẩy):")
                inputs["user_ids"] = (await wait_for_message(user, thread, "ID người dùng")).content.split(',')
                inputs["user_ids"] = [uid.strip() for uid in inputs["user_ids"] if uid.strip().isdigit()]
            else:
                inputs["user_ids"] = []
        elif command == "treoanh":
            await thread.send("Nhập link ảnh:")
            inputs["image_url"] = (await wait_for_message(user, thread, "link ảnh")).content.strip()
        
        await thread.send("Dán các token (1 dòng 1 token):")
        tokens_msg = await wait_for_message(user, thread, "tokens")
        if not tokens_msg:
            return None
        tokens = [t.strip() for t in tokens_msg.content.splitlines() if t.strip()]
        valid_tokens = []
        for token in tokens:
            if await validate_token(token):
                valid_tokens.append(token)
            else:
                await thread.send(f"Token không hợp lệ: {token[:5]}...{token[-5:]}")
                log_error(f"Token {token[:5]}...{token[-5:]} không hợp lệ")
        if not valid_tokens:
            await thread.send("Không có token hợp lệ!")
            return None
        
        await thread.send("Nhập delay (giây):")
        delay_msg = await wait_for_message(user, thread, "delay")
        if not delay_msg:
            return None
        try:
            delay = float(delay_msg.content)
            if delay <= 0:
                raise ValueError
        except ValueError:
            await thread.send("Delay không hợp lệ!")
            return None
        
        await thread.send("Dùng delay ngẫu nhiên? (y/n):")
        use_random_delay_msg = await wait_for_message(user, thread, "random delay")
        if not use_random_delay_msg:
            return None
        use_random_delay = use_random_delay_msg.content.lower() == 'y'
        min_delay = max_delay = delay
        if use_random_delay:
            await thread.send("Nhập delay thấp nhất (giây):")
            min_delay_msg = await wait_for_message(user, thread, "min delay")
            if not min_delay_msg:
                return None
            try:
                min_delay = float(min_delay_msg.content)
                if min_delay <= 0:
                    raise ValueError
            except ValueError:
                await thread.send("Delay thấp nhất không hợp lệ!")
                return None
            await thread.send("Nhập delay cao nhất (giây):")
            max_delay_msg = await wait_for_message(user, thread, "max delay")
            if not max_delay_msg:
                return None
            try:
                max_delay = float(max_delay_msg.content)
                if max_delay < min_delay:
                    await thread.send("Delay cao nhất phải lớn hơn hoặc bằng delay thấp nhất!")
                    return None
            except ValueError:
                await thread.send("Delay cao nhất không hợp lệ!")
                return None
        
        await thread.send("Dùng chữ in đậm? (y/n):")
        bold_text_msg = await wait_for_message(user, thread, "bold text")
        if not bold_text_msg:
            return None
        bold_text = bold_text_msg.content.lower() == 'y'
        
        message_file = config["message_file"] if command != "nhay2c" else "2c.txt"
        if not os.path.exists(message_file):
            await thread.send(f"File `{message_file}` không tồn tại!")
            return None
        with open(message_file, 'r', encoding='utf-8') as f:
            if command == "treo":
                messages = [f.read().strip()]
            else:
                messages = [line.strip() for line in f.read().splitlines() if line.strip()]
        
        return {
            "channel_ids": inputs.get("channel_ids", []),
            "tokens": valid_tokens,
            "delay": delay,
            "use_random_delay": use_random_delay,
            "min_delay": min_delay,
            "max_delay": max_delay,
            "bold_text": bold_text,
            "messages": messages,
            "mention_user": inputs.get("mention_user", False),
            "user_ids": inputs.get("user_ids", []),
            "name_to_call": inputs.get("name_to_call"),
            "image_url": inputs.get("image_url")
        }
    
    inputs = await collect_inputs()
    if not inputs:
        return
    
    tasks = []
    for channel_id in inputs["channel_ids"]:
        for i, token in enumerate(inputs["tokens"]):
            if command == "treo":
                tasks.append(spam_message(thread, token, channel_id, inputs["messages"][i % len(inputs["messages"])], inputs["delay"], inputs["use_random_delay"], inputs["min_delay"], inputs["max_delay"], semaphore, inputs["bold_text"]))
            elif command in ["nhay", "nhay2c"]:
                tasks.append(spam_message_nhay(thread, token, channel_id, inputs["messages"], inputs["delay"], inputs["use_random_delay"], inputs["min_delay"], inputs["max_delay"], inputs["mention_user"], inputs["user_ids"], semaphore, inputs["bold_text"]))
            elif command in ["fake", "reo"]:
                tasks.append(fake_typing_and_send_message(thread, token, channel_id, inputs["messages"], inputs["delay"], inputs["use_random_delay"], inputs["min_delay"], inputs["max_delay"], inputs["mention_user"], inputs["user_ids"], semaphore, inputs["bold_text"], inputs["name_to_call"]))
            elif command == "treoanh":
                tasks.append(spam_image(thread, token, channel_id, inputs["messages"][i % len(inputs["messages"])], inputs["image_url"], inputs["delay"], inputs["use_random_delay"], inputs["min_delay"], inputs["max_delay"], semaphore, inputs["bold_text"]))
    
    active_tasks[task_id] = tasks
    await asyncio.gather(*tasks)


async def start_join_command(user, thread):
    if user.id not in config["admins"]:
        await thread.send("Bạn không có quyền sử dụng lệnh này!")
        return
    
    task_id = f"{user.id}_{thread.id}"
    active_tasks[task_id] = []
    
    await thread.send("Nhập link mời server:")
    invite_msg = await wait_for_message(user, thread, "link mời")
    if not invite_msg:
        return
    invite_link = invite_msg.content.strip()
    
    await thread.send("Dán các token (1 dòng 1 token):")
    tokens_msg = await wait_for_message(user, thread, "tokens")
    if not tokens_msg:
        return
    tokens = [t.strip() for t in tokens_msg.content.splitlines() if t.strip()]
    valid_tokens = []
    for token in tokens:
        if await validate_token(token):
            valid_tokens.append(token)
        else:
            await thread.send(f"Token không hợp lệ: {token[:5]}...{token[-5:]}")
            log_error(f"Token {token[:5]}...{token[-5:]} không hợp lệ")
    if not valid_tokens:
        await thread.send("Không có token hợp lệ!")
        return
    
    await thread.send("Nhập delay (giây):")
    delay_msg = await wait_for_message(user, thread, "delay")
    if not delay_msg:
        return
    try:
        delay = float(delay_msg.content)
        if delay <= 0:
            raise ValueError
    except ValueError:
        await thread.send("Delay không hợp lệ!")
        return
    
    task = asyncio.create_task(join_thread(thread, valid_tokens, invite_link, delay, user.id))
    active_tasks[task_id].append(task)
    await task


async def checktoken_command(user, thread):
    if user.id not in config["admins"]:
        await thread.send("Bạn không có quyền sử dụng lệnh này!")
        return
    await thread.send("Dán các token (1 dòng 1 token):")
    tokens_msg = await wait_for_message(user, thread, "tokens")
    if not tokens_msg:
        return
    tokens = [t.strip() for t in tokens_msg.content.splitlines() if t.strip()]
    if not tokens:
        await thread.send("Không có token nào được cung cấp!")
        return
    valid_tokens = []
    invalid_tokens = []
    for token in tokens:
        if await validate_token(token):
            valid_tokens.append(token)
        else:
            invalid_tokens.append(token)
            log_error(f"Token {token[:5]}...{token[-5:]} không hợp lệ")
    embed = discord.Embed(title="Kết Quả Kiểm Tra Token", color=discord.Color.blue())
    embed.add_field(name="Token Sống", value="\n".join([f"`{t}`" for t in valid_tokens]) or "Không có", inline=False)
    embed.add_field(name="Token Chết", value="\n".join([f"`{t}`" for t in invalid_tokens]) or "Không có", inline=False)
    view = CopyTokensView(valid_tokens) if valid_tokens else None
    await thread.send(embed=embed, view=view)

async def setfile_command(user, thread):
    if user.id not in config["admins"]:
        await thread.send("Bạn không có quyền sử dụng lệnh này!")
        return
    await thread.send("Nhập tên file tin nhắn (.txt):")
    file_msg = await wait_for_message(user, thread, "tên file")
    if not file_msg:
        return
    file_name = file_msg.content.strip()
    if not file_name.endswith('.txt'):
        file_name += '.txt'
    if not os.path.exists(file_name):
        await thread.send(f"File `{file_name}` không tồn tại!")
        return
    config["message_file"] = file_name
    save_config(config)
    await thread.send(f"Đã đặt file tin nhắn: `{file_name}`")

async def addadmin_command(user, thread):
    if user.id not in config["admins"]:
        await thread.send("Bạn không có quyền sử dụng lệnh này!")
        return
    await thread.send("Tag người dùng để thêm làm admin:")
    msg = await wait_for_message(user, thread, "tag admin")
    if not msg:
        return
    if not msg.mentions:
        await thread.send("Vui lòng tag ít nhất một người dùng!")
        return
    for user in msg.mentions:
        if user.id not in config["admins"]:
            config["admins"].append(user.id)
            await thread.send(f"Đã thêm {user.mention} làm admin!")
        else:
            await thread.send(f"{user.mention} đã là admin!")
    save_config(config)

async def removeadmin_command(user, thread):
    if user.id not in config["admins"]:
        await thread.send("Bạn không có quyền sử dụng lệnh này!")
        return
    await thread.send("Tag người dùng để xóa khỏi admin:")
    msg = await wait_for_message(user, thread, "tag admin")
    if not msg:
        return
    if not msg.mentions:
        await thread.send("Vui lòng tag ít nhất một người dùng!")
        return
    for user in msg.mentions:
        if user.id in config["admins"]:
            config["admins"].remove(user.id)
            await thread.send(f"Đã xóa {user.mention} khỏi admin!")
        else:
            await thread.send(f"{user.mention} không phải là admin!")
    save_config(config)

async def listadmin_command(user, thread):
    if user.id not in config["admins"]:
        await thread.send("Bạn không có quyền sử dụng lệnh này!")
        return
    admins = "\n".join([f"<@{admin_id}>" for admin_id in config["admins"]]) or "Không có admin"
    embed = discord.Embed(title="Danh Sách Admin", description=admins, color=discord.Color.green())
    await thread.send(embed=embed)

async def uptime_command(user, thread):
    uptime_seconds = time.time() - start_time
    hours, remainder = divmod(int(uptime_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    await thread.send(f"Bot đã chạy được: {hours}h {minutes}m {seconds}s")

async def ping_command(user, thread):
    latency = bot.latency * 1000
    await thread.send(f"Độ trễ: {latency:.2f}ms")


bot.run(bot_token)