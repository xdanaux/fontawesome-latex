#!/usr/bin/env python3
# usage: generate_tex_bindings.py <VERSION>

import argparse
import sys
import subprocess
import re
import os, shutil
import fontforge

DEBUG=False;

numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'];

pdftex_replace = {
  "space"                 : ".notdef",             #0020 (blank)
  "dieresis"              : ".notdef",             #00a8 (blank)
  "copyright"             : ".notdef",             #00a9 (blank)
  "registered"            : ".notdef",             #00ae (blank)
  "acute"                 : ".notdef",             #00b4 (blank)
  "AE"                    : ".notdef",             #00c6 (blank)
  "Oslash"                : ".notdef",             #00d8 (blank)
  "trademark"             : ".notdef",             #2122 (blank)
  "infinity"              : ".notdef",             #221e (blank)
  "notequal"              : ".notdef",             #2260 (blank)
  "envelope"              : "envelope-o",          #f003
  "star_empty"            : "star-o",              #f006
  "ok"                    : "check",               #f00c
  "remove"                : "times",               #f00d
  "zoom_in"               : "search-plus",         #f00e
  "zoom_out"              : "search-minus",        #f010
  "off"                   : "power-off",           #f011
  "trash"                 : "trash-o",             #f014
  "file_alt"              : "file-o",              #f016
  "time"                  : "clock-o",             #f017
  "download_alt"          : "download",            #f019
  "download"              : "arrow-circle-o-down", #f01a
  "upload"                : "arrow-circle-o-up",   #f01b
  "play_circle"           : "play_circle_o",       #f01d
  "indent_left"           : "outdent",             #f03b
  "indent_right"          : "indent",              #f03c
  "facetime_video"        : "video-camera",        #f03d
  "picture"               : "picture-o",           #f03e
  "edit"                  : "pencil-square-o",     #f044
  "share"                 : "share-square-o",      #f045
  "check"                 : "check-square-o",      #f046
  "move"                  : "arrows",              #f047
  "plus_sign"             : "plus-circle",         #f055
  "minus_sign"            : "minus-circle",        #f056
  "remove_sign"           : "times-circle",        #f057
  "ok_sign"               : "check-circle",        #f058
  "question_sign"         : "question-circle",     #f059
  "info_sign"             : "info-circle",         #f05a
  "screenshot"            : "crosshairs",          #f05b
  "remove_circle"         : "times-circle-o",      #f05c
  "ok_circle"             : "check-circle-o",      #f05d
  "ban_circle"            : "ban",                 #f05e
  "share_alt"             : "share",               #f064
  "resize_full"           : "expand",              #f065
  "resize_small"          : "compress",            #f066
  "exclamation_sign"      : "exclamation-circle",  #f06a
  "eye_open"              : "eye",                 #f06e
  "eye_close"             : "eye-slash",           #f070
  "warning_sign"          : "exclamation-triangle",#f071
  "folder_close"          : "folder",              #f07b
  "resize_horizontal"     : "arrows-h",            #f07d
  "resize_vertical"       : "arrows-v",            #f07e
  "twitter_sign"          : "twitter-square",      #f081
  "facebook_sign"         : "facebook-square",     #f082
  "thumbs_up_alt"         : "thumbs-o-up",         #f087
  "thumbs_down_alt"       : "thumbs-o-down",       #f088
  "heart_empty"           : "heart-o",             #f08a
  "signout"               : "sign-out",            #f08b
  "linkedin_sign"         : "linkedin-square",     #f08c
  "pushpin"               : "thumb-tack",          #f08d
  "signin"                : "sign-in",             #f090
  "github_sign"           : "github-square",       #f092
  "upload_alt"            : "upload",              #f093
  "lemon"                 : "lemon-o",             #f094
  "check_empty"           : "square-o",            #f096
  "bookmark_empty"        : "bookmark-o",          #f097
  "phone_sign"            : "phone-square",        #f098
  "hdd"                   : "hdd-o",               #f0a0
  "bell"                  : "bell-o",              #f0a2
  "hand_right"            : "hand-o-right",        #f0a4
  "hand_left"             : "hand-o-left",         #f0a5
  "hand_up"               : "hand-o-up",           #f0a6
  "hand_down"             : "hand-o-down",         #f0a7
  "circle_arrow_left"     : "arrow-circle-left",   #f0a8
  "circle_arrow_right"    : "arrow-circle-right",  #f0a9
  "circle_arrow_up"       : "arrow-circle-up",     #f0aa
  "circle_arrow_down"     : "arrow-circle-down",   #f0ab
  "fullscreen"            : "arrows-alt",          #f0b2
  "group"                 : "users",               #f0c0
  "beaker"                : "flask",               #f0c3
  "cut"                   : "scissors",            #f0c4
  "copy"                  : "files-o",             #f0c5
  "paper_clip"            : "paperclip",           #f0c6
  "save"                  : "floppy-o",            #f0c7
  "sign_blank"            : "square",              #f0c8
  "reorder"               : "bars",                #f0c9
  "ul"                    : "list-ul",             #f0ca
  "ol"                    : "list-ol",             #f0cb
  "pinterest_sign"        : "pinterest-square",    #f0d3
  "google_plus_sign"      : "google-plus-square",  #f0d4
  "sort_down"             : "sort-desc",           #f0dd
  "sort_up"               : "sort-asc",            #f0de
  "envelope_alt"          : "envelope",            #f0e0
  "legal"                 : "gavel",               #f0e3
  "dashboard"             : "tachometer",          #f0e4
  "comment_alt"           : "comment-o",           #f0e5
  "comments_alt"          : "comments-o",          #f0e6
  "paste"                 : "clipboard",           #f0ea
  "light_bulb"            : "lightbulb-o",         #f0eb
  "bell_alt"              : "bell",                #f0f3
  "food"                  : "cutlery",             #f0f5
  "file_text_alt"         : "file-text-o",         #f0f6
  "building"              : "building-o",          #f0f7
  "hospital"              : "hospital-o",          #f0f8
  "h_sign"                : "h-square",            #f0fd
  "f0fe"                  : "plus-square",         #f0fe
  "double_angle_left"     : "angle-double-left",   #f100
  "double_angle_right"    : "angle-double-right",  #f101
  "double_angle_up"       : "angle-double-up",     #f102
  "double_angle_down"     : "angle-double-down",   #f103
  "mobile_phone"          : "mobile",              #f10b
  "circle_blank"          : "circle-o",            #f10c
  "folder_close_alt"      : "folder-o",            #f114
  "folder_open_alt"       : "folder-open-o",       #f115
  "expand_alt"            : ".notdef",             #f116 (blank)
  "collapse_alt"          : ".notdef",             #f117 (blank)
  "smile"                 : "smile-o",             #f118
  "frown"                 : "frown-o",             #f119
  "meh"                   : "meh-o",               #f11a
  "keyboard"              : "keyboard-o",          #f11c
  "flag_alt"              : "flag-o",              #f11d
  "star_half_empty"       : "star-half-o",         #f123
  "unlink"                : "chain-broken",        #f127
  "_279"                  : "info",                #f129
  "_283"                  : "eraser",              #f12d
  "microphone_off"        : "microphone-slash",    #f131
  "calendar_empty"        : "calendar-o",          #f133
  "chevron_sign_left"     : "chevron-circle-left", #f137
  "chevron_sign_right"    : "chevron-circle-right",#f138
  "chevron_sign_up"       : "chevron-circle-up",   #f139
  "chevron_sign_down"     : "chevron-circle-down", #f13a
  "ellipsis_horizontal"   : "ellipsis-h",          #f141
  "ellipsis_vertical"     : "ellipsis-v",          #f142
  "_303"                  : "rss-square",          #f143
  "play_sign"             : "play-circle",         #f144
  "minus_sign_alt"        : "minus-square",        #f146
  "check_minus"           : "minus-square-o",      #f147
  "check_sign"            : "check-square",        #f14a
  "edit_sign"             : "pencil-square",       #f14b
  "_312"                  : "external-link-square",#f14c
  "share_sign"            : "share-square",        #f14d
  "collapse"              : "caret-square-o-down", #f150
  "collapse_top"          : "caret-square-o-up",   #f151
  "_317"                  : "caret-square-o-right",#f152
  "sort_by_alphabet"      : "sort-alpha-asc",      #f15d
  "_329"                  : "sort-alpha-desc",     #f15e
  "sort_by_attributes"    : "sort-amount-asc",     #f160
  "sort_by_attributes_alt": "sort-amount-desc",    #f161
  "sort_by_order"         : "sort-numeric-asc",    #f162
  "sort_by_order_alt"     : "sort-numeric-desc",   #f163
  "_334"                  : "thumbs-up",           #f164
  "_335"                  : "thumbs-down",         #f165
  "youtube_sign"          : "youtube-square",      #f166
  "xing_sign"             : "xing-square",         #f169
  "stackexchange"         : "stack-overflow",      #f16c
  "f171"                  : "bitbucket",           #f171
  "bitbucket_sign"        : "bitbucket-square",    #f172
  "tumblr_sign"           : "tumblr-square",       #f174
  "dribble"               : "dribbble",            #f17d
  "gittip"                : "gratipay",            #f184
  "sun"                   : "sun-o",               #f185
  "_366"                  : "moon-o",              #f186
  "_372"                  : "pagelines",
  "_374"                  : "arrow-circle-o-right",#f18e
  "arrow_circle_alt_left" : "arrow-circle-o-left", #f190
  "_376"                  : "caret-square-o-left", #f191
  "dot_circle_alt"        : "dot-circle-o",        #f192
  "_378"                  : "wheelchair",
  "_380"                  : "try",
  "_382"                  : "space-shuttle",
  "_383"                  : "slack",
  "_384"                  : "envelope-square",
  "_385"                  : "wordpress",
  "_386"                  : "openid",
  "_387"                  : "university",
  "_388"                  : "graduation-cap",
  "_389"                  : "yahoo",
  "uniF1A0"               : "google",              #f1a0
  "f1a1"                  : "reddit",
  "_392"                  : "reddit-square",
  "_393"                  : "stumbleupon-circle",
  "f1a4"                  : "stumbleupon",
  "_395"                  : "delicious",
  "_396"                  : "digg",
  "_397"                  : "pied-piper",
  "_398"                  : "pied-piper-alt",
  "_399"                  : "drupal",
  "_400"                  : "joomla",
  "f1ab"                  : "language",            #f1ab
  "_402"                  : "fax",
  "_403"                  : "building",
  "_404"                  : "child",               #f1ae
  "uniF1B1"               : "paw",                 #f1b0
  "_406"                  : "spoon",               #f1b1
  "_407"                  : "cube",                #f1b2
  "_408"                  : "cubes",               #f1b3
  "_409"                  : "behance",             #f1b4
  "_410"                  : "behance-square",
  "_411"                  : "steam",
  "_412"                  : "steam-square",
  "_413"                  : "recycle",
  "_414"                  : "car",
  "_415"                  : "taxi",
  "_416"                  : "tree",
  "_417"                  : "spotify",
  "_418"                  : "deviantart",
  "_419"                  : "soundcloud",
  "uniF1C0"               : "database",            #f1c0
  "uniF1C1"               : "file-pdf-o",          #f1c1
  "_422"                  : "file-word-o",
  "_423"                  : "file-excel-o",
  "_424"                  : "file-powerpoint-o",
  "_425"                  : "file-image-o",
  "_426"                  : "file-archive-o",
  "_427"                  : "file-audio-o",
  "_428"                  : "file-video-o",
  "_429"                  : "file-code-o",
  "_430"                  : "vine",
  "_431"                  : "codepen",
  "_432"                  : "jsfiddle",
  "_433"                  : "life-ring",
  "_434"                  : "circle-o-notch",
  "uniF1D0"               : "rebel",
  "uniF1D1"               : "empire",
  "uniF1D2"               : "git-square",
  "_438"                  : "git",
  "_439"                  : "hacker-news",
  "uniF1D5"               : "tencent-weibo",
  "uniF1D6"               : "qq",
  "uniF1D7"               : "weixin",              #f1d7
  "_443"                  : "paper-plane",
  "_444"                  : "paper-plane-o",
  "_445"                  : "history",             #f1da
  "_446"                  : "circle-thin",
  "_447"                  : "header",              #f1dc
  "_448"                  : "paragraph",
  "_449"                  : "sliders",
  "uniF1E0"               : "share-alt",
  "_451"                  : "share-alt-square",
  "_452"                  : "bomb",
  "_453"                  : "futbol-o",
  "_454"                  : "tty",
  "_455"                  : "binoculars",          #f1e5
  "_456"                  : "plug",
  "_457"                  : "slideshare",
  "_458"                  : "twitch",              #f1e8
  "_459"                  : "yelp",                #f1e9
  "_460"                  : "newspaper-o",         #f1ea
  "_461"                  : "wifi",
  "_462"                  : "calculator",
  "_463"                  : "paypal",
  "_464"                  : "google-wallet",
  "uniF1F0"               : "cc-visa",
  "_466"                  : "cc-mastercard",
  "_467"                  : "cc-discover",
  "f1f3"                  : "cc-amex",
  "_469"                  : "cc-paypal",
  "_470"                  : "cc-stripe",
  "_471"                  : "bell-slash",
  "_472"                  : "bell-slash-o",
  "_473"                  : "trash",
  "_474"                  : "copyright",
  "_475"                  : "at",
  "_476"                  : "eyedropper",          #f1fb
  "f1fc"                  : "paint-brush",
  "_478"                  : "birthday-cake",
  "_479"                  : "area-chart",
  "_480"                  : "pie-chart",
  "_481"                  : "line-chart",
  "_482"                  : "lastfm",
  "_483"                  : "lastfm-square",
  "_484"                  : "toggle-off",
  "_485"                  : "toggle-on",
  "_486"                  : "bicycle",
  "_487"                  : "bus",
  "_488"                  : "ioxhost",
  "_489"                  : "angellist",
  "_490"                  : "cc",
  "_491"                  : "ils",                 #f20b
  "_492"                  : "meanpath",
  "_493"                  : "buysellads",
  "_494"                  : "connectdevelop",
  "f210"                  : "dashcube",
  "_496"                  : "forumbee",
  "f212"                  : "leanpub",
  "_498"                  : "sellsy",
  "_499"                  : "shirtsinbulk",
  "_500"                  : "simplybuilt",
  "_501"                  : "skyatlas",
  "_502"                  : "cart-plus",
  "_503"                  : "cart-arrow-down",
  "_504"                  : "diamond",
  "_505"                  : "ship",
  "_506"                  : "user-secret",
  "_507"                  : "motorcycle",
  "_508"                  : "street-view",
  "_509"                  : "heartbeat",
  "_511"                  : "mars",
  "_512"                  : "mercury",
  "_513"                  : "transgender",
  "_514"                  : "transgender-alt",
  "_515"                  : "venus-double",
  "_516"                  : "mars-double",
  "_517"                  : "venus-mars",
  "_518"                  : "mars-stroke",
  "_519"                  : "mars-stroke-v",
  "_520"                  : "mars-stroke-h",
  "_521"                  : "neuter",
  "_522"                  : ".notdef",             #f22d (blank)
  "_523"                  : ".notdef",             #f22e (blank)
  "_524"                  : ".notdef",             #f22f (blank)
  "_525"                  : "facebook-official",
  "_526"                  : "pinterest-p",
  "_527"                  : "whatsapp",
  "_528"                  : "server",
  "_529"                  : "user-plus",
  "_530"                  : "user-times",
  "_531"                  : "bed",
  "_532"                  : "viacoin",
  "_533"                  : "train",
  "_534"                  : "subway",
  "_535"                  : "medium",
  "_536"                  : ".notdef",             #f23b (blank)
  "_537"                  : ".notdef",             #f23c (blank)
  "_538"                  : ".notdef",             #f23d (blank)
  "_539"                  : ".notdef",             #f23e (blank)
  "lessequal"             : ".notdef",             #f500 (blank)
}


# command line arguments handling
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Generate TeX bindings for the FontAwesome font by Dave Gandy.');
parser.add_argument('version', help='FontAwesome version, such as "4.3.0"')
args = parser.parse_args();
VERSION = args.version;
FONT = 'FontAwesome.otf';
CSS = 'FontAwesome.css';

# download the font (.otf and .css) from fontawesome.io
# ------------------------------------------------------------------------------
if os.path.isfile(FONT) and subprocess.check_output(['otfinfo', '-v', FONT], universal_newlines=True).split()[1] == VERSION:
  print("Font already present");
else:
  # download the otf font and css
  print("Downloading the font and css...", end="");
  try:
    ZIP = "font-awesome-{}.zip".format(VERSION);
    subprocess.call(['curl', '-s', '-f', '-LOk', "http://fontawesome.io/assets/" + ZIP]);
    subprocess.call(['unzip', '-q', ZIP]);
    os.rename("font-awesome-{}/fonts/FontAwesome.otf".format(VERSION), FONT)
    os.rename("font-awesome-{}/css/font-awesome.css".format(VERSION), CSS)
    subprocess.call(['rm', '-R', ZIP, "font-awesome-{}/".format(VERSION)]);
  except:
    sys.exit("[Error] Can't download and extract the font: {}".format(sys.exc_info()[1]))
  print(" done");
  # convert the otf font to 1000 UPM to prevent a bug in xdvipdfmx causing bad
  # (cfr http://tex.stackexchange.com/questions/134121/fontawesome-icons-are-getting-too-big-using-xelatex)
  print("Converting the font to 1000 upm...", end="");
  font = fontforge.open(FONT);
  font.em = 1000;
  font.generate("FontAwesome-1000upm.otf");
  os.rename("FontAwesome-1000upm.otf", FONT);
  print(" done");

# ==============================================================================
# generic
# ==============================================================================
# parse the css to get the associated symbols numbers of each glyph
# ------------------------------------------------------------------------------
print("Identifying glyphs from css...", end="");
css_file = open(CSS, 'r');
css = css_file.read();
css_file.close();
# identify independent icons (icon styles were named icon-* in version 3.1.0, fa-* in version 4.3.0
pattern = re.compile(r"\.(icon|fa)-([a-z1-9-]+):before\s*\{\s*content:\s*\"(\\[0-9a-fA-F]{4,4})\";?\s*\}", re.MULTILINE);
glyphs = [ (glyph_name, glyph_symbol) for (icon_or_fa, glyph_name, glyph_symbol) in re.findall(pattern, css)];
# identify aliases
pattern = re.compile(r"(?=\.(icon|fa)-([a-z1-9-]+):before,\s*\.(icon|fa)-([a-z1-9-]+):before\s*[,{])", re.MULTILINE);
aliases = dict([ (glyph_alias, glyph_name) for (icon_or_fa1, glyph_alias, icon_or_fa2, glyph_name) in re.findall(pattern, css)]);
del(css);
# recurse through indirect aliases
def recurse_dictionary (dictionary, key):
  if key in dictionary:
    return recurse_dictionary(dictionary, dictionary[key]) if dictionary[key] in dictionary else dictionary[key];
  else:
    return None;
for key in aliases:
  aliases[key] = recurse_dictionary(aliases, key);
print(" done ({} unique glyphs, {} aliases)".format(len(glyphs), len(aliases)));
if DEBUG:
  print("  Aliases:");
  for key in sorted(aliases):
    print("    {} => {}".format(key, aliases[key]));

# generate the style file
# ------------------------------------------------------------------------------
print("Generating the generic symbol list...", end="");
symbols = open('fontawesomesymbols-generic.tex', 'w');
for glyph_name, glyph_symbol in glyphs:
  glyph_name = aliases.get(glyph_name, glyph_name); # in case the glyph is named after an alias in the otf file
  symbols.write("\\def\\fa{}{{\\faicon{{{}}}}}\n".format(glyph_name.replace('-',' ').title().replace(' ',''), glyph_name));
symbols.write("% aliases\n");
for alias in aliases:
  symbols.write("\\def\\fa{}{{\\faicon{{{}}}}}\\expandafter\\def\\csname faicon@{}\\endcsname{{\\faicon{{{}}}}}\n".format(alias.replace('-',' ').title().replace(' ',''), alias, alias, aliases[alias]));
symbols.close();
print(" done");


# ==============================================================================
# xe- and luatex
# ==============================================================================
# generate the tex symbols list file
# ------------------------------------------------------------------------------
print("Generating the xe-/luatex symbol list...", end="");
symbols = open('fontawesomesymbols-xeluatex.tex', 'w');
for glyph_name, glyph_symbol in glyphs:
  glyph_name = aliases.get(glyph_name, glyph_name); # in case the glyph is named after an alias in the otf file
#  print(str(glyph_name) + ": " + str(glyph_symbol)); # debug
  symbols.write("\\expandafter\\def\\csname faicon@{}\\endcsname{{{{\\FA\\symbol{{{}}}}}}}\n".format(glyph_name, glyph_symbol.replace('\\','"').upper()));
symbols.close();
print(" done");


# ==============================================================================
# pdftex
# ==============================================================================
# use otfinfo to get the list of glyph names in the font
# ------------------------------------------------------------------------------
print("Generating the pdftex symbol list...", end="");
try:
  glyphs_names = subprocess.check_output(['otfinfo', '-g', FONT], universal_newlines=True).strip().split();
  glyphs_names = sorted([x for x in glyphs_names if x != '.notdef' and pdftex_replace.get(x) != '.notdef']);
except:
  sys.exit("\n[Error] Can't run otfinfo: {}".format(sys.exc_info()[1]))

# check that the pdftex glyph set is the same as the xe-/luatex one
pdftex_glyphs_names = [pdftex_replace.get(glyph_name, glyph_name).replace('_', '-') for glyph_name in glyphs_names];
diff1 = set(dict(glyphs).keys()).difference(set(pdftex_glyphs_names)); # or use symmetric_difference()
diff2 = set(pdftex_glyphs_names).difference(set(dict(glyphs).keys()));
if diff1 or diff2:
#  sys.exit("\n[Issue] xe-/luatex and pdftex glyphs do not match:\n  Missing from pdftex glyphs ({}): {}\n  Missing from xe-/luatex glyphs ({}): {}".format(len(diff1), sorted(diff1), len(diff2), sorted(diff2)));
  print("\n[Issue] xe-/luatex and pdftex glyphs do not match");
  print("  Missing from pdftex glyphs ({}):".format(len(diff1)));
  if DEBUG:
    for missing in sorted(diff1):
      print("    {}".format(missing));
  print("  Missing from xe-/luatex glyphs ({}):".format(len(diff2)));
  if DEBUG:
    for missing in sorted(diff2):
      print("    {}".format(missing));    


# write the required number of enc files, each with up to 256 glyphs
# ------------------------------------------------------------------------------
encfile_count = 0;
for glyph_count, glyph_name in enumerate(glyphs_names):
  # open a new enc file if required
  if glyph_count % 256 == 0:
    if encfile_count > 0:
      encfile.write("] def\n");
      encfile.close();
    encfile_count += 1;
    encfile = open("fontawesome{}.enc".format(numbers[encfile_count]), 'w');
    encfile.write("/fontawesome{} [\n".format(numbers[encfile_count]));
  # write the glyph
  encfile.write("/{}\n".format(glyph_name));
#  print("{}-{}: {}".format(encfile_count, glyph_count, glyph_name)); # debug

# fill the last enc file up to 256 characters
while glyph_count + 1 < encfile_count * 256:
  encfile.write("/.notdef\n");
  glyph_count += 1;

# close the last enc file
encfile.write("] def\n");
encfile.close();

# generate the t1 fonts (tfm,pfb)
# ------------------------------------------------------------------------------
# ensure texmf tree structure
TFM = "./"; #"texmf/fonts/tfm/public/fontawesome"
ENC = "./"; #"texmf/fonts/enc/pdftex/public/fontawesome"
T1  = "./"; #"texmf/fonts/type1/public/fontawesome"
OTF = "./"; #"texmf/fonts/opentype/public/fontawesome"

for path in [TFM, ENC, T1, OTF]:
  os.makedirs(path, exist_ok=True);

# generate the t1 files
maplines = [];
otftotfm_errors = open("otftotfm_errors.log", 'w');
for i in range(1, encfile_count+1):
  try:
    encfile_name = 'fontawesome{}.enc'.format(numbers[i]);
    command = ['otftotfm', FONT,
      '--literal-encoding=' + encfile_name,
      '--tfm-directory=' + TFM,
      '--encoding-directory=' + ENC,
      '--type1-directory=' + T1];
    mapline = subprocess.check_output(command, stderr=otftotfm_errors, universal_newlines=True).strip();
    maplines.append("\\pdfmapline{{+{}}}".format(mapline));
    maplines.append("\\font\\FA{}=FontAwesome--".format(numbers[i]) + encfile_name);
    os.rename(encfile_name, os.path.join(ENC, encfile_name));
    if OTF is not "./":
      shutil.copy(FONT, os.path.join(OTF, FONT));
  except:
    sys.exit("[Error] Can't run otftotfm: {}".format(sys.exc_info()[1]))
otftotfm_errors.close();

# write the maplines to the package file
with open('templates/fontawesome.sty.template', 'r') as template, open('fontawesome.sty', 'w') as sty:
  for line in template:
    if line == "% <maplines go here>\n":
      sty.write('\n'.join(maplines) + "\n");
    else:
      sty.write(line);
template.close();
sty.close();

# generate the tex symbols list file
# ------------------------------------------------------------------------------
symbols = open('fontawesomesymbols-pdftex.tex', 'w');
for glyph_count, glyph_name in enumerate(pdftex_glyphs_names):
  symbols.write("\\expandafter\\def\\csname faicon@{}\\endcsname{{{{\\FA{}\\symbol{{{}}}}}}}\n".format(glyph_name, numbers[glyph_count//256 +1], glyph_count % 256));
symbols.close();
print(" done");


# ==============================================================================
# documentation
# ==============================================================================
# generate the doc
# ------------------------------------------------------------------------------
print("Generating the documentation...", end="");
all_glyphs = sorted([(glyph, '') for glyph, symbol in glyphs] + [(alias, 'alias') for alias in aliases]);
with open('templates/fontawesome.tex.template', 'r') as template, open('fontawesome.tex', 'w') as doc:
  for line in template:
    if line == "% <showcaseicon commands go here>\n":
      for glyph, tag in all_glyphs:
        doc.write("  \\showcaseicon{{{}}}{{fa{}}}{{{}}}\n".format(glyph, glyph.replace('-',' ').title().replace(' ',''), tag));
    else:
      doc.write(line);
template.close();
doc.close();
print(" done");

