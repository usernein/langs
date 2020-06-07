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

__version__ = "0.1.0"

class LangsFormatMap(dict):
    def __getitem__(self, key):
        if key in self:
            if type(self.get(key)) == str:
                return html.escape(self.get(key)) if self.escape_html else self.get(key)
            else:
                return self.get(key)
        else:
           return self.__missing__(key)
   
    def __missing__(self, key):
        if self.debug:
            print(f'Key "{key}" is missing on the string "{self.string}", language "{self.code}"')
        return '{'+key+'}'

class LangString(str):
    def __call__(self, **kwargs):
        try:
            result = self
        except:
            result = key
        
        mapping = LangsFormatMap(**kwargs)
        mapping.escape_html = self.escape_html
        mapping.string = self.key
        mapping.code = self.code
        mapping.debug = self.debug
        return result.format_map(mapping)
        
class Langs:
    strings = {}
    escape_html = False
    available = []
    code = 'en'
    
    def __init__(self, strings={}, escape_html=False, debug=True, **kwargs):
        self.strings = strings
        self.escape_html = escape_html
        
        if not kwargs and not strings:
            raise ValueError('Pass the languages and the path to their JSON files as keyword arguments (language=path)')

        for language_code,strings_object in kwargs.items():
            self.strings[language_code] = strings_object
            self.strings[language_code].update({'language_code': language_code})
        
        #self.strings = {'en':{'start':'Hi {name}!'}}
        self.available = list(self.strings.keys())
        self.code = 'en' if 'en' in self.available else self.available[0]
        self.debug = debug
    
    def __getattr__(self, key):
        try:
            result = self.strings[self.code][key]
        except:
            result = key
        obj = LangString(result)
        obj.escape_html=self.escape_html
        obj.key = key
        obj.code = self.code
        obj.debug = self.debug
        return obj
        
    def normalize_code(self, language_code):
        only_az = re.sub('[^a-z]', '', (language_code or ''))
        return only_az.lower()
        
    
    def get_language(self, language_code):
        clean_lang_code = self.normalize_code(language_code)
        if not clean_lang_code:
            raise ValueError('Invalid language_code')
            
        lang_copy = Langs(strings=self.strings, escape_html=self.escape_html)
        if clean_lang_code in lang_copy.available:
            lang_copy.code = clean_lang_code
        elif clean_lang_code[:2] in lang_copy.available:
            lang_copy.code = clean_lang_code[:2]
        return lang_copy
    
    def getLanguage(self, *args, **kwargs):
        print("Langs.getLanguage is deprecated and will be removed soon. Use Langs.get_language instead")
        return self.get_language(*args, **kwargs)