import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import List, Optional, Union, Any, Dict

# Constants
SEQUENTIAL_COLORS = [
    "#E5FAFF",
    "#B7F2FF",
    "#8AEAFF",
    "#5CE1FF",
    "#2FD9FF",
    "#00D1FF",
    "#00B0D6",
    "#006D85",
    "#004B5C",
]
CATEGORICAL_COLORS = ["#00D1FF", "#EB46FF", "#6B59FF", "#4FD1C5", "#1F68AC", "#FDE8FF"]
FONT_FAMILY = "sans-serif"
PLOTLY_TEMPLATE = "plotly_dark"
DEFAULT_LINE_COLOR = "white"
DEFAULT_LINE_WIDTH = 0
HELP_TEXT_BGCOLOR = "#333333"
HELP_TEXT_FONT_SIZE = 14
HELP_TEXT_FONT_COLOR = "white"


def set_axes(fig, x_format: str, y_format: str):
    """Format axes based on specified formats."""
    format_map = {"%": ".2%", "$": "$", "#": None}

    fig.update_yaxes(
        tickformat=format_map[y_format] if y_format == "%" else None,
        tickprefix=format_map[y_format] if y_format != "%" else None,
    )
    fig.update_xaxes(
        tickformat=format_map[x_format] if x_format == "%" else None,
        tickprefix=format_map[x_format] if x_format != "%" else None,
    )

    return fig


def update_layout(
    fig,
    orientation: str = "v",
    help_text: Optional[str] = None,
    custom_data: Optional[Dict[str, Any]] = None,
    hover_template: Optional[str] = None,
):
    """Apply common layout updates to the figure.

    Args:
        fig: The plotly figure to update.
        orientation: The orientation of the chart ("v" for vertical, "h" for horizontal).
        help_text: Optional text to display in the top-right corner of the chart.
        custom_data: Optional data to add to the chart.
        hover_template: Optional template for the chart's hover tooltip.
    """
    fig.update_xaxes(title_text="", automargin=True)
    fig.update_yaxes(title_text="")
    fig.update_traces(hovertemplate=None)

    # Add help text annotation to top-right corner of chart
    if help_text is not None:
        fig.update_layout(
            annotations=[
                dict(
                    x=1,
                    y=1.25,
                    xref="paper",
                    yref="paper",
                    text="❔",
                    showarrow=False,
                    font=dict(size=20),
                    xanchor="right",
                    yanchor="top",
                    hovertext=help_text,
                    hoverlabel=dict(
                        bgcolor=HELP_TEXT_BGCOLOR,
                        font_size=HELP_TEXT_FONT_SIZE,
                        font_color=HELP_TEXT_FONT_COLOR,
                    ),
                )
            ]
        )

    # Format the chart's hover tooltip
    for t in fig.data:
        t.hovertemplate = hover_template

    # Add custom data to chart
    if custom_data is not None:
        custom_df = custom_data.get("df")
        if isinstance(custom_df, pd.DataFrame) and not custom_df.empty:
            line_color = custom_data.get("line_color", DEFAULT_LINE_COLOR)
            line_width = custom_data.get("line_width", DEFAULT_LINE_WIDTH)
            custom_trace = go.Scatter(
                x=custom_df.iloc[:, 0],
                y=custom_df.iloc[:, 1],
                mode="lines",
                line=dict(color=line_color, width=line_width),
                name=custom_data.get("name", "Custom Data"),
                showlegend=custom_data.get("showlegend", False),
            )
            fig.add_trace(custom_trace)
        for t in fig.data:
            if t.name == custom_data.get("name", "Custom Data"):
                t.hovertemplate = custom_data.get("hover_template", None)

    # Add legend to chart and set hover mode
    fig.update_layout(
        hovermode=f"{'y' if orientation == 'h' else 'x'} unified",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5,
            title=None,
        ),
        font=dict(family=FONT_FAMILY),
    )
    return fig


def chart_many_bars(
    df,
    x_col: str,
    y_cols: List[str],
    title: str,
    color: Optional[str] = None,
    x_format: str = "#",
    y_format: str = "$",
    help_text: Optional[str] = None,
):
    """Create a bar chart with multiple series."""
    fig = px.bar(
        df,
        x=x_col,
        y=y_cols,
        title=title,
        color=color,
        color_discrete_sequence=CATEGORICAL_COLORS,
        template=PLOTLY_TEMPLATE,
    )
    fig = set_axes(fig, x_format, y_format)
    fig.update_xaxes(title_text="", automargin=True)
    fig.update_yaxes(title_text="")
    fig.update_layout(
        font=dict(family=FONT_FAMILY),
    )
    return update_layout(fig, help_text=help_text)


def chart_many_lines(
    df,
    x_col: str,
    y_cols: List[str],
    title: str,
    color: Optional[str] = None,
    x_format: str = "#",
    y_format: str = "$",
    help_text: Optional[str] = None,
):
    """Create a line chart with multiple series."""
    fig = px.line(
        df,
        x=x_col,
        y=y_cols,
        title=title,
        color=color,
        color_discrete_sequence=CATEGORICAL_COLORS,
        template=PLOTLY_TEMPLATE,
    )
    fig = set_axes(fig, x_format, y_format)
    return update_layout(fig, help_text=help_text)


def chart_bars(
    df,
    x_col: str,
    y_cols: Union[str, List[str]],
    title: str,
    color: Optional[str] = None,
    x_format: str = "#",
    y_format: str = "$",
    column: bool = False,
    barmode: str = "relative",
    help_text: Optional[str] = None,
    custom_data: Optional[Dict[str, Any]] = None,
    hover_template: Optional[str] = None,
):
    """Create a bar chart."""
    fig = px.bar(
        df,
        x=x_col,
        y=y_cols,
        title=title,
        color=color,
        color_discrete_sequence=CATEGORICAL_COLORS,
        template=PLOTLY_TEMPLATE,
        orientation="h" if column else "v",
        barmode=barmode,
    )
    fig = set_axes(fig, x_format, y_format)
    return update_layout(
        fig,
        orientation="h" if column else "v",
        help_text=help_text,
        custom_data=custom_data,
        hover_template=hover_template,
    )


def chart_area(
    df,
    x_col: str,
    y_cols: Union[str, List[str]],
    title: str,
    color: Optional[str] = None,
    x_format: str = "#",
    y_format: str = "$",
    column: bool = False,
    help_text: Optional[str] = None,
    custom_data: Optional[Dict[str, Any]] = None,
    hover_template: Optional[str] = None,
):
    """Create an area chart."""
    fig = px.area(
        df,
        x=x_col,
        y=y_cols,
        title=title,
        color=color,
        color_discrete_sequence=CATEGORICAL_COLORS,
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(hovertemplate=None)
    fig = set_axes(fig, x_format, y_format)
    return update_layout(
        fig,
        orientation="h" if column else "v",
        help_text=help_text,
        custom_data=custom_data,
        hover_template=hover_template,
    )


def chart_lines(
    df,
    x_col: str,
    y_cols: Union[str, List[str]],
    title: str,
    color: Optional[str] = None,
    smooth: bool = False,
    x_format: str = "#",
    y_format: str = "$",
    help_text: Optional[str] = None,
):
    """Create a line chart."""
    fig = px.line(
        df,
        x=x_col,
        y=y_cols,
        title=title,
        color=color,
        color_discrete_sequence=CATEGORICAL_COLORS,
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(line_shape=None if smooth else "hv")
    fig = set_axes(fig, x_format, y_format)
    return update_layout(fig, help_text=help_text)


def chart_oi(df, x_col: str, title: str, help_text: Optional[str] = None):
    """Create an Open Interest chart."""
    fig = px.area(
        df,
        x=x_col,
        y=["short_oi_pct", "long_oi_pct"],
        line_shape="hv",
        color_discrete_sequence=["red", "green"],
        title=title,
    )
    fig.update_yaxes(tickformat=".0%")
    return update_layout(fig, help_text=help_text)
