const { Client, GatewayIntentBits, REST, Routes, SlashCommandBuilder } = require('discord.js');

const TOKEN = 'MTUzMjcyMDY1MDU0MjY0NTQyMQ.GARqxu.98xmBfsY2M89ahXC0_icih3IB5603_rjww8lso';
const CLIENT_ID = '1532720650542645421';

const client = new Client({ 
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] 
});

const commands = [
  new SlashCommandBuilder().setName('ping').setDescription('Bot cua Nguyen')
].map(c => c.toJSON());

const rest = new REST({ version: '10' }).setToken('MTUzMjcyMDY1MDU0MjY0NTQyMQ.GARqxu.98xmBfsY2M89ahXC0_icih3IB5603_rjww8lso');
(async () => {
  await rest.put(Routes.applicationCommands(1532720650542645421), { body: commands });
  console.log('Da dang ky /ping');
})();

client.on('clientReady', () => {
  console.log('Bot online! ' + client.user.tag);
});

client.on('interactionCreate', async interaction => {
  if (!interaction.isChatInputCommand()) return;
  if (interaction.commandName === 'ping') {
    await interaction.reply('Pong! Bot cua Nguyen day! ' + client.ws.ping + 'ms');
  }
});

client.login('MTUzMjcyMDY1MDU0MjY0NTQyMQ.GARqxu.98xmBfsY2M89ahXC0_icih3IB5603_rjww8lso');