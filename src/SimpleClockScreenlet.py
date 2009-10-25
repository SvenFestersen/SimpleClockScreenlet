#!/usr/bin/env python
#
#       simpleClockScreenlet
#
#       Copyright 2009 Sven Festersen <sven@sven-festersen.de>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import datetime
import gtk
import gobject
import os
import screenlets
from screenlets.options import BoolOption
import sys
import time

import theme


class SimpleClockScreenlet(screenlets.Screenlet):
    """This Screenlet shows a simple clock."""

    __name__    = 'SimpleClockScreenlet'
    __version__ = 'Beta'
    __author__  = 'Sven Festersen'
    __desc__    = __doc__

    default_width = 250
    default_height = 75
    default_font_size = 50
    show_24_hours = True
    show_seconds = True
    _theme_info = None

    def __init__ (self, **keyword_args):
        screenlets.Screenlet.__init__(self, width=self.default_width, height=self.default_height, uses_theme=True, **keyword_args)
        self.theme_name = "BlackSquared"
        
        self.add_options_group("SimpleClock", "SimpleClock settings")
        
        opt_24 = BoolOption("SimpleClock", "show_24_hours", self.show_24_hours, "24 hours mode", "24 hours mode")
        self.add_option(opt_24)
        opt_sec = BoolOption("SimpleClock", "show_seconds", self.show_seconds, "Show seconds", "Show seconds")
        self.add_option(opt_sec)
    
    def on_init(self):
        self.add_default_menuitems()
        gobject.timeout_add(1000, self._update)
        
    def on_load_theme(self):
        self._theme_info = theme.ThemeInfo(self.theme.path + "/theme.conf")

    def on_draw(self, ctx):
        ctx.scale(self.scale, self.scale)

        format = "%I:%M"
        if self.show_24_hours:
            format = "%H:%M"
        if self.show_seconds:
            format += ":%S"
        
        self._theme_info.draw_background(ctx, self.default_width, self.default_height, self.scale)
        txt = time.strftime(format)
        ctx.set_font_size(self.default_font_size)
        ctx.set_source_rgba(*self._theme_info.foregroundColor)
        text_width = ctx.text_extents(txt)[2]
        text_height = ctx.text_extents(txt)[3]
        ctx.move_to((self.default_width - text_width) / 2, (self.default_height + text_height) / 2)
        ctx.show_text(txt)
        ctx.fill()
        
    def on_draw_shape (self, ctx):
        if self._theme_info:
            self.on_draw(ctx)
            
    def _update(self):
        self.window.queue_draw()
        return True

if __name__ == '__main__':
    import screenlets.session
    screenlets.session.create_session(SimpleClockScreenlet)
