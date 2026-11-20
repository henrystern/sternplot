"""Functions for modifying plot layouts."""

from sternplot.config import site_colour


def add_notes(fig, note, x=0, y="auto"):
    """Add note to bottom left of figure."""
    if isinstance(note, list):
        note = "<br>".join(note)
    if y == "auto":
        y = -0.15 - 0.05 * note.count("<br>")

    text_colour = fig.layout.template.layout.font.color
    fig.add_annotation(
        dict(
            x=x,
            y=y,
            xref="x domain",
            yref="y domain",
            text=note,
            showarrow=False,
            font=dict(color=text_colour),  # inherit size
            align="left",
        )
    )
    return fig


def inset_legend_layout(fig, x=0.02, y=0.99):
    """Get legend layout to inset legend in plot."""
    return fig.update_legends(
        dict(
            yanchor="top",
            y=y,
            xanchor="left",
            x=x,
            bordercolor=site_colour["dark_grey"],
            borderwidth=2,
        )
    )


def annotate_trace_items(
    fig, use_colour=True, xshift=8, yshift=0, font_size=12
):
    """Replace the plot legend with annotations next to each item."""
    for _, tr in enumerate(fig.data):
        if tr.x is None or len(tr.x) == 0:
            continue
        color = (
            tr.line.color
            if tr.line and tr.line.color and use_colour
            else (
                fig.layout.font.color
                or fig.layout.template.layout.font.color
                or ["#444"]
            )
        )
        fig.add_annotation(
            x=tr.x[0],
            y=tr.y[0],
            text=tr.name,
            showarrow=False,
            xref=tr.xaxis or "x",
            yref=tr.yaxis or "y",
            xanchor="left",
            xshift=xshift,
            yshift=yshift,
            font=dict(color=color, size=font_size),
        )
    return fig.update_layout(showlegend=False)


def hide_legend_items(fig, to_keep=[], to_hide=[], patch={}):
    """Hide traces that aren't in to_keep or are in to_hide."""
    patch = dict(visible=True) | patch
    return fig.for_each_trace(
        lambda x: x.update(patch if x.name not in to_hide else False)
    ).for_each_trace(
        lambda x: x.update(patch if x.name not in to_keep else True)
    )


def inset_facet_row_annotations(
    fig, selector=lambda x: x.textangle == 90, patch={}
):
    """Move the facet row annotations to go under the column annotations"""
    return fig.for_each_annotation(
        lambda x: x.update(
            dict(
                textangle=0,
                xref="x2 domain",
                x=0.5,
                xanchor="center",
                y=x.y + 0.255,
            )
            | patch
        ),
        selector,
    )


def split_facet_annotations(fig, selector=lambda x: "=" in x.text, patch={}):
    """Split the variable name from the facet annotations."""
    return fig.for_each_annotation(
        lambda a: a.update(
            dict(text=a.text.split("=")[-1]) | patch,
        ),
        selector=selector,
    )
