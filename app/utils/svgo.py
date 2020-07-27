# -*- coding: utf-8 -*-
import subprocess

from flask import current_app


def try_optimize_svg(original: str) -> str:
    if not current_app.config['SVG_OPTIMIZE_ENABLE']:
        return original
    args = [
        current_app.config['SVGO_PATH'],
        '--input', '-',
        '--output', '-',
        '--config', current_app.config['SVGO_CONFIG_PATH']
    ]
    try:
        with subprocess.Popen(args, encoding='utf-8',
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            try:
                (stdout, stderr) = proc.communicate(original, timeout=3)
                if stderr:
                    current_app.logger.warning('svg optimize error: %s', stderr)
                    return original
                current_app.logger.info('svg optimized %d bytes -> %d bytes', len(original), len(stdout))
                return stdout
            except subprocess.TimeoutExpired as err:
                current_app.logger.warning('svg optimize timeout')
    except Exception as err:
        current_app.logger.exception(err)
    return original
