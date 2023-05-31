from bs4 import BeautifulSoup
from glob import glob
import regex as re
import unicodedata

substitution_yue = (
    ('!', '！'),
    (',', '，'),
    (':', '：'),
    ('?', '？'),
    ('啝', '喎'),
    ('噖', '琴'),  # 噖[日晚] -> 琴[日晚]
    ('嚫', '親'),
    ('床', '牀'),
    ('杧', '芒'),
    ('著', '着'),  # 著 zyu3 as in 著作, does not exist in the corpus
    ('衭', '褲'),
    ('贃', '賺'),
    ('𠵉', '行'),
    ('𠶧', '掂'),
    ('𠸐', '禁'),
    ('𠹳', '杰'),
    ('𠹺', '埋'),
    ('𠻗', '呢'),
    ('𡁵', '緊'),
    ('𡃶', '錫'),
    ('𡄯', '噎'),
    ('𧨾', '氹'),
    ('𧵳', '蝕'),
    ('依𠺢', '依家'),
    ('橋​𠮩', '𠵇𠺫'),
    ('爹啲', '爹哋'),
    ('而𠺢', '而家'),
    ('𠺢吓', '家下'),
    ('𠺢陣', '家陣'),
    ('你 吖', '你吖'),
    ('喺 個', '喺個'),
    ('我 諗', '我諗'),
    ('星架波', '新加坡'),
    ('自覺得己', '覺得自己'),
    ('右冇畀返我', '又冇畀返我'),
)

_pattern_lower = re.compile(
    r'(?<![a-zA-Z])('
    'ARTS|'
    'BAND|'
    'BIO|'
    'CAMP|'
    'CANCER|'
    'CHEAP|'
    'CIVIL|'
    'COMPUTER|'
    'CREAM|'
    'FACIAL|'
    'FIT|'
    'FRIEND|'
    'GAG|'
    'HAPPY|'
    'KEEP|'
    'KEY|'
    'LAW|'
    'LIKE|'
    'MOVIE|'
    'OUT|'
    'PACK|'
    'QUALI|'
    'ROUND|'
    'SALES|'
    'SEMINAR|'
    'SEM|'
    'SHARP|'
    'SHOPPING|'
    'SHORT|'
    'TITLE|'
    'TUTORIAL|'
    'WINNER'
    r')(?![a-zA-Z])'
)
def upper_to_lower(s: str) -> str:
    return _pattern_lower.sub(lambda match: match.group(0).lower(), s)

_fw = 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０'
_hw = unicodedata.normalize('NFKC', _fw)
_trans = str.maketrans(_fw, _hw)
def full_width_to_half_width(s: str) -> str:
    return s.translate(_trans)

def remove_space(s: str) -> str:
    '''
    >>> remove_space('摸 A B 12至 3')
    '摸A B 12至3'
    >>> remove_space('噉你哋要唔要呢 ？')
    '噉你哋要唔要呢？'
    '''
    s = re.sub(r'(?<=[\p{Unified_Ideograph}\u3006\u3007]) (?=[\da-zA-Z！，：？《》])', r'', s)
    s = re.sub(r'(?<=[\da-zA-Z！，：？《》]) (?=[\p{Unified_Ideograph}\u3006\u3007])', r'', s)
    return s

_pattern_han = re.compile(r'[\p{Unified_Ideograph}\u3006\u3007]')
def is_han(c: str) -> str:
    return bool(_pattern_han.fullmatch(c))

_pattern_letter = re.compile(r'[a-zA-Z]')
def is_letter(c: str) -> str:
    return bool(_pattern_letter.fullmatch(c))

def normalise(yue: str, en: str) -> tuple[str, str]:
    for src, dst in substitution_yue:
        yue = yue.replace(src, dst)
    yue = yue.strip()
    en = en.strip()
    yue = upper_to_lower(yue)
    yue = full_width_to_half_width(yue)
    yue = remove_space(yue)
    if en[-1] == '!' and (is_han(yue[-1]) or is_letter(yue[-1])):
        yue += '！'
    if en[-1] == '?' and (is_han(yue[-1]) or is_letter(yue[-1])):
        yue += '？'
    if (is_han(yue[-1]) or is_letter(yue[-1])) and is_letter(en[-1]):
        if (4 <= len(yue) < 6 and yue[0] in '我你佢') or len(yue) >= 6:  # 一定係陳述句
            yue += '。'
            en += '.'
    if len(yue) < 4 and '，' not in yue and ',' in en:
        en = en.split(',', 1)[0]  # remove explanatory words
    return yue, en

pattern_pua = re.compile(r'[\ue000-\uf8ff\U000f0000-\U000ffffd\U00100000-\U0010fffd]')
def contains_pua(s: str) -> str:
    return bool(pattern_pua.search(s))

def is_paren_balanced(yue: str, en: str) -> bool:
    a = yue.count('（')
    b = yue.count('）')
    c = en.count('(')
    d = en.count(')')
    return a == b == c == d

def is_colon_balanced(yue: str, en: str) -> bool:
    a = yue.count('；')
    b = en.count(';')
    return a == b

def should_remove(yue: str, en: str) -> bool:
    bad_texts = ('(empty band???)', '[missing example characters???]')
    should_remove_list = ("She's not here, lit. Not even her shadow is seen",)
    return yue in bad_texts or \
        en in bad_texts or \
        en in should_remove_list or \
        contains_pua(yue) or \
        not is_paren_balanced(yue, en) or \
        not is_colon_balanced(yue, en) or \
        'i.e.' in en

filename = glob('Wenlin+Dictionaries-*.xml')[-1]

def main():
    with open(filename, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    pattern_data = re.compile(r'^[^ ]*hz +(.+)\n[^ ]*tr +(.+)', flags=re.MULTILINE)
    sentences = set()

    for page in soup.select('page'):
        content = page.select_one('text').get_text().removeprefix('<WL>').removesuffix('</WL>')

        for match in pattern_data.finditer(content):
            yue, en = match.groups((1, 2))
            if should_remove(yue, en):
                continue
            assert '\n' not in yue
            assert '\n' not in en
            yue, en = normalise(yue, en)
            sentences.add((yue, en))

    def key(item):
        yue, en = item
        return len(yue), yue, en
    sentences = sorted(sentences, key=key)

    with open('yue.txt', 'w', encoding='utf-8') as f1, \
            open('en.txt', 'w', encoding='utf-8') as f2:
        for yue, en in sentences:
            print(yue, file=f1)
            print(en, file=f2)

main()
