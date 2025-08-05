import os

from mcdreforged.api.decorator import new_thread
from mcdreforged.api.types import PluginServerInterface, InfoCommandSource, \
    ServerInterface
from mcdreforged.api.command import SimpleCommandBuilder, Number, Text, Integer
from spectator_tp.config import st_config
from spectator_tp.tools import update_config, save_json_file, tr, transfer
from spectator_tp.json_message import Message

CONFIG_NAME = "spectator_tp.json"
dim_translation = st_config.dim_translation
dim_convert = st_config.dim_convert
Prefix = st_config.prefix
short_command = st_config.short_command


def print_help_msg(src: InfoCommandSource):
    src.reply(
        Message.get_json_str(tr("introduction.help_message", Prefix, short_command, "Spectator TP", st_config.plugin_version))
    )


def on_load(server: PluginServerInterface, old):
    global dim_translation, dim_convert, Prefix, short_command
    config_folder = server.get_data_folder()
    if not os.path.exists(os.path.join(config_folder, CONFIG_NAME)):
        server.save_config_simple(st_config.get_default(), CONFIG_NAME)

    else:
        old_dict = server.load_config_simple(CONFIG_NAME, target_class=st_config, echo_in_console=False).serialize()
        new_dict = update_config(old_dict)
        if new_dict["plugin_version"] != st_config.plugin_version:
            new_dict["plugin_version"] = st_config.plugin_version

        save_json_file(os.path.join(config_folder, CONFIG_NAME), new_dict)

    cfg = server.load_config_simple(CONFIG_NAME, target_class=st_config)

    Prefix = cfg.prefix
    dim_translation = cfg.dim_translation
    dim_convert = cfg.dim_convert
    short_command = cfg.short_command
    short_command_enable = cfg.short_command_enable
    server.register_help_message(f"{short_command}", tr("introduction.short_msg"))
    server.register_help_message(f"{Prefix} help", tr("introduction.register_message"))
    builder = SimpleCommandBuilder()

    builder.command(f"{Prefix}", dimension_teleport)
    if short_command_enable:
        builder.command(f"{short_command}", dimension_teleport)
    builder.command(f"{Prefix} help", print_help_msg)
    builder.command(f"{Prefix} id <id1>", dimension_teleport)
    builder.command(f"{Prefix} id <id1> <id2>", dimension_teleport)
    builder.command(f"{Prefix} <x> <y> <z>", dimension_teleport)
    builder.command(f"{Prefix} <x> <y> <z> in <dimension>", dimension_teleport)

    builder.arg("id1", Text)
    builder.arg("id2", Text)
    builder.arg("x", Number)
    builder.arg("y", Number)
    builder.arg("z", Number)
    builder.arg("dimension", Integer)

    builder.register(server)


def get_PlayerInfo(name: str, data_path: str = ''):
    api = ServerInterface.get_instance().get_plugin_instance('minecraft_data_api')
    info = api.get_player_info(name, data_path)
    return info


def is_spector_or_creative(name: str):
    result = get_PlayerInfo(name, data_path="playerGameType")
    return result in (1, 3) if result is not None else None


def get_player_list():
    api = ServerInterface.get_instance().get_plugin_instance('minecraft_data_api')
    return api.get_server_player_list()


@new_thread("Spectator TP")
def dimension_teleport(src: InfoCommandSource, dic: dict):
    if not src.is_player:
        src.reply(tr("command.not_player"))
        return

    server = src.get_server()
    player = src.get_info().player

    if "id1" in dic and src.get_info().content != short_command:
        lst = get_player_list()
        if not lst:
            src.reply(tr("command.get_list_timeout"))
            return

        if "id2" in dic:
            p1, p2 = dic['id1'], dic['id2']
            if dic['id1'] not in lst[-1]:
                src.reply(tr("command.offline", p1))
                return

            if dic['id2'] not in lst[-1]:
                src.reply(tr("command.offline", p2))
                return

            result = is_spector_or_creative(p1)
            if result:
                server.execute(f"tp {p1} {p2}")
                src.reply(tr("command.id_tp", p1, p2))

            elif result is None:
                src.reply(tr("command.get_info_timeout"))

            else:
                src.reply(tr("command.mode_error", p1))

            return

        p1 = dic["id1"]

        if p1 not in lst[-1]:
            src.reply(tr("command.offline", p1))
            return

        result = is_spector_or_creative(player)
        if result:
            server.execute(f"tp {player} {p1}")
            src.reply(tr("command.id_tp", player, p1))

        elif result is None:
            src.reply(tr("command.get_info_timeout"))

        else:
            src.reply(tr("command.mode_error", player))

        return

    if "z" in dic and src.get_info().content != short_command:
        result = is_spector_or_creative(player)
        if result is None:
            src.reply(tr("command.get_info_timeout", player))
            return

        elif result is False:
            src.reply(tr("command.mode_error", player))
            return

        x, y, z = dic["x"], dic["y"], dic["z"]

        if "dimension" in dic:
            dimension = dic["dimension"]
            dimension = dim_convert.get(str(dimension))
            if not dimension:
                src.reply(tr("command.unidentified_dimension"))
                return
            server.execute(f'execute in {dimension} run tp {player} {x} {y} {z}')
            src.reply(Message.get_json_str(tr(
                "command.pos_tp", player, dim_translation.get(dimension)
                if dim_translation.get(dimension) else dimension, f"{x:.2f}", f"{y:.2f}", f"{z:.2f}"
            )))
            return

        dimension = get_PlayerInfo(player, "Dimension")

        if dimension is None:
            src.reply(tr("command.get_info_timeout", player))
            return

        server.execute(f'execute in {dimension} run tp {player} {x} {y} {z}')
        src.reply(Message.get_json_str(tr(
            "command.pos_tp", player, dim_translation.get(dimension)
            if dim_translation.get(dimension) else dimension, f"{x:.2f}", f"{y:.2f}", f"{z:.2f}"
        )))

    if not dic:

        mode = get_PlayerInfo(player, "playerGameType")

        if mode is None:
            src.reply(tr("command.get_info_timeout", player))
            return

        if mode not in (1, 3):
            src.reply(tr("command.mode_error", player))
            return

        dimension = get_PlayerInfo(player, "Dimension")

        if dimension is None:
            src.reply(tr("command.get_info_timeout", player))
            return

        if dimension == "minecraft:overworld":
            pos = get_PlayerInfo(player, "Pos")
            if pos is None:
                src.reply(tr("command.get_info_timeout", player))
                return
            x, y, z = transfer(pos[0], "/"), pos[1], transfer(pos[2], "/")
            server.execute(f'execute in minecraft:the_nether run tp {player} {x} {y} {z}')
            src.reply(Message.get_json_str(
                tr("command.pos_tp", player, dim_translation["minecraft:the_nether"], f"{x:.2f}", f"{y:.2f}",
                   f"{z:.2f}")))
            return

        elif dimension == "minecraft:the_nether":
            pos = get_PlayerInfo(player, "Pos")
            if pos is None:
                src.reply(tr("command.get_info_timeout", player))
                return
            x, y, z = transfer(pos[0]), pos[1], transfer(pos[2])
            server.execute(
                f'execute in minecraft:overworld run tp {player} {x} {y} {z}')
            src.reply(Message.get_json_str(
                tr("command.pos_tp", player, dim_translation["minecraft:overworld"], f"{x:.2f}", f"{y:.2f}",
                   f"{z:.2f}")))
            return

        src.reply(tr("command.dimension_error"))
