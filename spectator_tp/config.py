from mcdreforged.api.utils.serializer import Serializable


class st_config(Serializable):
    dim_convert: dict = {
        "0": "minecraft:overworld",
        "-1": "minecraft:the_nether",
        "1": "minecraft:the_end"
    }
    dim_translation: dict = {
        "minecraft:overworld": "主世界",
        "minecraft:the_nether": "下界",
        "minecraft:the_end": "末地"
    }
    prefix: str = "!tp"
    plugin_version: str = "1.0.0"
