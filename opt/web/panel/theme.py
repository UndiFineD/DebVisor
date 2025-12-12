# !/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


"""
Theme management for DebVisor Web Panel.

Features:
- Light and dark themes
- Custom color schemes
- CSS variable system
- User preference persistence
- System preference detection
- Theme switching

Supports customization of:
- Primary and secondary colors
- Font sizes and families
- Border radius and spacing
- Component styles
"""

import logging
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ThemeMode(Enum):
    """Theme modes."""

    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


@dataclass
class ColorPalette:
    """Color palette for theme."""

    primary: str = "    #2196F3"
    secondary: str = "    #FFC107"
    success: str = "    #4CAF50"
    warning: str = "    #FFC107"
    error: str = "    #F44336"
    info: str = "    #00BCD4"

    background: str = "    #FFFFFF"
    background_secondary: str = "    #F5F5F5"
    background_tertiary: str = "    #EEEEEE"

    text_primary: str = "    #212121"
    text_secondary: str = "    #757575"
    text_disabled: str = "    #BDBDBD"

    border: str = "    #E0E0E0"
    divider: str = "    #BDBDBD"

    shadow_light: str = "rgba(0, 0, 0, 0.05)"
    shadow_medium: str = "rgba(0, 0, 0, 0.1)"
    shadow_dark: str = "rgba(0, 0, 0, 0.2)"

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return asdict(self)

    def to_css_variables(self) -> str:
        """Generate CSS variables."""
        css = ":root {\n"
        for name, color in self.to_dict().items():
            css_var_name = "--color-" + name.replace("_", "-")
            css += f"  {css_var_name}: {color};\n"
        css += "}\n"
        return css


@dataclass
class Typography:
    """Typography settings."""

    font_family: str = (
        "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    )
    font_size_base: int = 14
    font_size_small: int = 12
    font_size_large: int = 16
    font_size_xlarge: int = 20

    line_height_base: float = 1.5
    line_height_tight: float = 1.2
    line_height_loose: float = 1.8

    font_weight_light: int = 300
    font_weight_normal: int = 400
    font_weight_medium: int = 500
    font_weight_bold: int = 700

    def to_css_variables(self) -> str:
        """Generate CSS variables."""
        css = ":root {\n"
        css += f"  --font-family: {self.font_family};\n"
        css += f"  --font-size-base: {self.font_size_base}px;\n"
        css += f"  --font-size-small: {self.font_size_small}px;\n"
        css += f"  --font-size-large: {self.font_size_large}px;\n"
        css += f"  --font-size-xlarge: {self.font_size_xlarge}px;\n"
        css += f"  --line-height-base: {self.line_height_base};\n"
        css += f"  --line-height-tight: {self.line_height_tight};\n"
        css += f"  --line-height-loose: {self.line_height_loose};\n"
        css += f"  --font-weight-light: {self.font_weight_light};\n"
        css += f"  --font-weight-normal: {self.font_weight_normal};\n"
        css += f"  --font-weight-medium: {self.font_weight_medium};\n"
        css += f"  --font-weight-bold: {self.font_weight_bold};\n"
        css += "}\n"
        return css


@dataclass
class Spacing:
    """Spacing and sizing."""

    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48

    border_radius_small: int = 2
    border_radius_medium: int = 4
    border_radius_large: int = 8
    border_radius_xlarge: int = 16

    def to_css_variables(self) -> str:
        """Generate CSS variables."""
        css = ":root {\n"
        css += f"  --spacing-xs: {self.xs}px;\n"
        css += f"  --spacing-sm: {self.sm}px;\n"
        css += f"  --spacing-md: {self.md}px;\n"
        css += f"  --spacing-lg: {self.lg}px;\n"
        css += f"  --spacing-xl: {self.xl}px;\n"
        css += f"  --spacing-xxl: {self.xxl}px;\n"
        css += f"  --border-radius-small: {self.border_radius_small}px;\n"
        css += f"  --border-radius-medium: {self.border_radius_medium}px;\n"
        css += f"  --border-radius-large: {self.border_radius_large}px;\n"
        css += f"  --border-radius-xlarge: {self.border_radius_xlarge}px;\n"
        css += "}\n"
        return css


@dataclass
class Shadow:
    """Shadow settings."""

    elevation_1: str = "0 2px 4px rgba(0, 0, 0, 0.1)"
    elevation_2: str = "0 4px 8px rgba(0, 0, 0, 0.12)"
    elevation_3: str = "0 8px 16px rgba(0, 0, 0, 0.15)"
    elevation_4: str = "0 16px 32px rgba(0, 0, 0, 0.2)"

    def to_css_variables(self) -> str:
        """Generate CSS variables."""
        css = ":root {\n"
        css += f"  --shadow-elevation-1: {self.elevation_1};\n"
        css += f"  --shadow-elevation-2: {self.elevation_2};\n"
        css += f"  --shadow-elevation-3: {self.elevation_3};\n"
        css += f"  --shadow-elevation-4: {self.elevation_4};\n"
        css += "}\n"
        return css


class Theme:
    """Theme definition."""

    def __init__(
        self,
        name: str,
        mode: ThemeMode,
        colors: Optional[ColorPalette] = None,
        typography: Optional[Typography] = None,
        spacing: Optional[Spacing] = None,
        shadow: Optional[Shadow] = None,
    ):
        """
        Initialize theme.

        Args:
            name: Theme name
            mode: Light or dark mode
            colors: Color palette
            typography: Typography settings
            spacing: Spacing settings
            shadow: Shadow settings
        """
        self.name = name
        self.mode = mode
        self.colors = colors or ColorPalette()
        self.typography = typography or Typography()
        self.spacing = spacing or Spacing()
        self.shadow = shadow or Shadow()

    def to_css(self) -> str:
        """Generate complete CSS for theme."""
        css = f"/* Theme: {self.name} ({self.mode.value}) */\n\n"
        css += self.colors.to_css_variables()
        css += self.typography.to_css_variables()
        css += self.spacing.to_css_variables()
        css += self.shadow.to_css_variables()

        # Add theme-specific styles
        css += self._get_component_styles()

        return css

    def _get_component_styles(self) -> str:
        """Get component-specific styles."""
        css = "\n/* Component Styles */\n"

        # Button styles
        css += """
button, .btn {
    background-color: var(--color-primary);
    color: white;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius-medium);
    border: none;
    cursor: pointer;
    font-family: var(--font-family);
    font-size: var(--font-size-base);
    transition: all 0.2s ease;
    box-shadow: var(--shadow-elevation-1);
}

button:hover, .btn:hover {
    box-shadow: var(--shadow-elevation-2);
    transform: translateY(-2px);
}

button:active, .btn:active {
    transform: translateY(0);
}

button:disabled, .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
"""

        # Card styles
        css += """
.card {
    background-color: var(--color-background);
    border-radius: var(--border-radius-large);
    padding: var(--spacing-md);
    box-shadow: var(--shadow-elevation-1);
    border: 1px solid var(--color-border);
}

.card:hover {
    box-shadow: var(--shadow-elevation-2);
}
"""

        # Input styles
        css += """
input, textarea, select {
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius-medium);
    padding: var(--spacing-sm) var(--spacing-md);
    font-family: var(--font-family);
    font-size: var(--font-size-base);
    color: var(--color-text-primary);
    transition: border-color 0.2s ease;
}

input:focus, textarea:focus, select:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
}
"""

        # Header/navbar styles
        css += """
.navbar, .header {
    background-color: var(--color-background-secondary);
    border-bottom: 1px solid var(--color-border);
    padding: var(--spacing-md);
    box-shadow: var(--shadow-elevation-1);
}
"""

        # Alert styles
        css += """
.alert {
    padding: var(--spacing-md);
    border-radius: var(--border-radius-medium);
    margin-bottom: var(--spacing-md);
}

.alert.alert-success {
    background-color: rgba(76, 175, 80, 0.1);
    border-left: 4px solid var(--color-success);
    color: var(--color-success);
}

.alert.alert-warning {
    background-color: rgba(255, 193, 7, 0.1);
    border-left: 4px solid var(--color-warning);
    color: var(--color-warning);
}

.alert.alert-error {
    background-color: rgba(244, 67, 54, 0.1);
    border-left: 4px solid var(--color-error);
    color: var(--color-error);
}

.alert.alert-info {
    background-color: rgba(0, 188, 212, 0.1);
    border-left: 4px solid var(--color-info);
    color: var(--color-info);
}
"""

        # Badge styles
        css += """
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: var(--border-radius-xlarge);
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-medium);
}

.badge-primary {
    background-color: var(--color-primary);
    color: white;
}

.badge-success {
    background-color: var(--color-success);
    color: white;
}

.badge-warning {
    background-color: var(--color-warning);
    color: white;
}

.badge-error {
    background-color: var(--color-error);
    color: white;
}
"""

        return css


class ThemeManager:
    """Manages themes and preferences."""

    def __init__(self) -> None:
        """Initialize theme manager."""
        self.themes: Dict[str, Theme] = {}
        self.current_theme: Optional[Theme] = None
        self.user_preference: ThemeMode = ThemeMode.AUTO

        # Register default themes
        self._register_default_themes()

    def _register_default_themes(self) -> None:
        """Register default light and dark themes."""
        # Light theme
        light_colors = ColorPalette(
            primary="    #2196F3",
            secondary="    #FFC107",
            background="    #FFFFFF",
            background_secondary="    #F5F5F5",
            text_primary="    #212121",
        )
        light_theme = Theme(
            name="Light",
            mode=ThemeMode.LIGHT,
            colors=light_colors,
        )
        self.register_theme(light_theme)

        # Dark theme
        dark_colors = ColorPalette(
            primary="    #1E88E5",
            secondary="    #FFB300",
            background="    #121212",
            background_secondary="    #1E1E1E",
            background_tertiary="    #2A2A2A",
            text_primary="    #E0E0E0",
            text_secondary="    #B0B0B0",
            border="    #424242",
            divider="    #616161",
        )
        dark_theme = Theme(
            name="Dark",
            mode=ThemeMode.DARK,
            colors=dark_colors,
        )
        self.register_theme(dark_theme)

        # Set light as default
        self.current_theme = light_theme

    def register_theme(self, theme: Theme) -> None:
        """
        Register a theme.

        Args:
            theme: Theme to register
        """
        self.themes[theme.name.lower()] = theme
        logger.info(f"Registered theme: {theme.name}")

    def set_theme(self, theme_name: str) -> bool:
        """
        Set current theme.

        Args:
            theme_name: Theme name

        Returns:
            True if successful
        """
        theme = self.themes.get(theme_name.lower())
        if theme is None:
            logger.error(f"Theme not found: {theme_name}")
            return False

        self.current_theme = theme
        logger.info(f"Set theme: {theme_name}")
        return True

    def set_preference(self, preference: ThemeMode) -> None:
        """
        Set user theme preference.

        Args:
            preference: Theme preference (light, dark, or auto)
        """
        self.user_preference = preference
        logger.info(f"Set theme preference: {preference.value}")

    def get_theme_css(self, theme_name: Optional[str] = None) -> str:
        """
        Get CSS for theme.

        Args:
            theme_name: Theme name (uses current if not specified)

        Returns:
            CSS string
        """
        if theme_name:
            theme = self.themes.get(theme_name.lower())
        else:
            theme = self.current_theme

        if theme is None:
            logger.error("No theme available")
            return ""

        return theme.to_css()

    def list_themes(self) -> List[str]:
        """
        List available themes.

        Returns:
            List of theme names
        """
        return list(self.themes.keys())

    def get_system_preference(self) -> ThemeMode:
        """
        Get system color scheme preference.

        Note: In a web context, this would come from CSS media query.
        In this implementation, we return AUTO to let the client decide.

        Returns:
            System preference
        """
        return ThemeMode.AUTO

    def get_effective_theme(self) -> Optional[Theme]:
        """
        Get effective theme based on user preference and system settings.

        Returns:
            Effective theme
        """
        if self.user_preference != ThemeMode.AUTO:
            return self.themes.get(self.user_preference.value, self.current_theme)

        # Auto mode - use system preference if available
        system_pref = self.get_system_preference()
        if system_pref != ThemeMode.AUTO:
            return self.themes.get(system_pref.value, self.current_theme)

        return self.current_theme

    def export_theme_config(self, theme_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Export theme configuration as dictionary.

        Args:
            theme_name: Theme name (uses current if not specified)

        Returns:
            Theme configuration dictionary
        """
        if theme_name:
            theme = self.themes.get(theme_name.lower())
        else:
            theme = self.current_theme

        if theme is None:
            return {}

        return {
            "name": theme.name,
            "mode": theme.mode.value,
            "colors": theme.colors.to_dict(),
            "available_themes": self.list_themes(),
            "user_preference": self.user_preference.value,
        }

    def create_custom_theme(
        self,
        name: str,
        mode: ThemeMode,
        colors_dict: Optional[Dict[str, str]] = None,
    ) -> Theme:
        """
        Create a custom theme.

        Args:
            name: Theme name
            mode: Theme mode
            colors_dict: Color palette dictionary

        Returns:
            Created theme
        """
        colors = ColorPalette()

        if colors_dict:
            for key, value in colors_dict.items():
                if hasattr(colors, key):
                    setattr(colors, key, value)

        theme = Theme(
            name=name,
            mode=mode,
            colors=colors,
        )

        self.register_theme(theme)
        return theme
