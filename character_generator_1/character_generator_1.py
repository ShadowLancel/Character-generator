# coding=utf-8
import os
import string
from PIL import Image, ImageDraw, ImageFont
import random

def create_output_folder(output_folder):
    # �������� ����� ��� ���������� �����������, ���� � ���
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def get_font_files(fonts_folder):
    # ��������� ������ ���� �������
    return [os.path.join(fonts_folder, f) for f in os.listdir(fonts_folder) if f.endswith(('.ttf', '.otf'))]

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def generate_image(font_file, text, image_size=(100, 100)):
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file, 20)
    
    # ��������� ��������������� �������������� ������ ������
    bbox = draw.textbbox((0, 0), text, font)
    
    # ���������� ������ � ������ ������
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (image_size[0] - text_width) // 2
    y = (image_size[1] - text_height) // 2
    draw.text((x, y), text, font=font, fill="black")
    return image

def generate_images(output_folder, num_images, fonts_folder, min_length=1, max_length=5, image_size=(100, 100)):
    create_output_folder(output_folder)
    font_files = get_font_files(fonts_folder)

    train_folder = os.path.join(output_folder, "train_imgs")
    test_folder = os.path.join(output_folder, "test_imgs")
    create_output_folder(train_folder)
    create_output_folder(test_folder)

    train_ratio = 0.8
    num_train_images = int(num_images * train_ratio)

    # �������������� ������ ������
    font_index = 0

    for i in range(num_train_images):
        # ����� �������� ������
        font_file = font_files[font_index]

        # ��������� ��������� ����� ������
        length = random.randint(min_length, max_length)

        # ��������� ��������� ������
        text = generate_random_string(length)

        # �������� �����������
        image = generate_image(font_file, text, image_size)

        # �������� ����� ��� ����������
        class_folder = os.path.join(train_folder, f"class_{font_index}")

        create_output_folder(class_folder)

        image_filename = f"image_{i}.png"
        image_path = os.path.join(class_folder, image_filename)
        image.save(image_path)

        # ����������� ������ ������, ���� ��������� ����� ������
        font_index = (font_index + 1) % len(font_files)

    print(f"������������� {num_train_images} ����������� � ������ {train_folder} (80%).")

    # ��������� �������� �������
    num_test_images = num_images - num_train_images

    # �������������� ������ ������ ��� �������� �������
    font_index = 0

    for i in range(num_test_images):
        # ����� �������� ������
        font_file = font_files[font_index]

        # ��������� ��������� ����� ������
        length = random.randint(min_length, max_length)

        # ��������� ��������� ������
        text = generate_random_string(length)

        # �������� �����������
        image = generate_image(font_file, text, image_size)

        # �������� ����� ��� ����������
        class_folder = os.path.join(test_folder, f"class_{font_index}")

        create_output_folder(class_folder)

        image_filename = f"image_{i + num_train_images}.png"
        image_path = os.path.join(class_folder, image_filename)
        image.save(image_path)

        # ����������� ������ ������, ���� ��������� ����� ������
        font_index = (font_index + 1) % len(font_files)

    print(f"Generate {num_train_images} train images and {num_test_images} test images.")

def main():
    output_folder = "output"
    num_images = 5000
    fonts_folder = "fonts"
    min_length = 1
    max_length = 5
    image_size = (100, 100)

    generate_images(output_folder, num_images, fonts_folder, min_length, max_length, image_size)

if __name__ == "__main__":
    main()
