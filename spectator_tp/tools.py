import json
from mcdreforged.api.types import ServerInterface
from spectator_tp.config import st_config as config


def tr(key, *args):
    return ServerInterface.get_instance().tr(f"spectator_tp.{key}", *args)


def save_json_file(target_dir: str, dic: dict):
    with open(target_dir, "w", encoding="utf-8") as fp:
        json.dump(dic, fp, indent=4, ensure_ascii=False)


def transfer(x, operation='*'):
    """
    对浮点数进行乘8或除8运算
    :param x: 输入数值（整数或浮点数）
    :param operation: '*' 表示乘8, '/' 表示除8
    :return: 运算结果（浮点数）
    """
    # 将输入转换为浮点数
    num = float(x)

    # 根据操作类型计算
    if operation == '*':
        result = num * 8.0
    elif operation == '/':
        result = num / 8.0
    else:
        return

    # 处理小数位数（使用格式化和转换保证浮点数输出）
    # 转换会确保至少一位小数，最多15位小数
    return float(
        format(result, '.15g').rstrip('0').rstrip('.') + '0' if '.' not in format(result, '.15g'
                                                                                  ) else format(result, '.15g').rstrip(
            '0').rstrip('.') or '0.0'
    )


def update_config(old_config, template=config.get_default().serialize()):
    for key in template:
        if key not in old_config:
            old_config[key] = template[key]
        else:
            old_val = old_config[key]
            template_val = template[key]
            if isinstance(old_val, dict) and isinstance(template_val, dict):
                update_config(old_val, template_val)
            elif isinstance(old_val, list) and isinstance(template_val, list):
                for i in range(len(template_val)):
                    if i < len(old_val):
                        old_elem = old_val[i]
                        template_elem = template_val[i]
                        if isinstance(old_elem, dict) and isinstance(template_elem, dict):
                            update_config(old_elem, template_elem)
                    else:
                        old_val.append(template_val[i])
    return old_config
