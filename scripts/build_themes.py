#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "themes" / "source-theme.json"
THEME_FILE = ROOT / "themes" / "flat-theme.json"
README_FILE = ROOT / "README.md"

README_START = "<!-- GENERATED:palette:start -->"
README_END = "<!-- GENERATED:palette:end -->"


def hex_to_rgba(color: str, alpha: str) -> str:
    return f"{color}{alpha}"


def build_players(accent_colors: list[str]) -> list[dict[str, str]]:
    players = []
    for color in accent_colors[:7]:
        players.append(
            {
                "cursor": color,
                "selection": hex_to_rgba(color, "33"),
                "background": color,
            }
        )
    players.append(players[0].copy())
    return players


def syntax_block(palette: dict[str, str], text_color: str) -> dict[str, dict[str, object]]:
    def token(color: str, font_style: str | None = None, font_weight: int | None = None) -> dict[str, object]:
        return {
            "color": color,
            "font_style": font_style,
            "font_weight": font_weight,
        }

    punctuation = palette["punctuation"]
    keyword = palette["keyword"]
    function = palette["function"]
    member = palette["member"]
    string = palette["string"]
    constant = palette["constant"]
    type_color = palette["type"]
    operator = palette["operator"]
    comment = palette["comment"]

    return {
        "variable": token(text_color),
        "variable.builtin": token(palette["builtin"], "italic"),
        "variable.parameter": token(palette["parameter"]),
        "variable.member": token(member),
        "variable.special": token(palette["special_variable"], "italic"),
        "constant": token(constant),
        "constant.builtin": token(constant),
        "constant.macro": token(palette["macro"]),
        "module": token(palette["module"], "italic"),
        "label": token(member),
        "string": token(string),
        "string.documentation": token(string),
        "string.regexp": token(palette["regexp"]),
        "string.escape": token(palette["escape"]),
        "string.special": token(palette["escape"]),
        "string.special.path": token(string),
        "string.special.symbol": token(constant),
        "string.special.url": token(palette["symbol"], "italic"),
        "character": token(string),
        "character.special": token(palette["escape"]),
        "boolean": token(constant),
        "number": token(constant),
        "number.float": token(constant),
        "type": token(type_color),
        "type.builtin": token(type_color, "italic"),
        "type.definition": token(type_color),
        "type.interface": token(type_color, "italic"),
        "type.super": token(type_color, "italic"),
        "attribute": token(palette["attribute"]),
        "property": token(member),
        "function": token(function),
        "function.builtin": token(function),
        "function.call": token(function),
        "function.macro": token(palette["attribute"]),
        "function.method": token(function),
        "function.method.call": token(function),
        "constructor": token(palette["constructor"]),
        "operator": token(operator),
        "keyword": token(keyword),
        "keyword.modifier": token(keyword),
        "keyword.type": token(keyword),
        "keyword.coroutine": token(keyword),
        "keyword.function": token(keyword),
        "keyword.operator": token(operator),
        "keyword.import": token(keyword),
        "keyword.repeat": token(keyword),
        "keyword.return": token(keyword),
        "keyword.debug": token(keyword),
        "keyword.exception": token(keyword),
        "keyword.conditional": token(keyword),
        "keyword.conditional.ternary": token(keyword),
        "keyword.directive": token(keyword),
        "keyword.directive.define": token(keyword),
        "keyword.export": token(keyword),
        "punctuation": token(punctuation),
        "punctuation.delimiter": token(punctuation),
        "punctuation.bracket": token(punctuation),
        "punctuation.special": token(operator),
        "punctuation.special.symbol": token(constant),
        "punctuation.list_marker": token(palette["parameter"]),
        "comment": token(comment),
        "comment.doc": token(comment),
        "comment.documentation": token(comment),
        "comment.error": token(palette["parameter"], "italic", 700),
        "comment.warning": token(type_color, "italic", 700),
        "comment.hint": token(operator, "italic", 700),
        "comment.todo": token(keyword, "italic", 700),
        "comment.note": token(member, "italic", 700),
        "diff.plus": token(string),
        "diff.minus": token(palette["parameter"]),
        "tag": token(palette["tag"]),
        "tag.attribute": token(palette["tag_attribute"]),
        "tag.delimiter": token(palette["tag_delimiter"]),
        "parameter": token(palette["parameter"]),
        "field": token(member),
        "namespace": token(type_color),
        "float": token(constant),
        "symbol": token(palette["symbol"]),
        "string.regex": token(palette["regexp"]),
        "text": token(text_color),
        "emphasis.strong": token(palette["parameter"], None, 700),
        "emphasis": token(palette["parameter"], "italic"),
        "embedded": token(text_color),
        "text.literal": token(palette["text_literal"]),
        "concept": token(type_color),
        "enum": token(type_color),
        "function.decorator": token(function),
        "type.class.definition": token(type_color),
        "hint": token(operator, "italic", 700),
        "link_text": token(palette["symbol"], "italic"),
        "link_uri": token(palette["symbol"]),
        "parent": token(text_color),
        "predictive": token(palette["predictive"], "italic"),
        "predoc": token(palette["predictive"]),
        "primary": token(text_color),
        "tag.doctype": token(keyword),
        "string.doc": token(string, "italic"),
        "title": token(palette["title"], None, 700),
        "variant": token(type_color),
    }


def build_style(variant: dict[str, object]) -> dict[str, object]:
    ui = variant["ui"]
    term = variant["terminal"]
    palette = variant["syntax_palette"]
    accent = ui["accent"]
    text = ui["text"]
    muted = ui["muted"]
    placeholder = ui["placeholder"]
    disabled = ui["disabled"]
    background = ui["background"]
    chrome = ui["chrome"]
    editor = ui["editor"]
    elevated = ui["elevated"]
    element = ui["element"]
    element_hover = ui["element_hover"]
    element_active = ui["element_active"]
    guide = ui["guide"]
    unreachable = ui["unreachable"]
    predictive = ui["predictive"]

    accent_colors = [
        accent,
        palette["member"],
        palette["string"],
        palette["type"],
        palette["keyword"],
        palette["function"],
        palette["parameter"],
    ]

    return {
        "accents": [hex_to_rgba(color, "66") for color in accent_colors],
        "background.appearance": "opaque",
        "border": hex_to_rgba(background, "00"),
        "border.variant": accent,
        "border.focused": accent,
        "border.selected": accent,
        "border.transparent": hex_to_rgba(background, "00"),
        "border.disabled": placeholder,
        "elevated_surface.background": elevated,
        "surface.background": chrome,
        "background": background,
        "element.background": element,
        "element.hover": element_hover,
        "element.active": element_active,
        "element.selected": element_active,
        "element.disabled": disabled,
        "drop_target.background": hex_to_rgba(accent, "66"),
        "ghost_element.background": "#00000000",
        "ghost_element.hover": element,
        "ghost_element.active": element_active,
        "ghost_element.selected": element_active,
        "ghost_element.disabled": disabled,
        "text": text,
        "text.muted": muted,
        "text.placeholder": placeholder,
        "text.disabled": disabled,
        "text.accent": accent,
        "icon": text,
        "icon.muted": muted,
        "icon.disabled": disabled,
        "icon.placeholder": placeholder,
        "icon.accent": accent,
        "status_bar.background": chrome,
        "title_bar.background": chrome,
        "title_bar.inactive_background": background,
        "toolbar.background": chrome,
        "tab_bar.background": chrome,
        "tab.inactive_background": chrome,
        "tab.active_background": element,
        "search.match_background": ui["search_match"],
        "panel.background": chrome,
        "panel.focused_border": accent,
        "panel.indent_guide": ui["guide_panel"],
        "panel.indent_guide_active": accent,
        "panel.indent_guide_hover": accent,
        "panel.overlay_background": elevated,
        "pane.focused_border": accent,
        "pane_group.border": hex_to_rgba(background, "00"),
        "scrollbar.thumb.background": ui["scrollbar_thumb"],
        "scrollbar.thumb.hover_background": ui["scrollbar_thumb_hover"],
        "scrollbar.thumb.border": "#00000000",
        "scrollbar.track.background": chrome,
        "scrollbar.track.border": hex_to_rgba(background, "00"),
        "editor.foreground": text,
        "editor.background": editor,
        "editor.gutter.background": editor,
        "editor.subheader.background": editor,
        "editor.active_line.background": ui["active_line"],
        "editor.highlighted_line.background": None,
        "editor.line_number": ui["line_number"],
        "editor.active_line_number": ui["active_line_number"],
        "editor.invisible": disabled,
        "editor.wrap_guide": guide,
        "editor.active_wrap_guide": placeholder,
        "editor.document_highlight.bracket_background": hex_to_rgba(accent, "20"),
        "editor.document_highlight.read_background": hex_to_rgba(accent, "10"),
        "editor.document_highlight.write_background": hex_to_rgba(accent, "22"),
        "editor.indent_guide": guide,
        "editor.indent_guide_active": accent,
        "terminal.background": editor,
        "terminal.ansi.background": editor,
        "terminal.foreground": text,
        "terminal.dim_foreground": muted,
        "terminal.bright_foreground": ui["active_line_number"],
        "terminal.ansi.black": term["black"],
        "terminal.ansi.red": term["red"],
        "terminal.ansi.green": term["green"],
        "terminal.ansi.yellow": term["yellow"],
        "terminal.ansi.blue": term["blue"],
        "terminal.ansi.magenta": term["magenta"],
        "terminal.ansi.cyan": term["cyan"],
        "terminal.ansi.white": term["white"],
        "terminal.ansi.bright_black": term["bright_black"],
        "terminal.ansi.bright_red": term["red"],
        "terminal.ansi.bright_green": term["green"],
        "terminal.ansi.bright_yellow": term["yellow"],
        "terminal.ansi.bright_blue": term["blue"],
        "terminal.ansi.bright_magenta": term["magenta"],
        "terminal.ansi.bright_cyan": term["cyan"],
        "terminal.ansi.bright_white": term["bright_white"],
        "terminal.ansi.dim_black": term["dim_black"],
        "terminal.ansi.dim_red": term["red"],
        "terminal.ansi.dim_green": term["green"],
        "terminal.ansi.dim_yellow": term["yellow"],
        "terminal.ansi.dim_blue": term["blue"],
        "terminal.ansi.dim_magenta": term["magenta"],
        "terminal.ansi.dim_cyan": term["cyan"],
        "terminal.ansi.dim_white": term["dim_white"],
        "link_text.hover": ui["link_hover"],
        "conflict": palette["type"],
        "conflict.border": palette["type"],
        "conflict.background": hex_to_rgba(palette["type"], "26"),
        "created": palette["string"],
        "created.border": palette["string"],
        "created.background": hex_to_rgba(palette["string"], "26"),
        "deleted": palette["parameter"],
        "deleted.border": palette["parameter"],
        "deleted.background": hex_to_rgba(palette["parameter"], "26"),
        "hidden": muted,
        "hidden.border": muted,
        "hidden.background": hex_to_rgba(editor, "26"),
        "hint": palette["attribute"],
        "hint.border": palette["attribute"],
        "hint.background": hex_to_rgba(editor, "26"),
        "ignored": muted,
        "ignored.border": muted,
        "ignored.background": hex_to_rgba(editor, "26"),
        "modified": palette["type"],
        "modified.border": palette["type"],
        "modified.background": hex_to_rgba(palette["type"], "26"),
        "predictive": predictive,
        "predictive.border": accent,
        "predictive.background": hex_to_rgba(editor, "26"),
        "renamed": palette["function"],
        "renamed.border": palette["function"],
        "renamed.background": hex_to_rgba(palette["function"], "26"),
        "info": palette["member"],
        "info.border": palette["member"],
        "info.background": hex_to_rgba(palette["member"], "26"),
        "warning": palette["type"],
        "warning.border": palette["type"],
        "warning.background": hex_to_rgba(palette["type"], "26"),
        "error": palette["parameter"],
        "error.border": palette["parameter"],
        "error.background": hex_to_rgba(palette["parameter"], "26"),
        "success": palette["string"],
        "success.border": palette["string"],
        "success.background": hex_to_rgba(palette["string"], "26"),
        "unreachable": unreachable,
        "unreachable.border": unreachable,
        "unreachable.background": hex_to_rgba(editor, "26"),
        "players": build_players(accent_colors),
        "version_control.added": palette["string"],
        "version_control.added_background": hex_to_rgba(palette["string"], "26"),
        "version_control.deleted": palette["parameter"],
        "version_control.deleted_background": hex_to_rgba(palette["parameter"], "26"),
        "version_control.modified": palette["type"],
        "version_control.modified_background": hex_to_rgba(palette["type"], "26"),
        "version_control.renamed": palette["function"],
        "version_control.conflict": palette["type"],
        "version_control.conflict_background": hex_to_rgba(palette["type"], "26"),
        "version_control.ignored": muted,
        "syntax": syntax_block(palette, text),
    }


def relative_luminance(color: str) -> float:
    color = color.lstrip("#")
    values = [int(color[i : i + 2], 16) / 255 for i in (0, 2, 4)]

    def convert(channel: float) -> float:
        if channel <= 0.04045:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4

    r, g, b = [convert(value) for value in values]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(color_a: str, color_b: str) -> float:
    a = relative_luminance(color_a)
    b = relative_luminance(color_b)
    high, low = sorted((a, b), reverse=True)
    return (high + 0.05) / (low + 0.05)


def validate_theme(theme: dict[str, object]) -> list[str]:
    style = theme["style"]
    errors = []
    editor_background = style["editor.background"]
    terminal_background = style["terminal.background"]
    checks = [
        ("editor.foreground", style["editor.foreground"], editor_background, 7.0),
        ("text.muted", style["text.muted"], editor_background, 4.5),
        ("editor.line_number", style["editor.line_number"], editor_background, 4.0),
        ("syntax.comment", style["syntax"]["comment"]["color"], editor_background, 4.5),
        ("terminal.ansi.black", style["terminal.ansi.black"], terminal_background, 2.5),
        ("terminal.ansi.white", style["terminal.ansi.white"], terminal_background, 4.5),
        ("terminal.ansi.bright_white", style["terminal.ansi.bright_white"], terminal_background, 7.0),
    ]
    for name, foreground, background, minimum in checks:
        value = contrast(foreground, background)
        if value < minimum:
            errors.append(
                f"{theme['name']}: {name} contrast {value:.2f} is below {minimum:.1f}"
            )
    if contrast(
        style["terminal.ansi.bright_white"], terminal_background
    ) < contrast(style["terminal.ansi.white"], terminal_background):
        errors.append(f"{theme['name']}: bright white is dimmer than white")
    return errors


def render_theme_document(source: dict[str, object]) -> str:
    document = {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": source["name"],
        "author": source["author"],
        "themes": [],
    }
    for variant in source["variants"]:
        document["themes"].append(
            {
                "name": variant["name"],
                "appearance": variant["appearance"],
                "style": build_style(variant),
            }
        )
    return json.dumps(document, indent=2) + "\n"


def render_readme_palettes(source: dict[str, object]) -> str:
    lines = []
    for variant in source["variants"]:
        lines.append(f"### {variant['name']}")
        for label, value in variant["readme_palette"].items():
            description = {
                "Background": "base editor canvas",
                "Foreground": "default editor text",
                "Accent": "focus and UI feedback",
                "Keywords": "language keywords",
                "Functions": "functions and methods",
                "Strings": "strings and text literals",
                "Numbers": "numbers and constants",
                "Comments": "comments and doc comments",
            }[label]
            lines.append(f"- **{label}**: `{value}` - {description}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def update_readme(readme_text: str, palette_text: str) -> str:
    start = readme_text.index(README_START) + len(README_START)
    end = readme_text.index(README_END)
    return readme_text[:start] + "\n" + palette_text + readme_text[end:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    source = json.loads(SOURCE_FILE.read_text())
    theme_json = render_theme_document(source)
    current_readme = README_FILE.read_text()
    next_readme = update_readme(current_readme, render_readme_palettes(source))

    theme_doc = json.loads(theme_json)
    errors = []
    for theme in theme_doc["themes"]:
        errors.extend(validate_theme(theme))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    if args.check:
        stale = []
        if not THEME_FILE.exists() or THEME_FILE.read_text() != theme_json:
            stale.append(str(THEME_FILE.relative_to(ROOT)))
        if next_readme != current_readme:
            stale.append(str(README_FILE.relative_to(ROOT)))
        if stale:
            print("Generated files are stale:", ", ".join(stale), file=sys.stderr)
            return 1
        return 0

    THEME_FILE.write_text(theme_json)
    README_FILE.write_text(next_readme)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
