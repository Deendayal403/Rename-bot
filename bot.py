from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server



class Bot(Client):
    global client 

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        # Initialize the global client object here
        global client 
        client = self

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME     
        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()       
            await web.TCPSite(app, "0.0.0.0", 8080).start()     
        print(f"{me.first_name} Is Started.....✨️")

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"{me.mention} Is Restarted !!\n\n📅 Date : {date}\n⏰ Time : {time}\n🌐 Timezone : Asia/Kolkata\n\n🉐 Version : v{__version__} (Layer {layer})</b>")                                
            except:
                print("Please Make This Is Admin In Your Log Channel")

    # Handle FloodWait Error 
    async def authorize(self):
        try:
            await super().authorize()
            print("Bot successfully authorized.")
        except pyrogram.errors.exceptions.flood_420.FloodWait as e:
            print(f"Flood Wait: {e}")
            time.sleep(e.x) # Flood Wait की अवधि के लिए wait करें
            await self.authorize() # फिर से authorize करने की कोशिश करें 

# ... अन्य functions ...

if __name__ == "__main__":
    Bot().run()






# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @JishuBotz
# Developer @JishuDeveloper
