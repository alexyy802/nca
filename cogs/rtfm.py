import io
import os
import re
import zlib
from typing import Dict, Iterable, Tuple, Optional

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context


def finder(text: str, collection: Iterable, *, key: str = None, lazy: bool = True):
    suggestions = []
    text = str(text)
    pat = '.*?'.join(map(re.escape, text))
    regex = re.compile(pat, flags=re.IGNORECASE)
    for item in collection:
        to_search = key(item) if key else item
        r = regex.search(to_search)
        if r:
            suggestions.append((len(r.group()), r.start(), item))

    def sort_key(tup: Tuple):
        if key:
            return tup[0], tup[1], key(tup[2])
        return tup

    if lazy:
        return (z for _, _, z in sorted(suggestions, key=sort_key))
    return [z for _, _, z in sorted(suggestions, key=sort_key)]


class SphinxObjectFileReader:
    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer: bytes):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode('utf-8')

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b''
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b'\n')
            while pos != -1:
                yield buf[:pos].decode('utf-8')
                buf = buf[pos + 1:]
                pos = buf.find(b'\n')


def parse_object_inv(stream: SphinxObjectFileReader, url: str):
    # key: URL
    # n.b.: key doesn't have `discord` or `discord.ext.commands` namespaces
    result = {}

    # first line is version info
    inv_version = stream.readline().rstrip()

    if inv_version != '# Sphinx inventory version 2':
        raise RuntimeError('Invalid objects.inv file version.')

    # next line is "# Project: <name>"
    # then after that is "# Version: <version>"
    projname = stream.readline().rstrip()[11:]
    stream.readline()

    # next line says if it's a zlib header
    line = stream.readline()
    # if 'zlib' not in line:
    #     raise RuntimeError('Invalid objects.inv file, not z-lib compatible.')

    # This code mostly comes from the Sphinx repository.
    entry_regex = re.compile(r'(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)')
    for line in stream.read_compressed_lines():
        match = entry_regex.match(line.rstrip())
        if not match:
            continue

        name, directive, _, location, dispname = match.groups()
        domain, _, subdirective = directive.partition(':')
        if directive == 'py:module' and name in result:
            # From the Sphinx Repository:
            # due to a bug in 1.1 and below,
            # two inventory entries are created
            # for Python modules, and the first
            # one is correct
            continue

        # Most documentation pages have a label
        if directive == 'std:doc':
            subdirective = 'label'

        if location.endswith('$'):
            location = location[:-1] + name

        key = name if dispname == '-' else dispname
        prefix = f'{subdirective}:' if domain == 'std' else ''

        if projname == 'discord.py':
            key = key.replace('discord.ext.commands.', '').replace('discord.', '')

        result[f'{prefix}{key}'] = os.path.join(url, location)

    return result


class Rtfm(Cog, name="Discordpy Documentation"):
    """
    Cog to have fancy discordpy doc embeds

    thanks danny :)
    """
    def __init__(self, bot):
        self.bot = bot
        self._cache = {}

    async def build_rtfm_lookup_table(self, page_types: Dict[str, str]):
        cache = {}
        for key, page in page_types.items():
            async with aiohttp.ClientSession() as session:
                resp = await session.get(page + '/objects.inv')
                if resp.status != 200:
                    return -1
                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = parse_object_inv(stream, page)
        self._cache = cache
        return 1

    async def do_rtfm(self, ctx: Context, key: str, obj: Optional[str]):
        page_types = {
            'discord.py': 'https://discordpy.readthedocs.io/en/master',
            'python': 'https://docs.python.org/3'
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if len(self._cache) == 0:
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)

        if key.startswith('discord.py'):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == '_':
                    continue
                if q == name:
                    obj = f'abc.Messageable.{name}'
                    break

        cache = list(self._cache[key].items())

        matches = finder(obj, cache, key=lambda t: t[0], lazy=False)[:5]

        if len(matches) == 0:
            return await ctx.send('Couldn\'t find anything, sorry.')

        e = discord.Embed(colour=discord.Colour.blurple(),
                          title=f'{key} documentation')
        e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
        e.set_footer(text='Inspired by https://github.com/Rapptz/RoboDanny')
        await ctx.send(embed=e)

    @commands.command(name='dpy_docs', aliases=['dpy', 'rtfm'])
    async def dpy_docs(self, ctx: Context, *, obj: str = None):
        await self.do_rtfm(ctx, 'discord.py', obj)

    @commands.command(name='py_docs', aliases=['py'])
    async def py_docs(self, ctx: Context, *, obj: str = None):
        await self.do_rtfm(ctx, 'python', obj)


def setup(client):
 client.add_cog(Rtfm(bot))
