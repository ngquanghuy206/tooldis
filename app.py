import nextcord
from nextcord.ext import commands
from nextcord import ui, Interaction, SlashOption, SelectOption
import yt_dlp
import asyncio
import requests
import re
import time
import logging
from typing import Optional, Dict, List
from dataclasses import dataclass
from collections import deque
import random
from datetime import datetime, timedelta
#BẢNG GIÁ MENU TOOL BY QUANG HUY
#THUÊ TOOL BOT CHỈ TỪ 10K VÀ CÒN NHIỀU DỊCH VỤ KHÁC

#TOOL MESSENGER
#• Treo cơ bản: 50k | Full Script: 350K
#• Treo gộp: 350K | Full Script: 550K
#• Treo có Cookie V1: 250K | Full Script: 450K
#• Treo đã Cookie V2 (New – như UG Phone): 450K | Full Script: 800K
#→ Các chức năng khác: Liên hệ Quang Huy

#TOOL ZALO
#• Treo cơ bản: 50K | 1 chức năng | Full Script: 100K
#• Treo gộp V1: 250K | Full Script: 350K
#• Treo gộp V2: 450K | Full Script: 750K
#• Tool giải trí: 50K – 500K

#TOOL TELEGRAM
#• Treo thường: 150K | Full Script: 300K
#• Treo đa token đa box V1: 250K | Full Script: 400K
#• Treo đa token VIP gộp mới nhất (chạy như UG Phone): 400K | Full Script: 1 triệu
#• Tool giải trí: 100K – 700K
#→ Các chức năng khác: Liên hệ Quang Huy

#TOOL DISCORD
#• Treo cơ bản: 150K | Full Script: 250K
#• Treo gộp: 350K | Full Script: 650K
#• Tool Join: 350K | Full Script: 750K
#→ Các chức năng khác: Liên hệ Quang Huy

#TOOL INSTAGRAM
#• Treo cơ bản: 250K | Full Script: 550K
#• Treo nhiều acc V1: 350K | Full Script: 600K
#• Treo nhiều acc V2: 550K | Full Script: 950K
#→ Các chức năng khác: Liên hệ Quang Huy

#MENU BOT
#• BOT Messenger: 350K – 2M5
#• BOT Zalo: 450K – 3M5
#• BOT Discord: 350K – 2M5
#• BOT Telegram: 350K – 2M5
#• BOT Instagram: 400K – 2M5
#• BOT TikTok: 550K – 3M2
#• BOT Zalo All-in-One: 50K – 5 triệu
#→ Còn nhiều bot khác – xin vui lòng liên hệ admin

#CÒN 40+ APP KHÁC CHƯA LIỆT KÊ – VUI LÒNG INBOX ĐỂ THAM KHẢO

#NHẬN CODE TOOL • BOT • WEB • APP THEO YÊU CẦU
#→ Giá chỉ từ 250K – 10 triệu 500K

#𝐓𝐇𝐎̂𝐍𝐆 𝐓𝐈𝐍 𝐋𝐈𝐄̂𝐍 𝐇𝐄̣̂

#➤ 𝐴𝐷𝑀𝐼𝑁: [ 𝑁𝐺𝑈𝑌𝐸̂̃𝑁 𝑄𝑈𝐴𝑁𝐺 𝐻𝑈𝑌 • 𝐷𝑍𝐼 ]
#• Vai trò: Trung gian giao dịch – coder AI Tool-Bot
#• Zalo: [0904562214]
#• Group: https://zalo.me/g/bhxmor546
#• Facebook: https://www.facebook.com/profile.php?id=100077964955704

def get_config(prompt):
    return input(prompt)


BOT_TOKEN = get_config('Nhập token bot: ')
ADMIN_ID = int(get_config('Nhập ID admin: '))


SPOTIFY_CLIENT_ID = "ead3b50eb1e04e3cb775ef8962385af5"
SPOTIFY_CLIENT_SECRET = "73bf6a716aa548868bf13abcde0180b4"
YOUTUBE_API_KEY = "AIzaSyCYghdfUT94l3CwPoMF12s4yDumsSZvKUs"
MAX_QUEUE_SIZE = 100
BOT_VERSION = "2.6"
UPDATE_TIME = "06/07/2025"
BOT_START_TIME = datetime.now()

intents = nextcord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nextcord.music_bot')

@bot.event
async def on_ready():
    logger.info(f'Bot đã kết nối với tên {bot.user.name}#{bot.user.discriminator} (ID: {bot.user.id})')
    
    
    bot.add_view(MusicControls(0))  
    
    try:
        
        import nextcord
        if nextcord.__version__.startswith('1.'):
            logger.warning("Phiên bản nextcord cũ (<2.0). Dùng sync_application_commands().")
            await bot.sync_application_commands()
        else:
            logger.info("Phiên bản nextcord >= 2.0. Dùng tree.sync().")
            synced = await bot.tree.sync()
            logger.info(f'Đã đồng bộ {len(synced)} lệnh.')
            for command in synced:
                logger.info(f' - {command.name}: {command.description}')
    except Exception as e:
        logger.error(f'Lỗi khi đồng bộ lệnh: {e}')
        logger.info('Vui lòng kiểm tra phiên bản nextcord (pip show nextcord) và nâng cấp nếu cần (pip install -U nextcord).')
    
    logger.info('Bot đã sẵn sàng nhận lệnh.')
    bot.loop.create_task(check_inactivity())
    bot.loop.create_task(cleanup_inactive_players())

@dataclass
class Song:
    title: str
    url: str
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    requester: Optional[str] = None
    original_query: Optional[str] = None

def format_duration(duration: Optional[int]) -> str:
    if duration is None or duration <= 0:
        return "Trực tiếp/Không xác định"
    
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"

class MusicPlayer:
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.queue = deque()
        self.current_song: Optional[Song] = None
        self.previous_songs = deque(maxlen=10)  
        self.is_playing = False
        self.is_paused = False
        self.loop_mode = 0
        self.volume = 0.5
        self.last_activity = time.time()
        self.cached_songs: Dict[str, Song] = {}
        self.text_channel: Optional[nextcord.TextChannel] = None
        
    def add_song(self, song: Song):
        if len(self.queue) >= MAX_QUEUE_SIZE:
            raise Exception(f"Hàng đợi đã đầy (tối đa {MAX_QUEUE_SIZE} bài hát)")
        self.queue.append(song)
        self.last_activity = time.time()
        
    def get_next_song(self) -> Optional[Song]:
        if self.loop_mode == 1 and self.current_song:
            return self.current_song
        elif self.loop_mode == 2 and self.current_song:
            self.queue.append(self.current_song)
        return self.queue.popleft() if self.queue else None
    
    def get_previous_song(self) -> Optional[Song]:
        if self.previous_songs:
            return self.previous_songs[-1]
        return None
    
    def clear_queue(self):
        self.queue.clear()
        self.previous_songs.clear()
        
    def skip_song(self):
        if self.loop_mode == 1:
            self.loop_mode = 0
        return self.get_next_song()
    
    def shuffle_queue(self):
        queue_list = list(self.queue)
        random.shuffle(queue_list)
        self.queue = deque(queue_list)
    
    def remove_song(self, position: int) -> Optional[Song]:
        if 0 < position <= len(self.queue):
            return self.queue.pop(position - 1)
        return None

music_players: Dict[int, MusicPlayer] = {}
spotify_token_cache = {"token": None, "expires_at": 0}
search_cache = {}

def get_music_player(guild_id: int) -> MusicPlayer:
    if guild_id not in music_players:
        music_players[guild_id] = MusicPlayer(guild_id)
    return music_players[guild_id]

def get_spotify_token() -> Optional[str]:
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return None
    current_time = time.time()
    if spotify_token_cache["token"] and current_time < spotify_token_cache["expires_at"]:
        return spotify_token_cache["token"]
    try:
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={
                'grant_type': 'client_credentials',
                'client_id': SPOTIFY_CLIENT_ID,
                'client_secret': SPOTIFY_CLIENT_SECRET
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        token = data.get('access_token')
        expires_in = data.get('expires_in', 3600)
        spotify_token_cache["token"] = token
        spotify_token_cache["expires_at"] = current_time + expires_in - 60
        return token
    except Exception as e:
        logger.error(f"Lỗi khi lấy token Spotify: {e}")
        return None

def get_spotify_track_info(track_id: str) -> Optional[Dict]:
    token = get_spotify_token()
    if not token:
        return None
    try:
        response = requests.get(
            f'https://api.spotify.com/v1/tracks/{track_id}',
            headers={'Authorization': f'Bearer {token}'},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Lỗi khi lấy thông tin từ Spotify: {e}")
        return None

def clean_youtube_url(url: str) -> str:
    if 'youtube.com/watch' in url:
        match = re.search(r'[?&]v=([^&]+)', url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/watch?v={video_id}"
    elif 'youtu.be/' in url:
        match = re.search(r'youtu\.be/([^?&]+)', url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/watch?v={video_id}"
    return url

def search_youtube_with_cache(query: str, max_results: int = 5) -> List[Dict]:
    cache_key = query.lower().strip()
    if cache_key in search_cache:
        logger.info(f"Sử dụng kết quả bộ nhớ đệm cho: {query}")
        return search_cache[cache_key]
    
    if YOUTUBE_API_KEY:
        try:
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'key': YOUTUBE_API_KEY,
                'fields': 'items(id(videoId),snippet(title,thumbnails))'
            }
            response = requests.get(
                "https://www.googleapis.com/youtube/v3/search",
                params=params,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            results = [
                {
                    'url': f"https://youtu.be/{item['id']['videoId']}",
                    'title': item['snippet']['title'],
                    'thumbnail': item['snippet']['thumbnails']['default']['url']
                }
                for item in data.get('items', [])
            ]
            search_cache[cache_key] = results
            logger.info(f"Kết quả YouTube API đã được lưu vào bộ nhớ đệm cho: {query}")
            return results
        except Exception as e:
            logger.error(f"Lỗi trong YouTube API: {e}")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': True,
        'socket_timeout': 15,
        'cookiefile': 'cookies.txt'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
            results = [
                {
                    'url': entry['webpage_url'],
                    'title': entry['title'],
                    'thumbnail': entry.get('thumbnail')
                }
                for entry in info.get('entries', [])
            ]
            search_cache[cache_key] = results
            logger.info(f"Kết quả yt-dlp đã được lưu vào bộ nhớ đệm cho: {query}")
            return results
    except Exception as e:
        logger.error(f"Lỗi trong tìm kiếm yt-dlp: {e}")
        return []

async def extract_song_info(source: str, requester: str, guild_id: int) -> Optional[Song]:
    player = get_music_player(guild_id)
    
    if any(domain in source for domain in ['youtube.com', 'youtu.be']):
        source = clean_youtube_url(source)
    
    cache_key = source.lower().strip()
    if cache_key in player.cached_songs:
        cached_song = player.cached_songs[cache_key]
        return Song(
            title=cached_song.title,
            url=cached_song.url,
            duration=cached_song.duration,
            thumbnail=cached_song.thumbnail,
            requester=requester,
            original_query=cached_song.original_query
        )
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt',
        'extract_flat': False,
        'socket_timeout': 15,
        'retries': 3,
        'live_from_start': True,
        'wait_for_video': (1, 5),
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(source, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            
            duration = info.get('duration')
            if duration is not None and duration <= 0:
                duration = None
                
            song = Song(
                title=info.get('title', 'Không rõ tiêu đề'),
                url=info.get('url') or next(
                    (f['url'] for f in info.get('formats', []) if f.get('url')),
                    source
                ),
                duration=duration,
                thumbnail=info.get('thumbnail'),
                requester=requester,
                original_query=source
            )
            player.cached_songs[cache_key] = song
            logger.info(f"Đã lưu bài hát vào bộ nhớ đệm: {song.title}")
            return song
    except Exception as e:
        logger.error(f"Lỗi khi trích xuất thông tin bài hát: {e}")
        return None

class MusicControls(ui.View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=None)
        self.guild_id = guild_id

    async def interaction_check(self, interaction: Interaction) -> bool:
        if not interaction.user.voice:
            await interaction.response.send_message("❌ Bạn phải ở trong kênh thoại để sử dụng nút này", ephemeral=True)
            return False
        return True

    @ui.button(label="Tạm dừng", style=nextcord.ButtonStyle.grey, emoji="⏸️", custom_id="music_pause")
    async def pause(self, interaction: Interaction, button: ui.Button):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            player = get_music_player(self.guild_id)
            player.is_paused = True
            await interaction.response.send_message("⏸️ Đã tạm dừng", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Không có bài hát nào đang phát", ephemeral=True)

    @ui.button(label="Tiếp tục", style=nextcord.ButtonStyle.grey, emoji="▶️", custom_id="music_resume")
    async def resume(self, interaction: Interaction, button: ui.Button):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            player = get_music_player(self.guild_id)
            player.is_paused = False
            await interaction.response.send_message("▶️ Đã tiếp tục", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Không có bài hát nào đang tạm dừng", ephemeral=True)

    @ui.button(label="Bỏ qua", style=nextcord.ButtonStyle.grey, emoji="⏭️", custom_id="music_skip")
    async def skip(self, interaction: Interaction, button: ui.Button):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ Đã bỏ qua", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Không có bài hát nào đang phát", ephemeral=True)

    @ui.button(label="Bài trước", style=nextcord.ButtonStyle.grey, emoji="⏮️", custom_id="music_previous")
    async def previous(self, interaction: Interaction, button: ui.Button):
        voice_client = interaction.guild.voice_client
        player = get_music_player(self.guild_id)
        if voice_client and player.previous_songs:
            player.queue.appendleft(player.current_song)
            player.current_song = player.previous_songs.pop()
            voice_client.stop()
            await interaction.response.send_message("⏮️ Đã quay lại bài trước", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Không có bài hát trước đó", ephemeral=True)

    @ui.button(label="Bài tiếp", style=nextcord.ButtonStyle.grey, emoji="⏭️", custom_id="music_next")
    async def next(self, interaction: Interaction, button: ui.Button):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ Đã chuyển bài tiếp theo", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Không có bài hát nào đang phát", ephemeral=True)

    @ui.button(label="Tăng âm lượng", style=nextcord.ButtonStyle.grey, emoji="🔊", custom_id="music_volume_up")
    async def volume_up(self, interaction: Interaction, button: ui.Button):
        player = get_music_player(self.guild_id)
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            current_volume = player.volume * 100
            new_volume = min(current_volume + 10, 100)
            player.volume = new_volume / 100
            if voice_client.source:
                voice_client.source.volume = player.volume
            await interaction.response.send_message(f"🔊 Âm lượng tăng lên {int(new_volume)}%", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Không có bài hát nào đang phát", ephemeral=True)

    @ui.button(label="Giảm âm lượng", style=nextcord.ButtonStyle.grey, emoji="🔉", custom_id="music_volume_down")
    async def volume_down(self, interaction: Interaction, button: ui.Button):
        player = get_music_player(self.guild_id)
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            current_volume = player.volume * 100
            new_volume = max(current_volume - 10, 0)
            player.volume = new_volume / 100
            if voice_client.source:
                voice_client.source.volume = player.volume
            await interaction.response.send_message(f"🔉 Âm lượng giảm xuống {int(new_volume)}%", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Không có bài hát nào đang phát", ephemeral=True)

    @ui.button(label="Lặp lại", style=nextcord.ButtonStyle.grey, emoji="🔂", custom_id="music_loop")
    async def loop(self, interaction: Interaction, button: ui.Button):
        player = get_music_player(self.guild_id)
        if player.loop_mode == 0:
            player.loop_mode = 1
            await interaction.response.send_message("🔂 Đã bật lặp lại cho bài hát hiện tại", ephemeral=True)
        else:
            player.loop_mode = 0
            await interaction.response.send_message("🔁 Đã tắt lặp lại", ephemeral=True)

    @ui.button(label="Xáo trộn", style=nextcord.ButtonStyle.grey, emoji="🔀", custom_id="music_shuffle")
    async def shuffle(self, interaction: Interaction, button: ui.Button):
        player = get_music_player(self.guild_id)
        if not player.queue:
            await interaction.response.send_message("❌ Hàng đợi trống", ephemeral=True)
        else:
            player.shuffle_queue()
            await interaction.response.send_message("🔀 Đã xáo trộn hàng đợi", ephemeral=True)

    @ui.button(label="Dừng", style=nextcord.ButtonStyle.red, emoji="🛑", custom_id="music_stop")
    async def stop(self, interaction: Interaction, button: ui.Button):
        player = get_music_player(self.guild_id)
        voice_client = interaction.guild.voice_client
        if voice_client:
            voice_client.stop()
            player.clear_queue()
            player.is_playing = False
            player.current_song = None
            await interaction.response.send_message("🛑 Đã dừng phát nhạc và xóa hàng đợi", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Không có bài hát nào đang phát", ephemeral=True)

class SongSelect(ui.Select):
    def __init__(self, songs: List[Dict], guild_id: int):
        self.guild_id = guild_id
        options = [
            SelectOption(label=song['title'][:100], value=song['url'], description=f"Thêm: {song['title'][:50]}")
            for song in songs
        ]
        super().__init__(placeholder="Chọn bài hát để thêm vào hàng đợi", options=options, custom_id="song_select")

    async def callback(self, interaction: Interaction):
        player = get_music_player(self.guild_id)
        song = await extract_song_info(self.values[0], interaction.user.display_name, self.guild_id)
        if not song:
            await interaction.response.send_message("❌ Không thể thêm bài hát", ephemeral=True)
            return
        
        player.add_song(song)
        embed = nextcord.Embed(
            title="➕ Đã thêm vào hàng đợi",
            description=f"**{song.title}**\n📍 Vị trí trong hàng đợi: {len(player.queue)}",
            color=0x00ff00
        )
        embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class SearchView(ui.View):
    def __init__(self, songs: List[Dict], guild_id: int):
        super().__init__(timeout=60)
        self.add_item(SongSelect(songs, guild_id))

async def play_next_song(voice_client, guild_id: int):
    player = get_music_player(guild_id)
    if not voice_client.is_connected():
        return
    next_song = player.get_next_song()
    if not next_song:
        player.is_playing = False
        player.current_song = None
        return
    try:
        if player.loop_mode == 1 and player.current_song and next_song == player.current_song:
            audio_url = next_song.url
        else:
            if time.time() - player.last_activity > 300:
                fresh_song = await extract_song_info(next_song.original_query or next_song.url, next_song.requester, guild_id)
                if fresh_song:
                    next_song = fresh_song
            audio_url = next_song.url
        if player.current_song:
            player.previous_songs.append(player.current_song)
        player.current_song = next_song
        player.is_playing = True
        player.last_activity = time.time()

        duration_str = format_duration(next_song.duration)
        embed = nextcord.Embed(
            title="🎵 Đang phát",
            description=f"**{next_song.title}**\n"
                        f"⏱️ Thời lượng: {duration_str}\n"
                        f"Yêu cầu bởi: {next_song.requester}",
            color=0x00ff00
        )
        embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
        if next_song.thumbnail:
            embed.set_thumbnail(url=next_song.thumbnail)
        
        if player.text_channel:
            try:
                await player.text_channel.send(embed=embed, view=MusicControls(guild_id))
            except nextcord.HTTPException as e:
                logger.error(f"Không thể gửi tin nhắn phát nhạc: {e}")
        
        def after_playing(error):
            if error:
                logger.error(f'Lỗi khi phát nhạc: {error}')
            coro = play_next_song(voice_client, guild_id)
            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
            try:
                fut.result()
            except Exception as e:
                logger.error(f'Lỗi khi lên lịch bài hát tiếp theo: {e}')
        
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin',
            'options': '-vn'
        }
        
        source = nextcord.PCMVolumeTransformer(
            nextcord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
        )
        source.volume = player.volume
        voice_client.play(source, after=after_playing)
    except Exception as e:
        logger.error(f"Lỗi khi phát bài hát: {e}")
        player.is_playing = False

async def check_inactivity():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(60)
        current_time = time.time()
        for guild in list(bot.guilds):
            player = get_music_player(guild.id)
            if (current_time - player.last_activity > 600 and 
                not player.is_playing):
                if voice_client := guild.voice_client:
                    await voice_client.disconnect()
                    logger.info(f"Ngắt kết nối do không hoạt động ở {guild.name}")

async def cleanup_inactive_players():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(3600)
        current_time = time.time()
        for guild_id, player in list(music_players.items()):
            if current_time - player.last_activity > 3600:
                del music_players[guild_id]
                logger.info(f"Đã dọn trình phát không hoạt động của guild {guild_id}")

@bot.slash_command(name='play', description='Phát nhạc từ YouTube hoặc Spotify')
async def play_command(interaction: Interaction, source: str = SlashOption(description="Link hoặc tên bài hát từ YouTube/Spotify")):
    await interaction.response.defer()
    if not interaction.user.voice:
        return await interaction.followup.send("❌ Bạn phải ở trong kênh thoại để sử dụng lệnh này")
    
    player = get_music_player(interaction.guild_id)
    player.text_channel = interaction.channel
    
    if not interaction.guild.voice_client:
        voice_client = await interaction.user.voice.channel.connect()
    else:
        voice_client = interaction.guild.voice_client
    
    try:
        final_source = source
        if 'spotify.com' in source:
            match = re.search(r'spotify\.com/(?:[A-Za-z0-9_-]+/)*track/([A-Za-z0-9]+)', source)
            if not match:
                return await interaction.followup.send("❌ Liên kết Spotify không hợp lệ.")
            track_id = match.group(1)
            
            track_info = get_spotify_track_info(track_id)
            if not track_info:
                return await interaction.followup.send("❌ Không thể lấy thông tin bài hát từ Spotify.")
            
            query = f"{track_info['name']} {track_info['artists'][0]['name']}"
            final_source = search_youtube_with_cache(query, max_results=1)[0]['url']
        
        if not final_source:
            return await interaction.followup.send("❌ Không thể tìm thấy bài hát trên YouTube.")
        
        if 'spotify.com' not in source and not any(domain in final_source for domain in ['youtube.com', 'youtu.be']):
            final_source = search_youtube_with_cache(source, max_results=1)[0]['url']
            if not final_source:
                return await interaction.followup.send("❌ Không thể tìm thấy bài hát trên YouTube.")
        
        song = await extract_song_info(final_source, interaction.user.display_name, interaction.guild_id)
        if not song:
            return await interaction.followup.send("❌ Không thể xử lý bài hát.")
        
        player.add_song(song)
        
        if not player.is_playing:
            await play_next_song(voice_client, interaction.guild_id)
            duration_str = format_duration(song.duration)
            embed = nextcord.Embed(
                title="🎵 Đang phát",
                description=f"**{song.title}**\n⏱️ Thời lượng: {duration_str}\nYêu cầu bởi: {song.requester}",
                color=0x00ff00
            )
            embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
            if song.thumbnail:
                embed.set_thumbnail(url=song.thumbnail)
            await interaction.followup.send(embed=embed, view=MusicControls(interaction.guild_id))
        else:
            embed = nextcord.Embed(
                title="➕ Đã thêm vào hàng đợi",
                description=f"**{song.title}**\n📍 Vị trí trong hàng đợi: {len(player.queue)}",
                color=0x00ff00
            )
            embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
            await interaction.followup.send(embed=embed)
    
    except Exception as e:
        logger.error(f"Lỗi khi phát nhạc: {e}")
        await interaction.followup.send(f"❌ Lỗi khi phát nhạc: {str(e)}")

@bot.slash_command(name='search', description='Tìm kiếm bài hát trên YouTube')
async def search_command(interaction: Interaction, query: str = SlashOption(description="Từ khóa tìm kiếm bài hát")):
    await interaction.response.defer()
    songs = search_youtube_with_cache(query, max_results=5)
    if not songs:
        return await interaction.followup.send("❌ Không tìm thấy bài hát nào.")
    
    embed = nextcord.Embed(
        title="🔍 Kết quả tìm kiếm",
        description="\n".join(
            f"`{i+1}.` **{song['title']}**" for i, song in enumerate(songs)
        ),
        color=0x00ff00
    )
    embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
    await interaction.followup.send(embed=embed, view=SearchView(songs, interaction.guild_id))

@bot.slash_command(name='queue', description='Hiển thị hàng đợi phát nhạc')
async def queue_command(interaction: Interaction):
    player = get_music_player(interaction.guild_id)
    if not player.current_song and not player.queue:
        return await interaction.response.send_message("📭 Hàng đợi trống")
    
    embed = nextcord.Embed(title="🎵 Hàng đợi phát nhạc", color=0x00ff00)
    embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
    
    if player.current_song:
        loop_indicator = ""
        if player.loop_mode == 1:
            loop_indicator = " 🔂"
        elif player.loop_mode == 2:
            loop_indicator = " 🔁"
        duration_str = format_duration(player.current_song.duration)
        embed.add_field(
            name="🎵 Đang phát:",
            value=f"**{player.current_song.title}**{loop_indicator}\n"
                  f"⏱️ Thời lượng: {duration_str}\n"
                  f"Yêu cầu bởi: {player.current_song.requester}",
            inline=False
        )
        if player.current_song.thumbnail:
            embed.set_thumbnail(url=player.current_song.thumbnail)
    
    if player.queue:
        next_songs = []
        for i, song in enumerate(list(player.queue)[:10], 1):
            duration_str = format_duration(song.duration)
            next_songs.append(f"`{i}.` **{song.title}** - ⏱️ {duration_str} - *{song.requester}*")
        embed.add_field(
            name="📋 Bài hát tiếp theo:",
            value="\n".join(next_songs),
            inline=False
        )
        if len(player.queue) > 10:
            embed.add_field(
                name="",
                value=f"... và {len(player.queue) - 10} bài hát khác",
                inline=False
            )
    
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name='clear', description='Xóa toàn bộ hàng đợi phát nhạc')
async def clear_command(interaction: Interaction):
    player = get_music_player(interaction.guild_id)
    player.clear_queue()
    await interaction.response.send_message("🗑️ Đã xóa hàng đợi")

@bot.slash_command(name='disconnect', description='Ngắt kết nối bot khỏi kênh thoại')
async def disconnect_command(interaction: Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        player = get_music_player(interaction.guild_id)
        player.clear_queue()
        player.is_playing = False
        player.current_song = None
        await voice_client.disconnect()
        await interaction.response.send_message("👋 Đã ngắt kết nối khỏi kênh thoại")
    else:
        await interaction.response.send_message("❌ Bot không ở trong kênh thoại nào")

@bot.slash_command(name='remove', description='Xóa một bài hát khỏi hàng đợi')
async def remove_command(interaction: Interaction, position: int = SlashOption(description="Vị trí bài hát trong hàng đợi")):
    player = get_music_player(interaction.guild_id)
    if not player.queue:
        return await interaction.response.send_message("❌ Hàng đợi trống")
    removed_song = player.remove_song(position)
    if removed_song:
        await interaction.response.send_message(f"🗑️ Đã xóa: **{removed_song.title}**")
    else:
        await interaction.response.send_message("❌ Vị trí không hợp lệ")

@bot.slash_command(name='nowplaying', description='Hiển thị bài hát đang phát')
async def nowplaying_command(interaction: Interaction):
    player = get_music_player(interaction.guild_id)
    if not player.current_song:
        return await interaction.response.send_message("❌ Không có bài hát nào đang phát")
    
    song = player.current_song
    duration_str = format_duration(song.duration)
    embed = nextcord.Embed(
        title="🎵 Đang phát",
        description=f"**{song.title}**\n"
                    f"⏱️ Thời lượng: {duration_str}\n"
                    f"Yêu cầu bởi: {song.requester}",
        color=0x00ff00
    )
    embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)
    await interaction.response.send_message(embed=embed, view=MusicControls(interaction.guild_id))

@bot.slash_command(name='sync', description='Buộc đồng bộ lệnh (chỉ dành cho quản trị viên)')
async def sync_command(interaction: Interaction):
    if interaction.user.id != ADMIN_ID:
        return await interaction.response.send_message("❌ Chỉ quản trị viên có thể sử dụng lệnh này", ephemeral=True)
    
    await interaction.response.defer()
    try:
        import nextcord
        if nextcord.__version__.startswith('1.'):
            await bot.sync_application_commands()
            await interaction.followup.send("✅ Đã đồng bộ lệnh (phiên bản nextcord cũ)")
        else:
            synced = await bot.tree.sync()
            await interaction.followup.send(f"✅ Đã đồng bộ thành công {len(synced)} lệnh")
    except Exception as e:
        await interaction.followup.send(f"❌ Lỗi khi đồng bộ lệnh: {e}")

@bot.slash_command(name='ping', description='Kiểm tra độ trễ của bot')
async def ping_command(interaction: Interaction):
    latency = round(bot.latency * 1000)
    embed = nextcord.Embed(
        title="🏓 Pong!",
        description=f"Độ trễ: **{latency}ms**",
        color=0x00ff00
    )
    embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name='uptime', description='Hiển thị thời gian bot đã hoạt động')
async def uptime_command(interaction: Interaction):
    uptime = datetime.now() - BOT_START_TIME
    days, seconds = uptime.days, uptime.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    uptime_str = f"{days} ngày, {hours} giờ, {minutes} phút, {seconds} giây"
    embed = nextcord.Embed(
        title="⏰ Thời gian hoạt động",
        description=f"Bot đã chạy được: **{uptime_str}**",
        color=0x00ff00
    )
    embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name='bank', description='Hiển thị thông tin tài khoản ngân hàng của admin')
async def bank_command(interaction: Interaction):
    embed = nextcord.Embed(
        title="🏦 Thông tin ngân hàng",
        description="Thông tin tài khoản ngân hàng của admin Nguyễn Quang Huy (Dzi):\n"
                    "- **Ngân hàng**: [Nhấn tại đây](http://giaodich-profile.onlinewebshop.net/)\n"
                    "- **Số tài khoản**: [Nhấn tại đây](http://giaodich-profile.onlinewebshop.net/)\n"
                    "- **Chủ tài khoản**: Nguyễn Quang Huy\n"
                    "- **Chi nhánh**: [Nhấn tại đây](http://giaodich-profile.onlinewebshop.net/)\n"
                    "**Lưu ý**: Vui lòng kiểm tra kỹ thông tin trước khi chuyển khoản!",
        color=0x00ff00
    )
    embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name='profile', description='Hiển thị thông tin liên hệ của admin')
async def profile_command(interaction: Interaction):
    embed = nextcord.Embed(
        title="👤 Hồ sơ admin",
        description="Thông tin liên hệ của admin Nguyễn Quang Huy (Dzi):\n"
                    "- **Facebook**: [Nhấn tại đây](https://facebook.com/share/1CJkDWUGBY/)\n"
                    "- **Zalo**: [Nhấn tại đây](https://zalo.me/0904562214)\n"
                    "- **Discord**: nguyenquanghuy06\n"
                    "- **Website**: [Nhấn tại đây](http://giaodich-profile.onlinewebshop.net/)\n"
                    "Liên hệ admin để được hỗ trợ hoặc hợp tác!",
        color=0x00ff00
    )
    embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name='help', description='Hiển thị danh sách lệnh')
async def help_command(interaction: Interaction):
    embed = nextcord.Embed(
        title="📜 Danh sách lệnh",
        description="Dưới đây là tất cả các lệnh có sẵn của bot. Một số chức năng (tạm dừng, tiếp tục, bỏ qua, v.v.) có thể dùng qua nút điều khiển khi phát nhạc:",
        color=0x00ff00
    )
    embed.add_field(
        name="Lệnh nhạc",
        value=(
            "`/play <nguồn>`: Phát nhạc từ YouTube hoặc Spotify\n"
            "`/search <từ khóa>`: Tìm kiếm bài hát trên YouTube\n"
            "`/queue`: Hiển thị hàng đợi phát nhạc\n"
            "`/clear`: Xóa toàn bộ hàng đợi\n"
            "`/disconnect`: Ngắt kết nối bot khỏi kênh thoại\n"
            "`/remove <vị trí>`: Xóa bài hát khỏi hàng đợi\n"
            "`/nowplaying`: Hiển thị bài hát đang phát và nút điều khiển"
        ),
        inline=False
    )
    embed.add_field(
        name="Lệnh thông tin",
        value=(
            "`/ping`: Kiểm tra độ trễ của bot\n"
            "`/uptime`: Hiển thị thời gian bot đã hoạt động\n"
            "`/bank`: Hiển thị thông tin ngân hàng của admin\n"
            "`/profile`: Hiển thị thông tin liên hệ của admin"
        ),
        inline=False
    )
    embed.add_field(
        name="Lệnh quản trị",
        value="`/sync`: Buộc đồng bộ lệnh (chỉ dành cho admin)",
        inline=False
    )
    embed.set_footer(text=f"Bot bởi Nguyễn Quang Huy (Dzi) | Cập nhật: {UPDATE_TIME} | Phiên bản: {BOT_VERSION}")
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)