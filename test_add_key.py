""" Задание 2.
Дополнить все тесты ключом команды 7z -t
(тип архива). Вынести этот параметр в конфиг. """

from checkers import checkout
import subprocess
import yaml

with open('config.yaml') as f:
    # читаем YAML документ
    data = yaml.safe_load(f)


class TestPositiv:

    def test_step1(self, make_folders, clear_folders, make_files):
        """проверка команды a (архивация)"""
        res1 = self.checkout(f"cd {data['folder_tst']}; 7z {data['archive_type']} a {data['folder_out']}/arx2",
                             "Everything is Ok")
        res2 = self.checkout(f"ls {data['folder_out']}", "arx2.7z")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        """проверка команды e (распаковка)"""
        res = []
        res.append(self.checkout(f"cd {data['folder_tst']}; 7z {data['archive_type']} a {data['folder_out']}/arx2",
                                 "Everything is Ok"))  # новая запаковка, чтобы тесты были независимы
        res.append(
            self.checkout(f"cd {data['folder_out']}; 7z {data['archive_type']} e arx2.7z -o{data['folder_ext']} -y",
                          "Everything is Ok"))  # распаковка
        for item in make_files:
            res.append(self.checkout(f"ls {data['folder_ext']}", "test1"))  # проверка наличия файла

        assert all(res), "test2 FAIL"

    def test_step1_1(self):
        """дополнительная проверка создания файла во время архивирования"""
        res_1 = self.checkout(f"cd {data['folder_out']}; 7z {data['archive_type']} a ../out/арх2 test_file.txt",
                              "Everithing is ok")
        res_2 = self.checkout(f"ls {data['folder_out']};", "арх2.7z")
        assert res_1 and res_2, "test 1_1 FAIL"

    def test_step2_1(self):
        """проверка создания файла во время распаковки"""
        res_1 = self.checkout(f"cd {data['folder_out']}; 7z {data['archive_type']} e арх2.7z -o{data['folder_ext']}",
                              "Everithing is ok")
        res_2 = self.checkout(f"ls {data['folder_out']};", "тестовый_файл.txt")
        assert res_1 and res_2, "test 2_1 FAIL"

    def test_step3(self):
        """проверка команды t (проверка целостности архива)"""
        assert self.checkout(f"cd {data['folder_out']}; 7z {data['archive_type']} t арх2.7z",
                             "Everithing is ok"), "test 3 FAIL"

    def test_step4(self):
        """проверка команды u (обновление архива)"""
        assert self.checkout(f"cd {data['folder_out']}; 7z {data['archive_type']} u арх2.7z",
                             "Everithing is ok"), "test 4 FAIL"

    def test_step5(self):
        """проверка команды d (удаление из архива)"""
        assert self.checkout(f"cd {data['folder_out']}; 7z {data['archive_type']} d арх.7z",
                             "Everithing is ok"), "test 5 FAIL"

    def test_step6(self, clear_folders, make_files):
        """проверка команды l (список файлов)"""
        res = []
        res.append(self.checkout(f"cd {data['folder_tst']}; 7z {data['archive_type']} a {data['folder_out']}/арх2",
                                 "Everything is Ok"))  # новая архивация для независимого теста
        for item in make_files:
            res.append(
                self.checkout(f"cd {data['folder_out']}; 7z {data['archive_type']} l арх2.7z {data['folder_ext']}",
                              f"{data['file_in_ext']}"))
        assert all(res), "test 6 FAIL"

    def test_step7(self, clear_folders, make_files, make_subfolder):
        """проверка команды x (извлечение с сохранением пути)"""
        res = []
        res.append(self.checkout(f"cd {data['folder_tst']}; 7z {data['archive_type']} a {data['folder_out']}/арх2",
                                 "Everything is Ok"))  # новая архивация для независимого теста
        res.append(self.checkout(f"cd {data['folder_out']}; 7z {data['archive_type']} x арх.7z -o{data['folder_ext']}",
                                 "Everithing is ok"))  # распаковка

        for item in make_files:
            res.append(self.checkout(f"ls {data['folder_ext_2']}", item))

        res.append(
            self.checkout(f"ls {data['folder_ext_2']} /", make_subfolder[0]))  # поиск по созданному имени подпапки
        res.append(self.checkout(f"ls {data['folder_ext2']}/{make_subfolder[0]}"), make_subfolder[1])
        assert all(res), "test6 FAIL"

    def test_step8(self, clear_folders, make_files):
        """проверка команды h (вычисление хэша)"""
        res = []
        for item in make_files:
            res.append(
                self.checkout(f"cd {data['folder_tst']}; 7z {data['archive_type']} h {item}", "Everything is Ok"))
            hash_value = subprocess.run(f"cd {data['folder_tst']}; crc32 {item}", shell=True, stdout=subprocess.PIPE,
                                        encoding="utf-8").stdout.strip().upper()
            res.append(self.checkout(f"cd {data['folder_tst']}; 7z {data['archive_type']} h {item}", hash_value))
        assert all(res), "test 8 FAIL"