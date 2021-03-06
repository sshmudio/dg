from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from mrz.generator.td3 import *
from transliterate import translit

MF = ImageFont.truetype('cfg/font/sans.ttf', 34)  # Основной шрифт
FFMRZ = ImageFont.truetype('cfg/font/cour.ttf', 47)  # Шрифт для MRZ
WIDTH = 440
SW = 440  # НАчальная ширина
SH = 1060
MFC = (40, 40, 40)  # Основной цвет шрифта


def write_main_data(mrz, save_after_main_data,  typedoc,  country,  id_number,  surname,  given_name,  genre,  birth_date):
    """ Нанесение на шаблон документа основной информации """
    img = Image.open('cfg/template/uain.png')  # Шаблон паспорта

    draw = ImageDraw.Draw(img)

    draw.text((WIDTH, SH), str(typedoc), MFC, font=MF)  # Иип документа

    draw.text((WIDTH + 140, SH), str(country),
              MFC, font=MF)  # Страна выдачи

    draw.text((WIDTH + 489, SH),  id_number, MFC,
              font=MF)  # Уникальный номер документа

    draw.text((WIDTH, SH + 67), str(surname + '/' + translit(surname,
                                                             'uk', reversed=True)).upper(), MFC,
              font=MF)  # Фамилия

    draw.text((WIDTH, SH + 134), str(given_name + '/' + translit(given_name,
                                                                 'uk', reversed=True)).upper(), MFC,
              font=MF)  # Имя влядельца документа

    draw.text((WIDTH, SH + 201),  country, MFC, font=MF)  # Гражданство

    draw.text((WIDTH, SH + 268), str('22 ЛЮТ/FEB 89'),
              MFC, font=MF)  # Дата рождения

    ''' ПОЛ '''
    if genre == "M":
        g = 'Ч/M'
    else:
        g = 'Ж/F'
    draw.text((WIDTH, SH + 335), g, MFC, font=MF)  # Пол
    ''' end ПОЛ '''

    draw.text((WIDTH + 489, SH + 268), str(birth_date) +
              '-' + '1233', MFC, font=MF)  # Персональный номер

    draw.text((WIDTH + 160, SH + 335), str('м. Київ/UKR').upper(),
              MFC, font=MF)  # Город

    draw.text((WIDTH + 460, 770), "ЕН № 14205", (178, 34, 34),
              font=ImageFont.truetype('media/cfg/font/sans.ttf', 40))

    draw.text((WIDTH, SH + 402), "22 ЛЮТ/FEB 15", MFC, font=MF)  # Дата выдачи

    draw.text((WIDTH, SH + 469), "19 ЛЮТ/FEB 25",
              MFC, font=MF)  # Дата окончания

    # Орган который выдал документ
    draw.text((WIDTH + 489, SH + 402), '8099', MFC, font=MF)

    draw.text((60, SH + 650), str(mrz), MFC, font=FFMRZ)  # Добавляем mrz

    img.save(save_after_main_data)
    return save_after_main_data


def write_id(save_after_main_data_p,  id_number):
    passport_number = id_number
    font = ImageFont.truetype('cfg/font/SNEgCheck1MP.ttf', 120)
    line_height = sum(font.getmetrics())  # в нашем случае 33 + 8 = 41
    fontimage = Image.new('L', (font.getsize(passport_number)[0], line_height))
    # И рисуем на ней белый текст
    ImageDraw.Draw(fontimage).text(
        (0, 0), passport_number, fill=120, font=font)
    fontimage = fontimage.rotate(90, resample=Image.BICUBIC, expand=True)
    orig = Image.open(save_after_main_data_p)
    orig.paste((67, 67, 67), box=(30, 180), mask=fontimage)
    orig.save(save_after_main_data_p)
    return save_after_main_data_p


def paste_photo(passport_temp_path, passport_photo_path, holohrama_path, all_done_path):
    passport_temp = Image.open(passport_temp_path).convert('RGBA')

    passport_photo = Image.open(passport_photo_path)
    width, height = passport_photo.size
    new_height = 425  # Высота
    new_width = int(new_height * width / height)
    passport_photo = passport_photo.resize(
        (new_width, new_height), Image.ANTIALIAS)
    if passport_photo.mode != 'RGBA':
        alpha_passpor_photo = Image.new('RGBA', (10, 10), 20)
        passport_photo.putalpha(alpha_passpor_photo)
    paste_mask_passport_photo = passport_photo.split()[
        3].point(lambda i: i * 17 / 100.)

    passport_temp.paste(passport_photo, (80, SH + 125),
                        mask=paste_mask_passport_photo)

    img = Image.open(holohrama_path)  # открываем файл голограммы
    wpercent = (500 / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((500, hsize), Image.ANTIALIAS)
    if img.mode != 'RGBA':
        alpha = Image.new('RGBA', (10, 10), 20)
        img.putalpha(alpha)
    paste_mask = img.split()[3].point(lambda i: i * 17 / 100.)
    passport_temp.paste(img, (140, SH + 310), mask=paste_mask)
    passport_temp.save(all_done_path)

    # passport_temp = Image.open(passport_temp_path).convert('RGBA')
    # passport_photo = Image.open(passport_photo_path)
    # width, height = passport_photo.size
    # new_height = 425  # Высота
    # new_width = int(new_height * width / height)
    # # gradient = get_gradient_3d(512, 256, (0, 0, 0), (255, 255, 255), (True, True, True))
    # # Image.fromarray(np.uint8(gradient)).save('cfg/out/gg.jpg', quality=95)
    # passport_photo = passport_photo.resize(
    #     (new_width, new_height), Image.ANTIALIAS)
    # passport_temp.paste(passport_photo, (80, SH + 125), passport_photo)
    # img = Image.open(holohrama_path)
    # wpercent = (500 / float(img.size[0]))
    # hsize = int((float(img.size[1]) * float(wpercent)))
    # img = img.resize((500, hsize), Image.ANTIALIAS)
    # if img.mode != 'RGBA':
    #     alpha = Image.new('RGBA', (10, 10), 20)
    #     img.putalpha(alpha)
    # paste_mask = img.split()[3].point(lambda i: i * 17 / 100.)
    # passport_temp.paste(img, (140, SH + 310), mask=paste_mask)
    # passport_temp.save(all_done_path)
    # return all_done_path
