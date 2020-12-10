# -*- coding: utf-8 -*-
import bisect
import math
from typing import List

import arrow
import plotly.graph_objects as go
from flask import Blueprint, current_app, request, Response
from marshmallow import EXCLUDE, ValidationError

from app.models.codestats_user import User
from app.models.daily_language_xp import DailyLanguageXp
from app.models.history_graph_config import GraphConfig
from app.schemas.history_graph_config import GraphConfigSchema
from app.utils.svgo import try_optimize_svg
from config import custom_config

history_graph = Blueprint('history_graph', __name__, url_prefix='/history-graph')


def calculate_best_range(y_max):
    exponent = math.floor(math.log10(y_max))
    fraction = y_max / 10 ** exponent
    possible_fractions = [1, 2, 5, 10]
    new_fraction = possible_fractions[bisect.bisect_left(possible_fractions[:-1], fraction)]
    tick_delta = new_fraction * 10 ** (exponent - 1)
    return math.ceil(y_max / tick_delta) * tick_delta


def get_graph(day_language_xp_list: List[DailyLanguageXp], config: GraphConfig):
    today = arrow.utcnow().to(config.timezone)
    first_day = today.shift(days=-config.history_days + 1)
    date_array = [day.date() for day in arrow.Arrow.range('day', first_day, today)]

    language_xp_dict = {}

    # accumulate xp per day for every language
    for obj in day_language_xp_list:
        try:
            pos = date_array.index(obj.date)
        except ValueError as err:
            continue
        xp_per_day = language_xp_dict.setdefault(obj.language, [0] * config.history_days)
        xp_per_day[pos] += obj.xp

    # sort by the sum of xp
    language_xp_list = list(filter(lambda s: s[0] not in custom_config.IGNORE_LIST, language_xp_dict.items()))
    language_xp_list.sort(key=lambda k_v: sum(k_v[1]), reverse=True)

    # not using day_language_xp_list because it may contains data not in date range
    no_data = True if not language_xp_list else False

    # if language number exceeds max_languages, group them into others
    if len(language_xp_list) > config.max_languages:
        others_xp_per_day_list = [
            xp_per_day
            for (language, xp_per_day) in language_xp_list[config.max_languages:]
        ]
        others_xp_per_day_sum = [
            sum(x) for x in zip(*others_xp_per_day_list)
        ]
        language_xp_list = (language_xp_list[:config.max_languages] +
                            [('Others', others_xp_per_day_sum)])

    # calculate the best range for y axis
    if no_data:
        # if the user has no data
        max_daily_xp = 0
    else:
        max_daily_xp = max(
            sum(x)
            for x in zip(*[v for (k, v) in language_xp_list])
        )
    max_daily_xp = max(max_daily_xp, 1)  # prevent math error caused by no data
    y_range = calculate_best_range(max_daily_xp)

    x_axis = [date.strftime('%b %e') for date in date_array]
    if no_data:
        # make a empty bar
        bars = [
            go.Bar(
                name='', x=x_axis, y=[0] * config.history_days, width=0.7,
                marker=go.bar.Marker(
                    line=go.bar.marker.Line(
                        width=0
                    )
                )
            )
        ]
    else:
        bars = [
            go.Bar(
                name=language, x=x_axis, y=xp_per_day, width=0.7,
                marker=go.bar.Marker(
                    color=config.language_colors[idx % len(config.language_colors)],
                    line=go.bar.marker.Line(
                        width=0
                    )
                )
            )
            for (idx, (language, xp_per_day)) in enumerate(language_xp_list)
        ]

    fig = go.Figure(
        data=bars,
        layout=go.Layout(
            paper_bgcolor=config.bg_color,
            plot_bgcolor=config.bg_color,
            width=config.width,
            height=config.height,
            barmode='stack',
            showlegend=False if no_data else config.show_legend,
            legend=go.layout.Legend(
                traceorder='normal',
                x=1,
                font=go.layout.legend.Font(
                    color=config.text_color
                )
            ),
            xaxis=go.layout.XAxis(
                type='category',
                tickmode='array',
                ticks='outside',
                ticklen=4,
                tickwidth=1,
                tickcolor=config.grid_color,
                tickson='boundaries',
                tickfont=go.layout.xaxis.Tickfont(
                    color=config.text_color,
                ),
                tickangle=-45,
                gridcolor=config.grid_color,
                gridwidth=1,
                dtick=1,
                showline=False,
                linecolor=config.grid_color
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text='XP',
                    standoff=10,
                    font=go.layout.yaxis.title.Font(
                        color=config.text_color
                    )
                ),
                ticks='outside',
                ticklen=4,
                tickwidth=1,
                tickcolor=config.grid_color,
                tickformat=',d',
                tickfont=go.layout.yaxis.Tickfont(
                    color=config.text_color
                ),
                gridcolor=config.grid_color,
                gridwidth=1,
                showline=True,
                linecolor=config.grid_color,
                zeroline=True,
                zerolinecolor=config.zeroline_color,
                zerolinewidth=1,
                separatethousands=True,
                range=[0, y_range]
            ),
            margin=go.layout.Margin(
                t=0,
                b=0,
                l=0,
                r=0,
                pad=0
            )
        )
    )
    # manually add top border
    fig.add_shape(
        type='line',
        x0=-0.5,
        y0=y_range,
        x1=config.history_days - 0.5,
        y1=y_range,
        line=go.layout.shape.Line(
            color=config.grid_color,
            width=2
        )
    )

    return fig


@history_graph.route('/<string:username>', methods=['GET'])
def get_history_graph(username: str):
    args = request.args.to_dict(flat=True)
    current_app.logger.info('args: %s', args)

    try:
        config: GraphConfig = GraphConfigSchema(unknown=EXCLUDE).load(args)
    except ValidationError as err:
        raise err

    # restricting usage to my user only
    if username != custom_config.USERNAME:
        user = User(custom_config.USERNAME)
    else:
        user = User(username)
    user.set_real_username()

    today = arrow.utcnow().to(config.timezone)
    # get history for 30 days directly to cache data
    first_day = today.shift(days=-30 + 1)
    day_language_xp_list = user.get_day_language_xp_list(first_day)

    graph = get_graph(day_language_xp_list, config)

    svg = graph.to_image('svg', engine='kaleido', width=config.width, height=config.height, scale=1)
    if current_app.config['SVG_OPTIMIZE_ENABLE']:
        svg = try_optimize_svg(svg.decode('utf-8'))

    return Response(svg, mimetype='image/svg+xml', headers={
        'Cache-Control': 'max-age=0'
    })
