# sinjieo_converter_complete.py
# 신지어 ↔ 한국어 변환기 (최종 완전판)

# -------------------------
# 자음/모음 매핑
# -------------------------
consonant_to_code = {
    'ㄱ':'1', 'ㅋ':'1!', 'ㄲ':'1?', 'ㄴ':'2', 'ㄹ':'2!',
    'ㄷ':'3', 'ㅌ':'3!', 'ㄸ':'3?', 'ㅂ':'4', 'ㅍ':'4!',
    'ㅃ':'4?', 'ㅅ':'5', 'ㅎ':'5!', 'ㅆ':'5?', 'ㅈ':'6',
    'ㅊ':'6!', 'ㅉ':'6?', 'ㅇ':'7', 'ㅁ':'7!'
}

vowel_to_code = {
    'ㅏ':'a', 'ㅑ':'a^', 'ㅐ':'af', 'ㅒ':'a^f', 'ㅔ':'bf', 'ㅖ':'b^f',
    'ㅓ':'b', 'ㅕ':'b^', 'ㅗ':'c', 'ㅛ':'c^', 'ㅜ':'d', 'ㅠ':'d^',
    'ㅡ':'e', 'ㅣ':'f', 'ㅚ':'cf', 'ㅢ':'ef', 'ㅙ':'caf', 'ㅟ':'df',
    'ㅝ':'db', 'ㅞ':'dbf', 'ㅘ':'ca'
}

code_to_consonant = {v:k for k,v in consonant_to_code.items()}
code_to_vowel = {v:k for k,v in vowel_to_code.items()}

# -------------------------
# 합성 종성 매핑
# -------------------------
composite_jong_to_sinjieo = {
    'ㄳ':'15&', 'ㄵ':'26&', 'ㄶ':'25!&',
    'ㄺ':'12&', 'ㄻ':'27&', 'ㄼ':'24&', 'ㄽ':'25&',
    'ㄾ':'23!&', 'ㄿ':'24!&', 'ㅀ':'25!&', 'ㅄ':'45&'
}
sinjieo_to_composite_jong = {v:k for k,v in composite_jong_to_sinjieo.items()}

# -------------------------
# 한글 조합 리스트
# -------------------------
chosung_list = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
jungsung_list = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
jongsung_list = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

import re

# -------------------------
# 한글 → 신지어
# -------------------------
def decompose_hangul(char):
    if '가' <= char <= '힣':
        code = ord(char) - ord('가')
        jong = code % 28
        jung = ((code - jong)//28) % 21
        cho = ((code - jong)//28)//21
        return cho, jung, jong
    return None

def hangul_to_sinjieo(text):
    result = ''
    for char in text:
        if char == ' ':
            result += '/'
            continue
        decomposed = decompose_hangul(char)
        if decomposed:
            cho, jung, jong_idx = decomposed
            result += consonant_to_code[chosung_list[cho]]
            result += vowel_to_code[jungsung_list[jung]]
            jong_char = jongsung_list[jong_idx]
            if jong_char:
                if jong_char in composite_jong_to_sinjieo:
                    result += composite_jong_to_sinjieo[jong_char]
                else:
                    result += consonant_to_code[jong_char]
        else:
            result += char
    return result

# -------------------------
# 신지어 → 한글
# -------------------------
def sinjieo_to_hangul(code):
    result = ''
    i = 0
    while i < len(code):
        if code[i] == '/':
            result += ' '
            i += 1
            continue

        # 초성
        cho = None
        for k in sorted(code_to_consonant.keys(), key=lambda x:-len(x)):
            if code[i:i+len(k)] == k:
                cho = code_to_consonant[k]
                i += len(k)
                break
        if not cho:
            result += code[i]
            i += 1
            continue

        # 중성
        jung = None
        for k in sorted(code_to_vowel.keys(), key=lambda x:-len(x)):
            if code[i:i+len(k)] == k:
                jung = code_to_vowel[k]
                i += len(k)
                break
        if not jung:
            result += cho
            continue

        # 종성
        jong = ''
        matched_composite = False
        for cj_code, cj in sorted(sinjieo_to_composite_jong.items(), key=lambda x:-len(x[0])):
            if code[i:i+len(cj_code)] == cj_code:
                jong = cj
                i += len(cj_code)
                matched_composite = True
                break

        if not matched_composite:
            for k in sorted(code_to_consonant.keys(), key=lambda x:-len(x)):
                if code[i:i+len(k)] == k:
                    candidate = code_to_consonant[k]
                    if candidate in jongsung_list:
                        next_vowel = False
                        for v in sorted(code_to_vowel.keys(), key=lambda x:-len(x)):
                            if code[i+len(k):i+len(k)+len(v)] == v:
                                next_vowel = True
                                break
                        if not next_vowel:
                            jong = candidate
                            i += len(k)
                    break

        cho_idx = chosung_list.index(cho)
        jung_idx = jungsung_list.index(jung)
        jong_idx = jongsung_list.index(jong) if jong else 0
        char_code = 44032 + (cho_idx*21 + jung_idx)*28 + jong_idx
        result += chr(char_code)

    return result

# -------------------------
# 반복 입력
# -------------------------
def main():
    print("=== 신지어 ↔ 한국어 변환기 (최종 완전판) ===")
    print("종료하려면 'exit' 입력")
    while True:
        text = input("\n한국어 또는 신지어 입력: ").strip()
        if text.lower() == 'exit':
            print("종료합니다.")
            break
        if all(c in '1234567890!?abcdef^&/' for c in text):
            print("한글 변환:", sinjieo_to_hangul(text))
        else:
            print("신지어 변환:", hangul_to_sinjieo(text))

if __name__ == "__main__":
    main()
