<p align="center">
    <h2 align="center">Code::Stats Profile Readme</h2>
    <p align="center">Get dynamically generated <a href="https://codestats.net">Code::Stats</a> stats on your profile readme!</p>
</p>

<p align="center">
    <a href="#demo">View Demo</a>
    ·
    <a href="https://github.com/WEGFan/codestats-profile-readme/issues">Report Bug</a>
    ·
    <a href="https://github.com/WEGFan/codestats-profile-readme/issues">Request Feature</a>
</p>

---

> Note that Github's server aborts the request if it reaches the 4-second timeout. So maybe the images won't show because my server is waiting for response from Code::Stats, try refreshing and see if it shows.  
> To prevent heavy load from Code::Stats server, all data from same user will be cached for 30 minutes before updating data.

## Features <!-- omit in toc -->

- [Code::Stats History Graph](#codestats-history-graph)
  - [Increasing history days](#increasing-history-days)
  - [Increasing maximum languages](#increasing-maximum-languages)
  - [Customizing colors](#customizing-colors)
  - [More customization](#more-customization)
  - [Demo](#demo)
- [Deploy on your own server](#deploy-on-your-own-server)

## Code::Stats History Graph

Simply add this to your markdown and change `username` to your Code::Stats username.

```markdown
![My Code::Stats history graph](https://codestats-readme.wegfan.cn/history-graph/username)
```

### Increasing history days

You can increase history days up to 30 days by adding a query parameter `?history_days=`

```markdown
![My Code::Stats history graph](https://codestats-readme.wegfan.cn/history-graph/username?history_days=30)
```

### Increasing maximum languages

You can increase maximum languages up to 15 by adding a query parameter `?max_languages=`

```markdown
![My Code::Stats history graph](https://codestats-readme.wegfan.cn/history-graph/username?max_languages=15)
```

### Customizing colors

You can customize the colors of grid, text, zeroline and bars by adding `grid_color`, `text_color`, `zeroline_color` and `language_colors` query parameters.

The `language_colors` is a list of colors seperated by comma and wrapped with `[]`, each color should be wrapped with quotes (e.g. `["red","hsl(0,100%,50%)","rgba(255,0,0,0.5)"]`)

```markdown
![My Code::Stats history graph](https://codestats-readme.wegfan.cn/history-graph/username?grid_color=e8e8e8&text_color=666666&zeroline_color=ababab&language_colors=["red","green","blue"])
```

See [color string](#color-string) below for supported color representations.

### More customization

| query parameter | type                                | description                                                                             | default value                                                                          |
| --------------- | ----------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| history_days    | integer                             | how many days to show in the graph, maximum 30                                          | 14                                                                                     |
| max_languages   | integer                             | how many languages to show before grouping into "Others", maximum 15                    | 8                                                                                      |
| timezone        | [timezone string](#timezone-string) | what timezone to use to calculate day ranges                                            | 00:00                                                                                  |
| width           | integer                             | the width of image (in pixels)                                                          | 900                                                                                    |
| height          | integer                             | the height of image (in pixels)                                                         | 450                                                                                    |
| show_legend     | boolean                             | whether to show graph legend on the right                                               | true                                                                                   |
| bg_color        | [color string](#color-string)       | the color of the image's background                                                     | ffffff                                                                                 |
| grid_color      | [color string](#color-string)       | the color of the grid                                                                   | e8e8e8                                                                                 |
| text_color      | [color string](#color-string)       | the color of the text                                                                   | 666666                                                                                 |
| zeroline_color  | [color string](#color-string)       | the color of the zero-line                                                              | ababab                                                                                 |
| language_colors | [color string](#color-string) list  | the colors of each langauge and "Others" (loops if length is less than `max_languages`) | \["3e4053","f15854","5da5da", "faa43a","60bd68","f17cb0", "b2912f","decf3f","b276b2"\] |

**Special types:**

<span id="color-string">Color string</span>

- A hex string without `#` (e.g. `ff0000`, `ADE` for `aaddee`)
- An rgb/rgba string (e.g. `rgb(255,0,0)`, `rgba(0,128,128,0.5)`)
- An hsl/hsla string (e.g. `hsl(0,100%,50%)`, `hsla(60,50%,50%,0.7)`)
- An hsv/hsva string (e.g. `hsv(0,100%,100%)`, `hsva(120,100%,100%,0.5)`)
- A named CSS color, full list [here](http://www.w3.org/TR/css3-color/#svg-color)
  
<span id="timezone-string">Timezone string</span>

- A string describing a timezone (e.g. `US/Pacific`, `Europe/Berlin`)
- A string in ISO 8601 style (e.g. `07:30`, `-05:00`, `0630`, `-08`)

### Demo

- Default

![WEGFan's Code::Stats history graph](https://codestats-readme.wegfan.cn/history-graph/WEGFan)

- Smaller with fewer history days & languages

![WEGFan's Code::Stats history graph](https://codestats-readme.wegfan.cn/history-graph/WEGFan?width=500&height=200&history_days=7&max_languages=5)

- Customizing colors

![WEGFan's Code::Stats history graph](https://codestats-readme.wegfan.cn/history-graph/WEGFan?bg_color=111&text_color=aaa&grid_color=333&language_colors=["3e4053","cc4b48","518fbd","ba7a2b","60bd68","f17cb0","b2912f","c71585","b276b2"])

---

## Deploy on your own server

You can also deploy this project on your own server by following the instructions below.

Prerequisites:

- [Python 3.6 64-bit](https://www.python.org/downloads/) or later. (64-bit is required because [kaleido](https://github.com/plotly/Kaleido) is currently not providing 32-bit pre-compiled wheels)
- **(Optional)** [Redis](https://redis.io/download/) for caching. If not installed, the app will use a file system cache instead, which is not very performant thus it is highly recommended that you configure a Redis server.
- **(Optional)** [SVGO](https://github.com/svg/svgo) for optimizing SVGs (also requires [Node.js](https://nodejs.org/en/download/))

1. Clone the project: `git clone https://github.com/WEGFan/codestats-profile-readme && cd codestats-profile-readme`
2. Install requirements: `pip install -r requirements.txt`
3. Edit your config in [config/custom_config.py](config/custom_config.py).
4. Run: `gunicorn -c gunicorn_config.py run:app`, and you should be able to access it by `http://127.0.0.1:2012` on your server
