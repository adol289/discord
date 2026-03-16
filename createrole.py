# ============================================
# CREATEROLE.PY - FITUR ROLE MANAGEMENT
# ============================================

import discord
from discord.ext import commands
from discord import app_commands
import datetime

class CreateRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✅ Fitur CreateRole (createrole.py) telah dimuat!")
    
    # ============================================
    # SLASH COMMAND: /createrole
    # ============================================
    @app_commands.command(name="createrole", description="Membuat role baru di server")
    @app_commands.describe(
        nama="Nama role yang akan dibuat",
        warna="Warna role (merah, biru, hijau, atau #FF0000)",
        alasan="Alasan pembuatan role"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def create_role(self, interaction: discord.Interaction, nama: str, warna: str = "default", alasan: str = "Tidak ada alasan"):
        role_color = self._parse_color(warna)
        
        try:
            new_role = await interaction.guild.create_role(
                name=nama,
                color=role_color,
                reason=f"Dibuat oleh {interaction.user.name} - {alasan}"
            )
            
            embed = discord.Embed(
                title="✅ **ROLE BERHASIL DIBUAT**",
                description=f"Role **{new_role.name}** telah berhasil dibuat!",
                color=role_color if role_color.value != 0 else discord.Color.green()
            )
            embed.add_field(name="🆔 **ID Role**", value=new_role.id, inline=True)
            embed.add_field(name="🎨 **Warna**", value=str(role_color).upper() if role_color.value != 0 else "Default", inline=True)
            embed.add_field(name="👤 **Dibuat Oleh**", value=interaction.user.mention, inline=True)
            embed.add_field(name="📝 **Alasan**", value=alasan, inline=False)
            embed.set_footer(text="Putra Corporation • Role Management")
            embed.timestamp = datetime.datetime.utcnow()
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Gagal membuat role: {e}", ephemeral=True)
    
    # ============================================
    # SLASH COMMAND: /deleterole
    # ============================================
    @app_commands.command(name="deleterole", description="Menghapus role dari server")
    @app_commands.describe(role="Role yang akan dihapus", alasan="Alasan penghapusan")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def delete_role(self, interaction: discord.Interaction, role: discord.Role, alasan: str = "Tidak ada alasan"):
        if role == interaction.guild.default_role:
            await interaction.response.send_message("❌ Tidak bisa menghapus role @everyone!", ephemeral=True)
            return
        
        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Role ini lebih tinggi dari role bot!", ephemeral=True)
            return
        
        role_name = role.name
        role_id = role.id
        
        try:
            await role.delete(reason=f"Dihapus oleh {interaction.user.name} - {alasan}")
            
            embed = discord.Embed(
                title="🗑️ **ROLE BERHASIL DIHAPUS**",
                description=f"Role **{role_name}** telah dihapus.",
                color=discord.Color.red()
            )
            embed.add_field(name="🆔 **ID Role**", value=role_id, inline=True)
            embed.add_field(name="👤 **Dihapus Oleh**", value=interaction.user.mention, inline=True)
            embed.add_field(name="📝 **Alasan**", value=alasan, inline=False)
            embed.set_footer(text="Putra Corporation • Role Management")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Gagal menghapus role: {e}", ephemeral=True)
    
    # ============================================
    # SLASH COMMAND: /giverole
    # ============================================
    @app_commands.command(name="giverole", description="Memberikan role kepada member")
    @app_commands.describe(member="Member", role="Role", alasan="Alasan")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def give_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role, alasan: str = "Tidak ada alasan"):
        if role == interaction.guild.default_role:
            await interaction.response.send_message("❌ Tidak bisa memberikan role @everyone!", ephemeral=True)
            return
        
        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Role ini lebih tinggi dari role bot!", ephemeral=True)
            return
        
        if role in member.roles:
            await interaction.response.send_message(f"❌ {member.mention} sudah memiliki role {role.mention}!", ephemeral=True)
            return
        
        try:
            await member.add_roles(role, reason=f"Diberikan oleh {interaction.user.name} - {alasan}")
            
            embed = discord.Embed(
                title="✅ **ROLE DIBERIKAN**",
                description=f"Role {role.mention} diberikan kepada {member.mention}",
                color=role.color if role.color.value != 0 else discord.Color.green()
            )
            embed.add_field(name="👤 **Member**", value=member.mention, inline=True)
            embed.add_field(name="🎨 **Role**", value=role.mention, inline=True)
            embed.add_field(name="👑 **Oleh**", value=interaction.user.mention, inline=True)
            embed.add_field(name="📝 **Alasan**", value=alasan, inline=False)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text="Putra Corporation • Role Management")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Gagal memberikan role: {e}", ephemeral=True)
    
    # ============================================
    # SLASH COMMAND: /takerole
    # ============================================
    @app_commands.command(name="takerole", description="Mengambil role dari member")
    @app_commands.describe(member="Member", role="Role", alasan="Alasan")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def take_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role, alasan: str = "Tidak ada alasan"):
        if role == interaction.guild.default_role:
            await interaction.response.send_message("❌ Tidak bisa mengambil role @everyone!", ephemeral=True)
            return
        
        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Role ini lebih tinggi dari role bot!", ephemeral=True)
            return
        
        if role not in member.roles:
            await interaction.response.send_message(f"❌ {member.mention} tidak memiliki role {role.mention}!", ephemeral=True)
            return
        
        try:
            await member.remove_roles(role, reason=f"Diambil oleh {interaction.user.name} - {alasan}")
            
            embed = discord.Embed(
                title="✅ **ROLE DIAMBIL**",
                description=f"Role {role.mention} diambil dari {member.mention}",
                color=discord.Color.orange()
            )
            embed.add_field(name="👤 **Member**", value=member.mention, inline=True)
            embed.add_field(name="🎨 **Role**", value=role.mention, inline=True)
            embed.add_field(name="👑 **Oleh**", value=interaction.user.mention, inline=True)
            embed.add_field(name="📝 **Alasan**", value=alasan, inline=False)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text="Putra Corporation • Role Management")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Gagal mengambil role: {e}", ephemeral=True)
    
    # ============================================
    # SLASH COMMAND: /roleinfo
    # ============================================
    @app_commands.command(name="roleinfo", description="Melihat informasi detail tentang role")
    @app_commands.describe(role="Role yang ingin dilihat")
    async def role_info(self, interaction: discord.Interaction, role: discord.Role):
        members_with_role = [member for member in interaction.guild.members if role in member.roles]
        member_count = len(members_with_role)
        
        member_mentions = [member.mention for member in members_with_role[:10]]
        member_text = ", ".join(member_mentions) if member_mentions else "Tidak ada"
        if member_count > 10:
            member_text += f" dan {member_count - 10} lainnya..."
        
        embed = discord.Embed(
            title=f"📋 **INFORMASI ROLE: {role.name}**",
            color=role.color if role.color.value != 0 else discord.Color.blue()
        )
        embed.add_field(name="🆔 **ID Role**", value=role.id, inline=True)
        embed.add_field(name="🎨 **Warna**", value=str(role.color).upper() if role.color.value != 0 else "Default", inline=True)
        embed.add_field(name="📅 **Dibuat Pada**", value=role.created_at.strftime("%d-%m-%Y %H:%M"), inline=True)
        embed.add_field(name="👥 **Jumlah Member**", value=f"{member_count} member", inline=True)
        embed.add_field(name="📌 **Hoist**", value="✅ Ya" if role.hoist else "❌ Tidak", inline=True)
        embed.add_field(name="🔊 **Mentionable**", value="✅ Ya" if role.mentionable else "❌ Tidak", inline=True)
        embed.add_field(name="👤 **Member dengan Role**", value=member_text, inline=False)
        embed.set_footer(text="Putra Corporation • Role Management")
        
        await interaction.response.send_message(embed=embed)
    
    # ============================================
    # SLASH COMMAND: /rolecolor
    # ============================================
    @app_commands.command(name="rolecolor", description="Mengubah warna role")
    @app_commands.describe(role="Role", warna="Warna baru")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_color(self, interaction: discord.Interaction, role: discord.Role, warna: str):
        if role == interaction.guild.default_role:
            await interaction.response.send_message("❌ Tidak bisa mengubah warna @everyone!", ephemeral=True)
            return
        
        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Role ini lebih tinggi dari role bot!", ephemeral=True)
            return
        
        new_color = self._parse_color(warna)
        
        try:
            await role.edit(color=new_color, reason=f"Warna diubah oleh {interaction.user.name}")
            
            embed = discord.Embed(
                title="🎨 **WARNA ROLE DIUBAH**",
                description=f"Warna role {role.mention} telah diubah!",
                color=new_color if new_color.value != 0 else discord.Color.green()
            )
            embed.add_field(name="🎨 **Warna Baru**", value=str(new_color).upper() if new_color.value != 0 else "Default", inline=True)
            embed.add_field(name="👑 **Diubah Oleh**", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Gagal mengubah warna: {e}", ephemeral=True)
    
    # ============================================
    # SLASH COMMAND: /rolehoist
    # ============================================
    @app_commands.command(name="rolehoist", description="Atur tampilan terpisah role")
    @app_commands.describe(role="Role", hoist="True/Tidak")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_hoist(self, interaction: discord.Interaction, role: discord.Role, hoist: bool):
        if role == interaction.guild.default_role:
            await interaction.response.send_message("❌ Tidak bisa mengatur @everyone!", ephemeral=True)
            return
        
        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Role ini lebih tinggi dari role bot!", ephemeral=True)
            return
        
        try:
            await role.edit(hoist=hoist, reason=f"Hoist diatur oleh {interaction.user.name}")
            
            status = "ditampilkan terpisah" if hoist else "tidak ditampilkan terpisah"
            embed = discord.Embed(
                title="📌 **PENGATURAN HOIST**",
                description=f"Role {role.mention} sekarang **{status}**.",
                color=discord.Color.blue()
            )
            embed.add_field(name="👑 **Diatur Oleh**", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Gagal mengatur hoist: {e}", ephemeral=True)
    
    # ============================================
    # SLASH COMMAND: /rolemention
    # ============================================
    @app_commands.command(name="rolemention", description="Atur apakah role bisa di-mention")
    @app_commands.describe(role="Role", mentionable="True/Tidak")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_mention(self, interaction: discord.Interaction, role: discord.Role, mentionable: bool):
        if role == interaction.guild.default_role:
            await interaction.response.send_message("❌ Tidak bisa mengatur @everyone!", ephemeral=True)
            return
        
        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message("❌ Role ini lebih tinggi dari role bot!", ephemeral=True)
            return
        
        try:
            await role.edit(mentionable=mentionable, reason=f"Mentionable diatur oleh {interaction.user.name}")
            
            status = "bisa di-mention" if mentionable else "tidak bisa di-mention"
            embed = discord.Embed(
                title="🔊 **PENGATURAN MENTION**",
                description=f"Role {role.mention} sekarang **{status}**.",
                color=discord.Color.blue()
            )
            embed.add_field(name="👑 **Diatur Oleh**", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Gagal mengatur mention: {e}", ephemeral=True)
    
    # ============================================
    # FUNGSI PEMBANTU: PARSE WARNA
    # ============================================
    def _parse_color(self, color_str: str) -> discord.Color:
        color_str = color_str.lower().strip()
        
        color_map = {
            "merah": discord.Color.red(),
            "biru": discord.Color.blue(),
            "hijau": discord.Color.green(),
            "kuning": discord.Color.gold(),
            "orange": discord.Color.orange(),
            "ungu": discord.Color.purple(),
            "pink": discord.Color.magenta(),
            "hitam": discord.Color.default(),
            "putih": discord.Color.default(),
            "default": discord.Color.default(),
        }
        
        if color_str in color_map:
            return color_map[color_str]
        
        if color_str.startswith("#") and len(color_str) == 7:
            try:
                return discord.Color(int(color_str[1:], 16))
            except:
                pass
        
        return discord.Color.default()

# ============================================
# SETUP FUNCTION
# ============================================
async def setup(bot):
    await bot.add_cog(CreateRoleCog(bot))
    print("🔧 CreateRoleCog telah ditambahkan ke bot")