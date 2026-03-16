import discord
from discord import app_commands
from discord.ext import commands
import datetime
import os
import asyncio
from config.config import TOKEN

# ============================================
# KONFIGURASI BOT - PUTRA CORPORATION
# ============================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # PENTING: Untuk fitur welcome/leave

class PutraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="", intents=intents, help_command=None)
        self.synced = False
    
    async def setup_hook(self):
        # Load leave.py (Welcome & Leave)
        try:
            await self.load_extension("leave")
            print("✅ Berhasil memuat leave.py (Welcome & Leave)")
        except Exception as e:
            print(f"❌ Gagal memuat leave.py: {e}")
        
        # Load createrole.py (Role Management)
        try:
            await self.load_extension("createrole")
            print("✅ Berhasil memuat createrole.py (Role Management)")
        except Exception as e:
            print(f"❌ Gagal memuat createrole.py: {e}")
        
        # Sync slash commands
        await self.tree.sync()
        self.synced = True
        print("✅ Slash commands synced!")

bot = PutraBot()

# ============================================
# EVENT: BOT SIAP
# ============================================
@bot.event
async def on_ready():
    print(f'[SIAP TUAN PUTRA] Bot {bot.user} telah online!')
    print(f'ID Bot: {bot.user.id}')
    print(f'Menggunakan Slash Commands: /')
    print('-' * 30)
    await bot.change_presence(activity=discord.Game(name="/help | Putra Corp"))

# ============================================
# EVENT: DEBUG (TAMPILKAN SLASH COMMANDS)
# ============================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content == "!debug":
        commands_list = [cmd.name for cmd in bot.tree.get_commands()]
        await message.channel.send(f"**Slash Commands terdaftar:** {', '.join(commands_list)}")

# ============================================
# SLASH COMMAND: /help
# ============================================
@bot.tree.command(name="help", description="Menampilkan semua fitur dan command PutraBot")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📚 **PUTRA BOT COMMANDS**",
        description="Bot eksklusif buatan Xyxz untuk Tuan Putra\nGunakan `/` untuk melihat semua command",
        color=discord.Color.blue()
    )
    embed.add_field(name="🛠️ **UTILITY**", value="`/help` - Menampilkan menu ini\n`/ping` - Cek respon bot", inline=False)
    embed.add_field(name="👤 **USER INFO**", value="`/avatar [user]` - Lihat avatar user\n`/userinfo [user]` - Info detail user", inline=False)
    embed.add_field(name="📊 **SERVER INFO**", value="`/serverinfo` - Info detail server", inline=False)
    embed.add_field(name="🔨 **MODERATION**", value="`/clear [jumlah]` - Hapus pesan\n`/kick [user]` - Kick member\n`/ban [user]` - Ban member", inline=False)
    embed.add_field(name="👋 **WELCOME/LEAVE**", value="`/setwelcome [channel]` - Atur channel welcome\n`/resetwelcome` - Reset channel ke auto\n`/testwelcome` - Test welcome message\n`/testleave` - Test leave notification", inline=False)
    embed.add_field(name="👑 **ROLE MANAGEMENT**", value="`/createrole` - Buat role baru\n`/deleterole` - Hapus role\n`/giverole` - Beri role ke member\n`/takerole` - Ambil role dari member\n`/roleinfo` - Info role\n`/rolecolor` - Ubah warna role\n`/rolehoist` - Atur tampilan role\n`/rolemention` - Atur mention role", inline=False)
    embed.set_footer(text="Putra Corporation • Eksklusif")
    
    await interaction.response.send_message(embed=embed)

# ============================================
# SLASH COMMAND: /ping
# ============================================
@bot.tree.command(name="ping", description="Cek respon dan latency bot")
async def ping_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🏓 PONG!",
        description=f"**Latency:** `{round(bot.latency * 1000)}ms`\n**Status:** Online",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

# ============================================
# SLASH COMMAND: /avatar
# ============================================
@bot.tree.command(name="avatar", description="Lihat avatar user")
@app_commands.describe(user="User yang ingin dilihat avatar-nya")
async def avatar_command(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    
    embed = discord.Embed(
        title=f"🖼️ Avatar {user.name}",
        color=user.color if hasattr(user, 'color') else discord.Color.blue()
    )
    embed.set_image(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.set_footer(text=f"ID: {user.id}")
    
    await interaction.response.send_message(embed=embed)

# ============================================
# SLASH COMMAND: /clear
# ============================================
@bot.tree.command(name="clear", description="Hapus pesan di channel")
@app_commands.describe(jumlah="Jumlah pesan yang akan dihapus (1-100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear_command(interaction: discord.Interaction, jumlah: int):
    if jumlah < 1 or jumlah > 100:
        await interaction.response.send_message("❌ Jumlah harus antara 1-100", ephemeral=True)
        return
    
    await interaction.channel.purge(limit=jumlah)
    embed = discord.Embed(
        description=f"✅ **{jumlah}** pesan telah dihapus!",
        color=discord.Color.orange()
    )
    await interaction.response.send_message(embed=embed, delete_after=3)

# ============================================
# SLASH COMMAND: /userinfo
# ============================================
@bot.tree.command(name="userinfo", description="Lihat informasi detail user")
@app_commands.describe(user="User yang ingin dilihat infonya")
async def userinfo_command(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    
    member = None
    if interaction.guild:
        member = interaction.guild.get_member(user.id)
    
    embed = discord.Embed(
        title=f"👤 Info User: {user.name}",
        color=member.color if member else discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="Bot?", value="✅ Ya" if user.bot else "❌ Tidak", inline=True)
    embed.add_field(name="Akun Dibuat", value=user.created_at.strftime("%d-%m-%Y %H:%M"), inline=True)
    
    if member:
        embed.add_field(name="Nickname", value=member.nick if member.nick else "Tidak ada", inline=True)
        embed.add_field(name="Bergabung", value=member.joined_at.strftime("%d-%m-%Y %H:%M") if member.joined_at else "Tidak diketahui", inline=True)
    
    await interaction.response.send_message(embed=embed)

# ============================================
# SLASH COMMAND: /serverinfo
# ============================================
@bot.tree.command(name="serverinfo", description="Lihat informasi detail server")
async def serverinfo_command(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("❌ Perintah ini hanya bisa di server!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title=f"📊 Info Server: {guild.name}",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.utcnow()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    # Hitung statistik
    total_members = len(guild.members)
    online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)
    bot_count = sum(1 for member in guild.members if member.bot)
    human_count = total_members - bot_count
    
    embed.add_field(name="ID Server", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
    embed.add_field(name="Member", value=f"{total_members} total ({online_members} online)", inline=True)
    embed.add_field(name="Human/Bot", value=f"{human_count} human • {bot_count} bot", inline=True)
    embed.add_field(name="Channel", value=len(guild.channels), inline=True)
    embed.add_field(name="Role", value=len(guild.roles), inline=True)
    embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
    embed.add_field(name="Boost Count", value=guild.premium_subscription_count, inline=True)
    embed.add_field(name="Dibuat Pada", value=guild.created_at.strftime("%d-%m-%Y"), inline=True)
    
    await interaction.response.send_message(embed=embed)

# ============================================
# SLASH COMMAND: /kick
# ============================================
@bot.tree.command(name="kick", description="Kick member dari server")
@app_commands.describe(member="Member yang akan dikick", alasan="Alasan kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick_command(interaction: discord.Interaction, member: discord.Member, alasan: str = "Tidak ada alasan"):
    # Validasi
    if member == interaction.user:
        await interaction.response.send_message("❌ Tidak bisa kick diri sendiri!", ephemeral=True)
        return
    
    if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
        await interaction.response.send_message("❌ Tidak bisa kick member dengan role lebih tinggi!", ephemeral=True)
        return
    
    try:
        await member.kick(reason=f"Kick oleh {interaction.user.name}: {alasan}")
        
        embed = discord.Embed(
            title="👢 **MEMBER DIKICK**",
            description=f"**{member.mention}** telah dikick dari server.",
            color=discord.Color.red()
        )
        embed.add_field(name="👤 Member", value=f"{member.name} ({member.id})", inline=True)
        embed.add_field(name="👑 Oleh", value=interaction.user.mention, inline=True)
        embed.add_field(name="📝 Alasan", value=alasan, inline=False)
        embed.set_footer(text="Putra Corporation • Moderation")
        
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Gagal kick member: {e}", ephemeral=True)

# ============================================
# SLASH COMMAND: /ban
# ============================================
@bot.tree.command(name="ban", description="Ban member dari server")
@app_commands.describe(member="Member yang akan diban", alasan="Alasan ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban_command(interaction: discord.Interaction, member: discord.User, alasan: str = "Tidak ada alasan"):
    # Validasi
    if member == interaction.user:
        await interaction.response.send_message("❌ Tidak bisa ban diri sendiri!", ephemeral=True)
        return
    
    try:
        await interaction.guild.ban(member, reason=f"Ban oleh {interaction.user.name}: {alasan}")
        
        embed = discord.Embed(
            title="🔨 **MEMBER DIBANNED**",
            description=f"**{member.mention}** telah dibanned dari server.",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="👤 Member", value=f"{member.name} ({member.id})", inline=True)
        embed.add_field(name="👑 Oleh", value=interaction.user.mention, inline=True)
        embed.add_field(name="📝 Alasan", value=alasan, inline=False)
        embed.set_footer(text="Putra Corporation • Moderation")
        
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Gagal ban member: {e}", ephemeral=True)

# ============================================
# ERROR HANDLING
# ============================================
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Anda tidak punya izin untuk menggunakan perintah ini!", ephemeral=True)
    
    elif isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"❌ Command dalam cooldown. Coba lagi {error.retry_after:.2f} detik lagi.", ephemeral=True)
    
    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message(f"❌ Bot tidak memiliki izin: {error.missing_permissions}", ephemeral=True)
    
    elif isinstance(error, app_commands.CommandNotFound):
        await interaction.response.send_message("❌ Command tidak ditemukan. Gunakan `/help` untuk melihat daftar command.", ephemeral=True)
    
    elif isinstance(error, app_commands.TransformerError):
        await interaction.response.send_message(f"❌ Input tidak valid: {error}", ephemeral=True)
    
    else:
        await interaction.response.send_message(f"❌ Terjadi error: {error}", ephemeral=True)
        print(f"Error detail: {error}")

# ============================================
# JALANKAN BOT
# ============================================
if __name__ == "__main__":
    if TOKEN == "MASUKKAN_TOKEN_BOT_ANDA_DISINI":
        print("❌ ERROR: Tuan belum memasukkan Token Bot!")
        print("📝 Silakan masukkan token bot di file config/config.py")
        print("📝 Contoh: TOKEN = 'MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.ABCDEF.GhIjkLmNoPqRsTuVwXyZ'")
    else:
        try:
            print("🚀 Menjalankan bot...")
            bot.run(TOKEN)
        except discord.LoginFailure:
            print("❌ ERROR: Token tidak valid! Periksa kembali token di config/config.py")
        except Exception as e:
            print(f"❌ ERROR: {e}")
