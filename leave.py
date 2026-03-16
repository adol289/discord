# ============================================
# LEAVE.PY - FITUR WELCOME DAN LEAVE NOTIFICATION
# ============================================
# File khusus untuk menangani:
# 1. Welcome message (member join)
# 2. Leave notification (member leave)
# 3. Command untuk mengatur channel welcome
# 4. Test commands untuk preview
# ============================================

import discord
from discord.ext import commands
from discord import app_commands
import datetime
from typing import Optional

class WelcomeLeaveCog(commands.Cog):
    """Cog untuk fitur welcome dan leave notification"""
    
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = None  # Untuk menyimpan channel ID
        print("✅ Fitur Welcome & Leave (leave.py) telah dimuat!")
    
    # ============================================
    # FUNGSI GET CHANNEL (untuk welcome/leave)
    # ============================================
    def get_welcome_channel(self, guild):
        """Mendapatkan channel untuk welcome/leave"""
        
        # Cek apakah sudah diset dengan command
        if self.welcome_channel_id:
            channel = self.bot.get_channel(self.welcome_channel_id)
            if channel and channel.guild == guild:
                return channel
        
        # Cari channel dengan nama 'welcome'
        channel = discord.utils.get(guild.text_channels, name="welcome")
        if channel:
            return channel
        
        # Cari channel dengan nama 'general'
        channel = discord.utils.get(guild.text_channels, name="general")
        if channel:
            return channel
        
        # Ambil channel teks pertama
        for channel in guild.text_channels:
            return channel
        
        return None
    
    # ============================================
    # EVENT: MEMBER BERGABUNG (WELCOME)
    # ============================================
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Dipanggil ketika member baru bergabung ke server"""
        
        # Dapatkan channel welcome
        welcome_channel = self.get_welcome_channel(member.guild)
        if not welcome_channel:
            return
        
        # Buat embed welcome
        embed = discord.Embed(
            title="🎉 **MEMBER BARU BERGABUNG!**",
            description=f"Halo **{member.mention}**, selamat datang di **{member.guild.name}**!\n\nSilakan baca peraturan dan perkenalkan diri ya!",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        
        # Tambah thumbnail (avatar member)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Tambah informasi
        embed.add_field(name="📝 **Username**", value=member.name, inline=True)
        embed.add_field(name="🆔 **ID Member**", value=member.id, inline=True)
        embed.add_field(name="📅 **Akun Dibuat**", value=member.created_at.strftime("%d-%m-%Y"), inline=True)
        
        # Hitung jumlah member sekarang
        member_count = len(member.guild.members)
        embed.add_field(name="👥 **Total Member**", value=f"{member_count} member", inline=True)
        embed.add_field(name="🎂 **Member Ke-**", value=f"#{member_count}", inline=True)
        
        # Footer
        embed.set_footer(
            text="Putra Corporation • Selamat Bergabung!", 
            icon_url=member.guild.icon.url if member.guild.icon else None
        )
        
        # Kirim ke channel
        await welcome_channel.send(embed=embed)
        
        # Kirim DM ke member baru (opsional)
        try:
            dm_embed = discord.Embed(
                title=f"🎉 Selamat datang di {member.guild.name}!",
                description="Terima kasih telah bergabung di server Putra Corporation. Semoga betah ya!",
                color=discord.Color.blue()
            )
            dm_embed.set_footer(text="Putra Corporation • Official Server")
            await member.send(embed=dm_embed)
        except:
            # Jika member matikan DM, lewati
            pass
        
        print(f"📥 Welcome: {member.name} bergabung ke {member.guild.name}")
    
    # ============================================
    # EVENT: MEMBER KELUAR (LEAVE NOTIFICATION)
    # ============================================
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Dipanggil ketika member keluar dari server"""
        
        # Dapatkan channel untuk leave (sama dengan welcome)
        leave_channel = self.get_welcome_channel(member.guild)
        if not leave_channel:
            return
        
        # Hitung durasi member bergabung
        join_duration = None
        duration_text = "Tidak diketahui"
        
        if member.joined_at:
            join_duration = datetime.datetime.utcnow() - member.joined_at
            days = join_duration.days
            hours = join_duration.seconds // 3600
            minutes = (join_duration.seconds % 3600) // 60
            
            if days > 0:
                duration_text = f"{days} hari {hours} jam"
            elif hours > 0:
                duration_text = f"{hours} jam {minutes} menit"
            else:
                duration_text = f"{minutes} menit"
        
        # Buat embed leave
        embed = discord.Embed(
            title="👋 **MEMBER KELUAR**",
            description=f"**{member.name}** telah meninggalkan server kami.",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.utcnow()
        )
        
        # Tambah thumbnail (avatar member)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Tambah informasi
        embed.add_field(name="📝 **Username**", value=member.name, inline=True)
        embed.add_field(name="🆔 **ID Member**", value=member.id, inline=True)
        embed.add_field(name="📅 **Akun Dibuat**", value=member.created_at.strftime("%d-%m-%Y"), inline=True)
        
        if member.joined_at:
            embed.add_field(
                name="📥 **Bergabung Sejak**", 
                value=member.joined_at.strftime("%d-%m-%Y"), 
                inline=True
            )
            embed.add_field(name="⏱️ **Lama Bergabung**", value=duration_text, inline=True)
        
        # Hitung jumlah member sekarang
        member_count = len(member.guild.members)
        embed.add_field(name="👥 **Total Member Sekarang**", value=f"{member_count} member", inline=True)
        
        # Footer
        embed.set_footer(
            text="Putra Corporation • Sampai jumpa lagi!", 
            icon_url=member.guild.icon.url if member.guild.icon else None
        )
        
        # Kirim ke channel
        await leave_channel.send(embed=embed)
        
        print(f"📤 Leave: {member.name} keluar dari {member.guild.name}")
    
    # ============================================
    # SLASH COMMAND: /setwelcome (Atur channel welcome)
    # ============================================
    @app_commands.command(
        name="setwelcome", 
        description="Atur channel untuk welcome & leave notification"
    )
    @app_commands.describe(
        channel="Channel yang akan digunakan untuk welcome/leave"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def setwelcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Mengatur channel untuk welcome dan leave notification"""
        
        # Simpan channel ID
        self.welcome_channel_id = channel.id
        
        # Buat embed sukses
        embed = discord.Embed(
            title="✅ **CHANNEL WELCOME DIATUR**",
            description=f"Channel {channel.mention} sekarang akan digunakan untuk:\n• Welcome message (member join)\n• Leave notification (member leave)",
            color=discord.Color.green()
        )
        embed.set_footer(text="Putra Corporation • Pengaturan berhasil")
        
        await interaction.response.send_message(embed=embed)
        
        # Kirim pesan test ke channel yang dipilih
        test_embed = discord.Embed(
            title="🔔 **Welcome & Leave Channel**",
            description="Channel ini telah diatur sebagai tujuan untuk notifikasi member join dan leave.\n\nContoh pesan akan muncul ketika ada member yang bergabung atau keluar.",
            color=discord.Color.blue()
        )
        await channel.send(embed=test_embed)
    
    # ============================================
    # SLASH COMMAND: /testwelcome (Test fitur welcome)
    # ============================================
    @app_commands.command(
        name="testwelcome", 
        description="Test fitur welcome (simulasi)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def testwelcome(self, interaction: discord.Interaction):
        """Test fitur welcome dengan simulasi"""
        
        # Buat embed simulasi welcome
        embed = discord.Embed(
            title="🎉 **TEST WELCOME MESSAGE**",
            description="Ini adalah contoh bagaimana welcome message akan terlihat ketika member baru bergabung.",
            color=discord.Color.green()
        )
        
        # Gunakan avatar user sebagai contoh
        embed.set_thumbnail(
            url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
        )
        
        embed.add_field(name="📝 **Username**", value=interaction.user.name, inline=True)
        embed.add_field(name="🆔 **ID Member**", value=interaction.user.id, inline=True)
        embed.add_field(
            name="📅 **Akun Dibuat**", 
            value=interaction.user.created_at.strftime("%d-%m-%Y"), 
            inline=True
        )
        embed.add_field(
            name="👥 **Total Member**", 
            value=f"{len(interaction.guild.members)} member", 
            inline=True
        )
        embed.set_footer(text="Putra Corporation • Mode Test")
        
        await interaction.response.send_message(embed=embed)
    
    # ============================================
    # SLASH COMMAND: /testleave (Test fitur leave)
    # ============================================
    @app_commands.command(
        name="testleave", 
        description="Test fitur leave (simulasi)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def testleave(self, interaction: discord.Interaction):
        """Test fitur leave dengan simulasi"""
        
        # Hitung durasi (contoh)
        join_date = interaction.user.joined_at if interaction.user.joined_at else datetime.datetime.utcnow()
        duration = datetime.datetime.utcnow() - join_date
        days = duration.days
        hours = duration.seconds // 3600
        
        duration_text = f"{days} hari {hours} jam" if days > 0 else f"{hours} jam"
        
        # Buat embed simulasi leave
        embed = discord.Embed(
            title="👋 **TEST LEAVE NOTIFICATION**",
            description="Ini adalah contoh bagaimana leave notification akan terlihat ketika member keluar.",
            color=discord.Color.orange()
        )
        
        # Gunakan avatar user sebagai contoh
        embed.set_thumbnail(
            url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
        )
        
        embed.add_field(name="📝 **Username**", value=interaction.user.name, inline=True)
        embed.add_field(name="🆔 **ID Member**", value=interaction.user.id, inline=True)
        embed.add_field(
            name="📅 **Akun Dibuat**", 
            value=interaction.user.created_at.strftime("%d-%m-%Y"), 
            inline=True
        )
        embed.add_field(
            name="📥 **Bergabung Sejak**", 
            value=interaction.user.joined_at.strftime("%d-%m-%Y") if interaction.user.joined_at else "Tidak diketahui", 
            inline=True
        )
        embed.add_field(name="⏱️ **Lama Bergabung**", value=duration_text, inline=True)
        embed.add_field(
            name="👥 **Total Member Sekarang**", 
            value=f"{len(interaction.guild.members)} member", 
            inline=True
        )
        embed.set_footer(text="Putra Corporation • Mode Test")
        
        await interaction.response.send_message(embed=embed)
    
    # ============================================
    # SLASH COMMAND: /resetwelcome (Reset channel ke default)
    # ============================================
    @app_commands.command(
        name="resetwelcome", 
        description="Reset channel welcome ke default (auto-detect)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def resetwelcome(self, interaction: discord.Interaction):
        """Reset channel welcome ke mode auto-detect"""
        
        self.welcome_channel_id = None
        
        embed = discord.Embed(
            title="🔄 **CHANNEL WELCOME RESET**",
            description="Channel welcome sekarang akan **auto-detect** (cari #welcome, #general, atau channel pertama).",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

# ============================================
# SETUP FUNCTION
# ============================================
async def setup(bot):
    """Fungsi untuk memuat cog ke bot utama"""
    await bot.add_cog(WelcomeLeaveCog(bot))
    print("🔧 WelcomeLeaveCog telah ditambahkan ke bot")
