import interactions
import os 
import platform
import random
import requests
from interactions import *

token = "MTEzNDMxNjg5NjM0MzMwNjM4Mw.GdUlCX.A0KSAHnaHfSTrPlTQ8OAP3rxgrovPlu0hNrKHU"

meoaw = interactions.Client(token=token, intents=Intents.ALL)

ch_id = "1134315448939319296" # ช่องสำหรับส่ง panel

phone = "0997028658"

# Log Config

log_id = "1130191079900192800" # ไอดีช่องหลังบ้าน !

# Embed Config

m_title = "4K SHOP"

m_tn = "https://media.discordapp.net/attachments/1126090909600198737/1126420978461839450/11_AD3AC24.gif"

m_img = "https://media.discordapp.net/attachments/1126090909600198737/1126420978461839450/11_AD3AC24.gif"
# Role Config

role_01 = "1130073598237884487" # ไอดียศที่ 1

role01_name = "VIP ร้าน4K" # ชื่อยศที่ 1

role_01p = "20.00" # ราคายศที่ 1 ใส่ลงท้าย .00 เช่น 10 บาท ก็คือ 10.00

role_02 = "" # ไอดียศที่ 2

role02_name = "" # ชื่อยศที่ 2

role_02p = "" # ราคายศที่ 2 ใส่ลงท้าย .00 เช่น 20 บาท ก็คือ 20.00

role_03 = "" # ไอดียศที่ 3

role03_name = "" # ชื่อยศที่ 3

role_03p = "" # ราคายศที่ 3 ใส่ลงท้าย .00 เช่น 30 บาท ก็คือ 30.00


@interactions.listen()
async def on_ready():

    ch = await meoaw.fetch_channel(channel_id=ch_id)

    main_embed = interactions.Embed(title=f"**{m_title} Topup**", description="_ _", color=0x00FF00)

    main_embed.add_field(name="> วิธีใช้งาน", value="_ _\n`❓`: กดปุ่ม `เติมเงิน` เพื่อใช้งาน !\n_ _\n_ _")

    main_embed.set_thumbnail(m_tn) 

    main_embed.set_image(m_img)

    main_embed.set_footer("4K SHOP")

    topup = Button(
        style=ButtonStyle.GREEN,
        custom_id="topup_cb",
        label="เติมเงิน",
    )
    
    all = Button(
        style=ButtonStyle.SECONDARY,
        custom_id="all_cb",
        label="ดูยศทั้งหมด",
    )
    how_to = Button(
        style=ButtonStyle.BLUE,
        custom_id="how_cb",
        label="สอนซื้อ",
    )

    await ch.send(embeds=main_embed, components=[topup, all, how_to])


    if platform.system() == 'Windows':

        os.system(f'cls & title {m_title}')
        
        print(" ")

        print(f"{m_title}")

        print(" ")
    
    else:

        os.system("clear")

        print(" ")

        print(f"{m_title} Topup (5.1 )")

        print(" ")

@interactions.listen()
async def on_component(event: BaseComponent):

    ctx = event.ctx

    match ctx.custom_id:
        case "topup_cb": 
            select_plan = StringSelectMenu(
                [
                    interactions.StringSelectOption(label="เติมเงิน", emoji="💸", value="test"),
                ],
                placeholder="🟢 เลือกยศที่จะซื้อ",
                min_values=1,
                max_values=1,
            )

            await ctx.send(components=select_plan, ephemeral=True)

            def check(component: Button) -> bool:
                return component.ctx.author.id == ctx.author.id

            try:

                used_component = await meoaw.wait_for_component(components=select_plan, check=check, timeout=30)
                used_ctx = used_component.ctx

                rolebuy = used_ctx.values[0]

                topup_modal = Modal(
                    ShortText(
                    label="ลิงค์ซองของขวัญ",
                    custom_id="giftLink",
                    required=True,
                    placeholder="กรุณาใส่ลิ้งค์ซอง !",
                    max_length=80,
                    ),
                    title="🧧 เติมเงินรับยศ!",
                )
                await used_ctx.send_modal(modal=topup_modal)

                modal_ctx: ModalContext = await used_ctx.bot.wait_for_modal(topup_modal)

                giftLink = modal_ctx.responses['giftLink']

                auth = requests.get(f"https://zamex-hub.000webhostapp.com/index.php?phone={phone}&link={giftLink}")

                gotji = auth.json()

                if gotji["status"] == "SUCCESS":

                    if gotji["amount"] == role_01p:

                        role_01s = interactions.Embed(title=f"**{m_title} Success ( 1 )**", description="_ _", color=0x92f0a3)

                        role_01s.add_field(name="> สถานะ", value="_ _\n`✅`: ซื้อยศสำเร็จ\n_ _\n")

                        role_01s.add_field(name="> ยศที่ได้รับ", value=f"_ _\n`🎗️`: <@&{role_01}>\n_ _\n")

                        role_01s.add_field(name="> จำนวนเงิน", value=f"_ _\n`💸`: <@&{role_01p}>\n_ _\n")

                        await modal_ctx.author.add_role(role_01)

                        await ctx.send(embeds=role_01s, ephemeral=True)

                        log_01 = await meoaw.fetch_channel(channel_id=log_id)

                        log_01eb = interactions.Embed(title=f"**{m_title} Log**", description="_ _", color=0x75ffb1)

                        log_01eb.add_field(name="> สถานะ", value="_ _\n`✅`: ซื้อยศสำเร็จ !\n_ _\n_ _")

                        log_01eb.add_field(name="> ยศที่ได้รับ", value=f"_ _\n`❓`: <@&{role_01}>\n_ _\n_ _")

                        await log_01.send(f"<@{ctx.author.id}>", embeds=log_01eb)

                    elif gotji["amount"] == role_02p:

                        role_02s = interactions.Embed(title=f"**{m_title} Success ( 2 )**", description="_ _", color=0x92f0a3)

                        role_02s.add_field(name="> สถานะ", value="_ _\n`✅`: ซื้อยศสำเร็จ\n_ _\n")

                        role_02s.add_field(name="> ยศที่ได้รับ", value=f"_ _\n`🎗️`: <@&{role_02}>\n_ _\n")

                        role_02s.add_field(name="> จำนวนเงิน", value=f"_ _\n`💸`: <@&_{role_02p}>\n_ _\n")

                        await ctx.send(embeds=role_02s, ephemeral=True)

                        log_02 = await meoaw.fetch_channel(channel_id=log_id)

                        log_02eb = interactions.Embed(title=f"**{m_title} Log**", description="_ _", color=0x75ffb1)

                        log_02eb.add_field(name="> สถานะ", value="_ _\n`✅`: ซื้อยศสำเร็จ !\n_ _\n_ _")

                        log_02eb.add_field(name="> ยศที่ได้รับ", value=f"_ _\n`❓`: <@&{role_02}>\n_ _\n_ _")

                        await log_02.send(f"<@{ctx.author.id}>", embeds=log_02eb)

                    elif gotji["amount"] == role_03p:

                        role_03s = interactions.Embed(title=f"**{m_title} Success ( 3 )**", description="_ _", color=0x92f0a3)

                        role_03s.add_field(name="> สถานะ", value="_ _\n`✅`: ซื้อยศสำเร็จ\n_ _\n")

                        role_03s.add_field(name="> ยศที่ได้รับ", value=f"_ _\n`🎗️`: <@&{role_03}>\n_ _\n")

                        role_03s.add_field(name="> จำนวนเงิน", value=f"_ _\n`💸`: <@&{role_03p}>\n_ _\n")

                        await ctx.send(embeds=role_03s, ephemeral=True)

                        log_03 = await meoaw.fetch_channel(channel_id=log_id)

                        log_03eb = interactions.Embed(title=f"**{m_title} Log**", description="_ _", color=0x75ffb1)

                        log_03eb.add_field(name="> สถานะ", value="_ _\n`✅`: ซื้อยศสำเร็จ !\n_ _\n_ _")

                        log_03eb.add_field(name="> ยศที่ได้รับ", value=f"_ _\n`❓`: <@&{role_03}>\n_ _\n_ _")

                        await log_03.send(f"<@{ctx.author.id}>", embeds=log_03eb)

                    else:

                        role_04s = interactions.Embed(title=f"**{m_title} Success ( 4 )**", description="_ _", color=0xf59300)

                        role_04s.add_field(name="> สถานะ", value="_ _\n`✅`: ซื้อยศสำเร็จ\n_ _\n")

                        role_04s.add_field(name="> ยศที่ได้รับ", value=f"_ _\n`🎗️`: ไม่พบยศ !\n_ _\n")

                        role_04s.add_field(name="> จำนวนเงิน", value=f"_ _\n`💸`: ไม่สามารถดึงค่าได้ !\n_ _\n")

                        await ctx.send(embeds=role_04s, ephemeral=True)

                        log_04 = await meoaw.fetch_channel(channel_id=log_id)

                        log_04eb = interactions.Embed(title=f"**{m_title} Log**", description="_ _", color=0x75ffb1)

                        log_04eb.add_field(name="> สถานะ", value="_ _\n`❗`: เติมเงินเกินกว่าที่ระบบตั้งไว้ !\n_ _\n_ _")

                        await log_04.send(f"<@{ctx.author.id}>", embeds=log_04eb)
                        
                

                else:

                    print("Fail")

                    fail = interactions.Embed(title=f"**{m_title} Fail**", description="_ _", color=0xf50049)

                    fail.add_field(name="> สถานะ", value="_ _\n`❌`: เติมเงินไม่สำเร็จ\n_ _\n")

                    await ctx.send(embeds=fail, ephemeral=True)

                    fail_x = await meoaw.fetch_channel(channel_id=log_id)

                    faileb = interactions.Embed(title=f"**{m_title} Log**", description="_ _", color=0xff004c)

                    faileb.add_field(name="> สถานะ", value="_ _\n`❌`: เติมเงินไม่สำเร็จ\n_ _\n_ _")

                    await fail_x.send(f"<@{ctx.author.id}>", embeds=faileb)
                        
            except TimeoutError:

                print("Timed Out!")

        case "all_cb":

            role_all = interactions.Embed(title=f"**{m_title} Role**", description="_ _", color=0xeef092)

            role_all.add_field(name=f"> ยศ {role01_name}", value=f"_ _\n<@&{role_01}>\n_ _\n`💰`: `{role_01p}`\n_ _\n_ _")

            role_all.add_field(name=f"> ยศ {role02_name}", value=f"_ _\n<@&{role_02}>\n_ _\n`💰`: `{role_02p}`\n_ _\n_ _")

            role_all.add_field(name=f"> ยศ {role03_name}", value=f"_ _\n<@&{role_03}>\n_ _\n`💰`: `{role_03p}`\n_ _\n_ _")

            role_all.set_footer("4K SHOP")

            await ctx.send(embeds=role_all, ephemeral=True)


        case "how_cb":
            await ctx.send("https://cdn.discordapp.com/attachments/1058504363036917920/1135588994059608134/lv_0_20230731201117.mp4")
        

meoaw.start(token)

# Code by Meoaw | discord.gg/meoaw | Last update 23/4/66 10:42
