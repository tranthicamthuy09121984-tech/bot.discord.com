const { Client, GatewayIntentBits, EmbedBuilder, REST, Routes, SlashCommandBuilder } = require('discord.js');
require('dotenv').config();

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const commands = [
  new SlashCommandBuilder().setName('help').setDescription('Xem các lệnh'),
  new SlashCommandBuilder().setName('weather').setDescription('Xem thời tiết')
    .addStringOption(o => o.setName('thanh_pho').setDescription('Tên thành phố').setRequired(true)),
].map(c => c.toJSON());

const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);

client.on('ready', async () => {
  console.log(`Bot online: ${client.user.tag}`);
  try {
    await rest.put(Routes.applicationCommands(client.user.id), { body: commands });
    console.log('Đã đăng ký lệnh /help và /weather');
  } catch (e) { console.error(e); }
});

client.on('interactionCreate', async interaction => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === 'help') {
    const embed = new EmbedBuilder()
      .setTitle('🤖 URobot - Danh sách lệnh')
      .setColor(0x00ff00)
      .addFields(
        { name: '/help', value: 'Hiện bảng này', inline: true },
        { name: '/weather [thành phố]', value: 'Xem thời tiết VD: /weather Ho Chi Minh', inline: true },
      );
    await interaction.reply({ embeds: [embed] });
  }

  if (interaction.commandName === 'weather') {
    await interaction.deferReply();
    const city = interaction.options.getString('thanh_pho');
    try {
      const res = await fetch(`https://wttr.in/${city}?format=j1`);
      const data = await res.json();
      const cur = data.current_condition[0];
      await interaction.editReply(`**Thời tiết ${city}:** ${cur.weatherDesc[0].value} - ${cur.temp_C}°C (cảm giác ${cur.FeelsLikeC}°C)`);
    } catch {
      await interaction.editReply(`Không tìm thấy thời tiết cho ${city} 😢`);
    }
  }
});

client.login(process.env.DISCORD_TOKEN);