import os
import re
import textwrap
import aiofiles
import aiohttp
import numpy as np
import random
from PIL import Image, ImageChops, ImageOps, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from AnonXMusic.resource import thumbs, color
from AnonXMusic import app
from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def add_corners(im):
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, im.split()[-1])
    im.putalpha(mask)


async def gen_thumb(videoid, user_id):
    if os.path.isfile(f"cache/{videoid}_{user_id}.png"):
        return f"cache/{videoid}_{user_id}.png"
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                result["viewCount"]["short"]
            except:
                pass
            try:
                result["channel"]["name"]
            except:
                pass

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        try:
            wxyz = await bot.get_profile_photos(user_id)
            wxy = await bot.download_media(wxyz[0]['file_id'], file_name=f'{user_id}.jpg')
        except:
            abc = await bot.get_profile_photos(bot.id)
            wxy = await bot.download_media(abc[0]['file_id'], file_name=f'{bot.id}.jpg')
        xy = Image.open(wxy)
        a = Image.new('L', [640, 640], 0)
        b = ImageDraw.Draw(a)
        b.pieslice([(0, 0), (640,640)], 0, 360, fill = 255, outline = "white")
        c = np.array(xy)
        d = np.array(a)
        e = np.dstack((c, d))
        f = Image.fromarray(e)
        x = f.resize((107, 107))

        images = random.choice(thumbs)
        border = random.choice(colors)
        youtube = Image.open(f"cache/thumb{videoid}.png")
        bg = Image.open(f"AnonXMusic/resource/{images}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        image3 = changeImageSize(1280, 720, bg)
        image5 = image3.convert("RGBA")
        Image.alpha_composite(background, image5).save(f"cache/temp{videoid}.png")

        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo.save(f"cache/chop{videoid}.png")
        if not os.path.isfile(f"cache/cropped{videoid}.png"):
            im = Image.open(f"cache/chop{videoid}.png").convert("RGBA")
            add_corners(im)
            im.save(f"cache/cropped{videoid}.png")

        crop_img = Image.open(f"cache/cropped{videoid}.png")
        logo = crop_img.convert("RGBA")
        logo.thumbnail((365, 365), Image.ANTIALIAS)
        width = int((1280 - 365) / 2)
        background = Image.open(f"cache/temp{videoid}.png")
        background.paste(logo, (width + 2, 138), mask=logo)
        background.paste(x, (710, 427), mask=x)
        background.paste(image3, (0, 0), mask=image3)
        img = ImageOps.expand(background, border=10, fill=f"{border}")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("AnonXMusic/resource/font2.ttf", 45)
        ImageFont.truetype("AnonXMusic/resource/font2.ttf", 70)
        arial = ImageFont.truetype("AnonXMusic/resource/font2.ttf", 30)
        ImageFont.truetype("AnonXMusic/resource/font.ttf", 30)
        para = textwrap.wrap(title, width=32)
        try:
            draw.text(
                (450, 35),
                f"STARTED PLAYING",
                fill="white",
                stroke_width=1,
                stroke_fill="white",
                font=font,
            )
            if para[0]:
                text_w, text_h = draw.textsize(f"{para[0]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 560),
                    f"{para[0]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
            if para[1]:
                text_w, text_h = draw.textsize(f"{para[1]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 610),
                    f"{para[1]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
        except:
            pass
        text_w, text_h = draw.textsize(f"Duration: {duration} Mins", font=arial)
        draw.text(
            ((1280 - text_w) / 2, 665),
            f"Duration: {duration} Mins",
            fill="white",
            font=arial,
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        img.save(f"cache/{videoid}_{user_id}.png")
        return f"cache/{videoid}_{user_id}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL


async def que_thumb(videoid, user_id):
    if os.path.isfile(f"cache/que{videoid}_{user_id}.png"):
        return f"cache/que{videoid}_{user_id}.png"
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                result["viewCount"]["short"]
            except:
                pass
            try:
                result["channel"]["name"]
            except:
                pass

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        try:
            wxyz = await bot.get_profile_photos(user_id)
            wxy = await bot.download_media(wxyz[0]['file_id'], file_name=f'{user_id}.jpg')
        except:
            abc = await bot.get_profile_photos(bot.id)
            wxy = await bot.download_media(abc[0]['file_id'], file_name=f'{bot.id}.jpg')
        xy = Image.open(wxy)
        a = Image.new('L', [640, 640], 0)
        b = ImageDraw.Draw(a)
        b.pieslice([(0, 0), (640,640)], 0, 360, fill = 255, outline = "white")
        c = np.array(xy)
        d = np.array(a)
        e = np.dstack((c, d))
        f = Image.fromarray(e)
        x = f.resize((107, 107))

        images = random.choice(thumbs)
        border = random.choice(colors)
        youtube = Image.open(f"cache/thumb{videoid}.png")
        bg = Image.open(f"AnonXMusic/resource/{images}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        image3 = changeImageSize(1280, 720, bg)
        image5 = image3.convert("RGBA")
        Image.alpha_composite(background, image5).save(f"cache/temp{videoid}.png")

        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo.save(f"cache/chop{videoid}.png")
        if not os.path.isfile(f"cache/cropped{videoid}.png"):
            im = Image.open(f"cache/chop{videoid}.png").convert("RGBA")
            add_corners(im)
            im.save(f"cache/cropped{videoid}.png")

        crop_img = Image.open(f"cache/cropped{videoid}.png")
        logo = crop_img.convert("RGBA")
        logo.thumbnail((365, 365), Image.ANTIALIAS)
        width = int((1280 - 365) / 2)
        background = Image.open(f"cache/temp{videoid}.png")
        background.paste(logo, (width + 2, 138), mask=logo)
        background.paste(x, (710, 427), mask=x)
        background.paste(image3, (0, 0), mask=image3)
        img = ImageOps.expand(background, border=10, fill=f"{border}")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("AnonXMusic/resource/font2.ttf", 45)
        ImageFont.truetype("AnonXMusic/resource/font2.ttf", 70)
        arial = ImageFont.truetype("AnonXMusic/resource/font2.ttf", 30)
        ImageFont.truetype("AnonXMusic/resource/font.ttf", 30)
        para = textwrap.wrap(title, width=32)
        try:
            draw.text(
                (455, 35),
                "ADDED TO QUEUE",
                fill="white",
                stroke_width=1,
                stroke_fill="white",
                font=font,
            )
            if para[0]:
                text_w, text_h = draw.textsize(f"{para[0]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 560),
                    f"{para[0]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
            if para[1]:
                text_w, text_h = draw.textsize(f"{para[1]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 610),
                    f"{para[1]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
        except:
            pass
        text_w, text_h = draw.textsize(f"Duration: {duration} Mins", font=arial)
        draw.text(
            ((1280 - text_w) / 2, 665),
            f"Duration: {duration} Mins",
            fill="white",
            font=arial,
        )

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        file = f"cache/que{videoid}_{user_id}.png"
        img.save(f"cache/que{videoid}_{user_id}.png")
        return f"cache/que{videoid}_{user_id}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
