import os
import time
import shutil
import asyncio
import traceback
from ..functions.filters import OWNER_FILTER
from ..functions.helper import (
    progress_for_pyrogram,
    download_file,
    absolute_paths,
    send_media,
    URL_REGEX
)
from ..config import Config
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from .. import client


@Client.on_message(filters.regex(pattern=URL_REGEX) & OWNER_FILTER & filters.private)
async def linkloader(bot: Client, update: Message):
    dirs = f'{Config.DOWNLOAD_DIR}{update.from_user.id}'
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    filename = f'{dirs}.zip'
    pablo = await update.reply_text('Downloading...')
    urls = URL_REGEX.findall(update.text)
    rm, total, up = len(urls), len(urls), 0
    await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
    for url in urls:
        await download_file(url, dirs)
        up += 1
        rm -= 1
        try:
            await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        except FloodWait as e:
            client.logger.warning(
                'Floodwait for {} seconds'.format(e.value))
            await asyncio.sleep(e.value)
            await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        except Exception:
            client.logger.warning(traceback.format_exc())
    await pablo.edit_text('Uploading...')
    if Config.AS_ZIP:
        shutil.make_archive(dirs, 'zip', dirs)
        start_time = time.time()
        try:
            sended_media = await update.reply_document(
                document=filename,
                thumb=client.custom_thumbnail.get(update.from_user.id),
                caption=client.custom_caption.get(update.from_user.id, ''),
                progress=progress_for_pyrogram,
                progress_args=(
                    'Uploading...',
                    pablo,
                    start_time
                )
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            sended_media = await update.reply_document(
                document=filename,
                thumb=client.custom_thumbnail.get(update.from_user.id),
                caption=client.custom_caption.get(update.from_user.id, ''),
                progress=progress_for_pyrogram,
                progress_args=(
                    'Uploading...',
                    pablo,
                    start_time
                )
            )
        except Exception:
            client.logger.warning(traceback.format_exc())
        if Config.DUMP_ID:
            try:
                await sended_media.forward(Config.DUMP_ID)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await sended_media.forward(Config.DUMP_ID)
            except Exception:
                client.logger.warning(traceback.format_exc())
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    else:
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
        for files in dldirs:
            await send_media(files, pablo)
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except Exception:
                client.logger.warning(traceback.format_exc())
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)


@Client.on_message(filters.document & OWNER_FILTER & filters.private)
async def documentloader(bot: Client, update: Message):
    dirs = f'{Config.DOWNLOAD_DIR}{update.from_user.id}'
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    if not update.document.file_name.endswith(('.txt', '.text')):
        return
    filename = f'{Config.DOWNLOAD_DIR}.zip'
    pablo = await update.reply_text('Downloading...')
    fl = await update.download()
    with open(fl) as f:
        urls = URL_REGEX.findall(f.read())
    os.remove(fl)
    rm, total, up = len(urls), len(urls), 0
    await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
    for url in urls:
        await download_file(url, dirs)
        up += 1
        rm -= 1
        try:
            await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        except FloodWait as e:
            client.logger.warning(
                'Floodwait for {} seconds'.format(e.value))
            await asyncio.sleep(e.value)
            await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        except Exception:
            client.logger.warning(traceback.format_exc())
    await pablo.edit_text('Uploading...')
    if Config.AS_ZIP:
        shutil.make_archive(dirs, 'zip', dirs)
        start_time = time.time()
        try:
            sended_media = await update.reply_document(
                document=filename,
                thumb=client.custom_thumbnail.get(update.from_user.id),
                caption=client.custom_caption.get(update.from_user.id, ''),
                progress=progress_for_pyrogram,
                progress_args=(
                    'Uploading...',
                    pablo,
                    start_time
                )
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            sended_media = await update.reply_document(
                document=filename,
                thumb=client.custom_thumbnail.get(update.from_user.id),
                caption=client.custom_caption.get(update.from_user.id, ''),
                progress=progress_for_pyrogram,
                progress_args=(
                    'Uploading...',
                    pablo,
                    start_time
                )
            )
        except Exception:
            client.logger.warning(traceback.format_exc())
        if Config.DUMP_ID:
            try:
                await sended_media.forward(Config.DUMP_ID)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await sended_media.forward(Config.DUMP_ID)
            except Exception:
                client.logger.warning(traceback.format_exc())
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    else:
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
        for media in dldirs:
            try:
                await send_media(media, pablo)
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await send_media(media, pablo)
            except Exception:
                client.logger.warning(traceback.format_exc())
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except FloodWait as e:
                client.logger.warning(
                    'Floodwait for {} seconds'.format(e.value))
                await asyncio.sleep(e.value)
                await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
            except Exception:
                client.logger.warning(traceback.format_exc())
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)
