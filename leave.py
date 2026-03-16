# ============================================
# LEAVE.PY - FITUR WELCOME DAN LEAVE NOTIFICATION
# ============================================

import discord
from discord.ext import commands
from discord import app_commands
import datetime

class WelcomeLeaveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = None
        print("✅ Fitur Welcome & Leave (leave.py) telah dimuat!")
    
    # ============================================
    # EVENT: MEMBER BERGABUNG (WELCOME)
    # ============================================
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = None
        
        if self.welcome_channel_id:
            welcome_channel = self.bot.get_channel(self.welcome_channel_id)
        
        if not welcome_channel:
            welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
        
        if not welcome_channel:
            welcome_channel = discord.utils.get(member.guild.text_channels, name="general")
        
        if not welcome_channel:
            for channel in member.guild.text_channels:
                welcome_channel = channel
                break
        
        if not welcome_channel:
            return
        
        embed = discord.Embed(
            title="🎉 **MEMBER BARU BERGABUNG!**",
            description=f"Halo **{member.mention}**, selamat datang di **{member.guild.name}**!",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="📝 **Username**", value=member.name, inline=True)
        embed.add_field(name="🆔 **ID Member**", value=member.id, inline=True)
        embed.add_field(name="📅 **Akun Dibuat**", value=member.created_at.strftime("%d-%m-%Y"), inline=True)
        
        member_count = len(member.guild.members)
        embed.add_field(name="👥 **Total Member**", value=f"{member_count} member", inline=True)
        embed.add_field(name="🎂 **Member Ke-**", value=f"#{member_count}", inline=True)
        
        embed.set_footer(text="Putra Corporation • Selamat Bergabung!", icon_url=member.guild.icon.url if member.guild.icon else None)
        
        await welcome_channel.send(embed=embed)
        
        try:
            dm_embed = discord.Embed(
                title=f"🎉 Selamat datang di {member.guild.name}!",
                description="Terima kasih telah bergabung di server Putra Corporation. Semoga betah ya!",
                color=discord.Color.blue()
            )
            dm_embed.set_footer(text="Putra Corporation • Official Server")
            await member.send(embed=dm_embed)
        except:
            pass
        
        print(f"📥 Welcome: {member.name} bergabung ke {member.guild.name}")
    
    # ============================================
    # EVENT: MEMBER KELUAR (LEAVE NOTIFICATION)
    # ============================================
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        leave_channel = None
        
        if self.welcome_channel_id:
            leave_channel = self.bot.get_channel(self.welcome_channel_id)
        
        if not leave_channel:
            leave_channel = discord.utils.get(member.guild.text_channels, name="welcome")
        
        if not leave_channel:
            leave_channel = discord.utils.get(member.guild.text_channels, name="general")
        
        if not leave_channel:
            for channel in member.guild.text_channels:
                leave_channel = channel
                break
        
        if not leave_channel:
            return
        
        join_duration = datetime.datetime.utcnow() - member.joined_at if member.joined_at else None
        duration_text = "Tidak diketahui"
        
        if join_duration:
            days = join_duration.days
            hours = join_duration.seconds // 3600
            minutes = (join_duration.seconds % 3600) // 60
            
            if days > 0:
                duration_text = f"{days} hari {hours} jam"
            elif hours > 0:
                duration_text = f"{hours} jam {minutes} menit"
            else:
                duration_text = f"{minutes} menit"
        
        embed = discord.Embed(
            title="👋 **MEMBER KELUAR**",
            description=f"**{member.name}** telah meninggalkan server kami.",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="📝 **Username**", value=member.name, inline=True)
        embed.add_field(name="🆔 **ID Member**", value=member.id, inline=True)
        embed.add_field(name="📅 **Akun Dibuat**", value=member.created_at.strftime("%d-%m-%Y"), inline=True)
        
        if member.joined_at:
            embed.add_field(name="📥 **Bergabung Sejak**", value=member.joined_at.strftime("%d-%m-%Y"), inline=True)
            embed.add_field(name="⏱️ **Lama Bergabung**", value=duration_text, inline=True)
        
        member_count = len(member.guild.members)
        embed.add_field(name="👥 **Total Member Sekarang**", value=f"{member_count} member", inline=True)
        
        embed.set_footer(text="Putra Corporation • Sampai jumpa lagi!", icon_url=member.guild.icon.url if member.guild.icon else None)
        
        await leave_channel.send(embed=embed)
        print(f"📤 Leave: {member.name} keluar dari {member.guild.name}")
    
    # ============================================
    # SLASH COMMAND: /setwelcome
    # ============================================
    @app_commands.command(name="setwelcome", description="Atur channel untuk welcome & leave notification")
    @app_commands.describe(channel="Channel yang akan digunakan untuk welcome/leave")
    @app_commands.checks.has_permissions(administrator=True)
    async def setwelcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.welcome_channel_id = channel.id
        
        embed = discord.Embed(
            title="✅ **CHANNEL WELCOME DIATUR**",
            description=f"Channel {channel.mention} sekarang akan digunakan untuk welcome dan leave notification.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Putra Corporation • Pengaturan berhasil")
        
        await interaction.response.send_message(embed=embed)
    
    # ============================================
    # SLASH COMMAND: /testwelcome
    # ============================================
    @app_commands.command(name="testwelcome", description="Test fitur welcome (simulasi)")
    @app_commands.checks.has_permissions(administrator=True)
    async def testwelcome(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎉 **TEST WELCOME MESSAGE**",
            description="Ini adalah contoh bagaimana welcome message akan terlihat.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.add_field(name="📝 **Username**", value=interaction.user.name, inline=True)
        embed.add_field(name="🆔 **ID Member**", value=interaction.user.id, inline=True)
        embed.add_field(name="📅 **Akun Dibuat**", value=interaction.user.created_at.strftime("%d-%m-%Y"), inline=True)
        embed.add_field(name="👥 **Total Member**", value=f"{len(interaction.guild.members)} member", inline=True)
        embed.set_footer(text="Putra Corporation • Mode Test")
        
        await interaction.response.send_message(embed=embed)
    
    # ============================================
    # SLASH COMMAND: /testleave
    # ============================================
    @app_commands.command(name="testleave", description="Test fitur leave (simulasi)")
    @app_commands.checks.has_permissions(administrator=True)
    async def testleave(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="👋 **TEST LEAVE NOTIFICATION**",
            description="Ini adalah contoh bagaimana leave notification akan terlihat.",
            color=discord.Color.orange()
        )
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.add_field(name="📝 **Username**", value=interaction.user.name, inline=True)
        embed.add_field(name="🆔 **ID Member**", value=interaction.user.id, inline=True)
        embed.add_field(name="📅 **Akun Dibuat**", value=interaction.user.created_at.strftime("%d-%m-%Y"), inline=True)
        embed.add_field(name="📥 **Bergabung Sejak**", value=interaction.user.joined_at.strftime("%d-%m-%Y") if interaction.user.joined_at else "Tidak diketahui", inline=True)
        embed.add_field(name="👥 **Total Member Sekarang**", value=f"{len(interaction.guild.members)} member", inline=True)
        embed.set_footer(text="Putra Corporation • Mode Test")
        
        await interaction.response.send_message(embed=embed)

# ============================================
# SETUP FUNCTION
# ============================================
async def setup(bot):
    await bot.add_cog(WelcomeLeaveCog(bot))
    print("🔧 WelcomeLeaveCog telah ditambahkan ke bot")