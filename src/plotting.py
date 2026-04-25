from __future__ import annotations


def get_plotly_go() -> object:
    """Import Plotly graph objects with a user-friendly error."""
    try:
        import plotly.graph_objects as go
    except ModuleNotFoundError as exc:
        raise ValueError(
            "Thiếu package `plotly`. Hãy cài dependencies từ `requirements.txt` trước khi xem biểu đồ."
        ) from exc

    return go


def create_line_figure(
    x_values,
    y_values,
    name: str,
    title: str,
    xaxis_title: str,
    yaxis_title: str,
) -> object:
    """Create a line chart with the shared Plotly layout."""
    go = get_plotly_go()
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines+markers",
            name=name,
        )
    )
    figure.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        margin=dict(l=20, r=20, t=50, b=20),
        height=380,
    )
    return figure


def create_bar_figure(
    x_values,
    y_values,
    name: str,
    title: str,
    xaxis_title: str,
    yaxis_title: str,
) -> object:
    """Create a bar chart with the shared Plotly layout."""
    go = get_plotly_go()
    figure = go.Figure(data=[go.Bar(x=x_values, y=y_values, name=name)])
    figure.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        margin=dict(l=20, r=20, t=50, b=20),
        height=320,
    )
    return figure


def create_multi_line_figure(
    series_list: list[dict],
    title: str,
    xaxis_title: str,
    yaxis_title: str,
    height: int = 380,
) -> object:
    """Create a multi-series line chart with the shared Plotly layout."""
    go = get_plotly_go()
    figure = go.Figure()
    for series in series_list:
        figure.add_trace(
            go.Scatter(
                x=series["x"],
                y=series["y"],
                mode=series.get("mode", "lines+markers"),
                name=series["name"],
            )
        )

    figure.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        margin=dict(l=20, r=20, t=50, b=20),
        height=height,
    )
    return figure
