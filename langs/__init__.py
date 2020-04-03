"""
langs - tools for managing l10n strings
Copyright (C) 2020 Cezar H. <https://github.com/usernein>

This file is part of langs.

langs is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

langs is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with langs.  If not, see <https://www.gnu.org/licenses/>.
"""
import html
import re

__version__ = "0.0.3"

class LangsFormatMap(dict):
    def __missing__(self, key):
        return '{'+key+'}'

class LangString(str):
    def __call__(self, **kwargs):
        try:
            result = self
        except:
            result = key
        
        if self.escape_html:
            kwargs = map(
                lambda item: (item[0],html.escape(item[1])),
                kwargs.items()
            )
            kwargs = dict(kwargs)
        return result.format_map(LangsFormatMap(**kwargs))
        
class Langs:
    def __init__(self, strings={}, escape_html=False, **kwargs):
        self.strings = strings
        self.escape_html = escape_html
        
        if not kwargs and not strings:
            raise ValueError('Pass the languages and the path to their JSON files as keyword arguments (language=path)')

        for language_code,strings_object in kwargs.items():
            self.strings[language_code] = strings_object
            self.strings[language_code].update({'language_code': language_code})
        
        #self.strings = {'en':{'start':'Hi {name}!'}}
        self.languages = list(self.strings.keys())
        self.language = 'en' if 'en' in self.languages else self.languages[0]
        
    def __getattr__(self, key):
        try:
            result = self.strings[self.language][key]
        except:
            result = key
        obj = LangString(result)
        obj.escape_html=self.escape_html
        return obj
    
    def getLanguage(self, language_code):
        clean_lang_code = re.sub('[^a-z]', '', (language_code or '').lower())
        if not clean_lang_code:
            raise ValueError('Invalid language_code')
            
        lang_copy = Langs(strings=self.strings, escape_html=self.escape_html)
        if clean_lang_code in lang_copy.languages:
            lang_copy.language = clean_lang_code
        return lang_copy
