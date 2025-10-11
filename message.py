# bot_praca_magica.py
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

# ===========================
# CONFIGURAÇÃO
# ===========================
TOKEN = "SEU_TOKEN_AQUI"
CHANNEL_ID = 1421223793044750547  # Canal fixo para o painel

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Estrutura das praças
andares = ["ANTIDEMONIO", "EXP3", "EXP2", "EXP1"]
salas = ["Esquerda", "Meio", "Direita"]
duracoes = {
    "30 minutos": 30,
    "1 hora": 60,
    "1 hora 30 minutos": 90
}

# Claims ativos
claims = {
    andar: {sala: None for sala in salas} for andar in andares
}

# ===========================
# VIEW COM SELECTS E BOTÕES
# ===========================
class ClaimView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Escolha o andar",
        options=[discord.SelectOption(label=a) for a in andares],
        custom_id="select_andar"
    )
    async def select_andar(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.andar = select.values[0]
        await interaction.response.defer()

    @discord.ui.select(
        placeholder="Escolha a sala",
        options=[discord.SelectOption(label=s) for s in salas],
        custom_id="select_sala"
    )
    async def select_sala(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.sala = select.values[0]
        await interaction.response.defer()

    @discord.ui.select(
        placeholder="Escolha a duração",
        options=[discord.SelectOption(label=d) for d in duracoes.keys()],
        custom_id="select_duracao"
    )
    async def select_duracao(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.duracao = select.values[0]
        await interaction.response.defer()

    @discord.ui.button(label="✅ Claimar Praça", style=discord.ButtonStyle.success, custom_id="claim_button")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not hasattr(self, "andar") or not hasattr(self, "sala") or not hasattr(self, "duracao"):
            await interaction.response.send_message("⚠️ Selecione andar, sala e duração antes de claimar!", ephemeral=True)
            return

        andar, sala, duracao = self.andar, self.sala, self.duracao
        if claims[andar][sala] and claims[andar][sala]["expires_at"] > datetime.now():
            await interaction.response.send_message("❌ Esta sala já está claimada!", ephemeral=True)
            return

        claims[andar][sala] = {
            "user": interaction.user,
            "expires_at": datetime.now() + timedelta(minutes=duracoes[duracao]),
            "duracao": duracao
        }

        await update_panel()
        await interaction.response.send_message(f"✅ Você claimou **{andar} - {sala}** por {duracao}!", ephemeral=True)

    @discord.ui.button(label="❌ Cancelar meu Claim", style=discord.ButtonStyle.danger, custom_id="cancel_button")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        for andar in claims:
            for sala in claims[andar]:
                if claims[andar][sala] and claims[andar][sala]["user"].id == interaction.user.id:
                    claims[andar][sala] = None
                    await update_panel()
                    await interaction.response.send_message("🗑️ Seu claim foi cancelado!", ephemeral=True)
                    return
        await interaction.response.send_message("⚠️ Você não possui nenhum claim ativo!", ephemeral=True)

# ===========================
# EMBED DO PAINEL
# ===========================
def build_embed():
    embed = discord.Embed(
        title="📍 Praça Mágica — Painel de Claims",
        color=discord.Color.purple(),
        timestamp=datetime.now()
    )
    for andar in andares:
        desc = ""
        for sala in salas:
            claim = claims[andar][sala]
            if claim and claim["expires_at"] > datetime.now():
                restante = claim["expires_at"] - datetime.now()
                minutos, segundos = divmod(int(restante.total_seconds()), 60)
                desc += f"**{sala}:** {claim['user'].mention} — ⏰ {claim['duracao']} (resta {minutos:02d}:{segundos:02d})\n"
            else:
                desc += f"**{sala}:** — Livre —\n"
        embed.add_field(name=andar, value=desc, inline=False)

    embed.set_footer(text="Use os botões para claimar / cancelar. Tempo máximo 1h30.")
    return embed

# ===========================
# ATUALIZA PAINEL
# ===========================
panel_message = None

async def update_panel():
    global panel_message
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    embed = build_embed()
    if panel_message:
        try:
            await panel_message.edit(embed=embed, view=ClaimView())
            return
        except:
            pass

    panel_message = await channel.send(embed=embed, view=ClaimView())

# ===========================
# LOOP PARA EXPIRAR CLAIMS
# ===========================
@tasks.loop(seconds=30)
async def check_expirations():
    updated = False
    for andar in claims:
        for sala in claims[andar]:
            if claims[andar][sala] and claims[andar][sala]["expires_at"] <= datetime.now():
                claims[andar][sala] = None
                updated = True
    if updated:
        await update_panel()

# ===========================
# EVENTOS
# ===========================
@bot.event
async def on_ready():
    print(f"🤖 Bot online como {bot.user}")
    await update_panel()
    check_expirations.start()
    bot.add_view(ClaimView())  # mantém botões ativos após restart

# ===========================
# RODAR BOT
# ===========================
if __name__ == "__main__":
    bot.run(TOKEN)
