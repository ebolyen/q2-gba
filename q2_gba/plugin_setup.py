# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import io
import os
import base64
import shutil

from qiime.plugin import Plugin, Int, Properties, SemanticType, FileFormat, DataLayout


plugin = Plugin(
    name='gba',
    version='0.0.1dev',
    website='https://github.com/ebolyen/q2-gba',
    package='q2_gba'
)


Game = SemanticType('Game', field_names='type')
GBA = SemanticType('GBA', variant_of=Game.field['type'])

plugin.register_semantic_type(Game)
plugin.register_semantic_type(GBA)


class GBAFormat(FileFormat):
    name = 'GBA'

    @classmethod
    def sniff(cls, filepath):
        return True


ROM_data_layout = DataLayout('rom', 1)
ROM_data_layout.register_file('game.gba', GBAFormat)
plugin.register_type_to_data_layout(Game[GBA], 'rom', 1)


def ROM_data_layout_to_buffered_reader(data_dir):
    return open(os.path.join(data_dir, 'game.gba'), 'rb')


def buffered_reader_to_ROM_data_layout(view, data_dir):
    with open(os.path.join(data_dir, 'game.gba'), 'wb') as fh:
        fh.write(view.read())


plugin.register_data_layout(ROM_data_layout)

plugin.register_data_layout_reader('rom', 1, io.BufferedReader,
                                   ROM_data_layout_to_buffered_reader)

plugin.register_data_layout_writer('rom', 1, io.BufferedReader,
                                   buffered_reader_to_ROM_data_layout)


def play(output_dir : str, rom : io.BufferedReader) -> None:
    with open(os.path.join(output_dir, 'gameloader.js'), 'wb') as fh:
        fh.write(b"onDataLoad('" + base64.b64encode(rom.read()) + b"');")

    copytree(os.path.join(os.path.dirname(__file__), 'assets'),
             os.path.join(output_dir))


# From http://stackoverflow.com/a/12514470/579416
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


plugin.visualizers.register_function(
    function=play,
    inputs={'rom': Game[GBA]},
    parameters={},
    name='View GBA',
    description='Visualize .gba files.'
)
