<div align="center">

  <p align="center">
    <a href="https://t.me/cry_batya">
      <img src="https://img.shields.io/badge/Telegram-Channel-blue?style=for-the-badge&logo=telegram" alt="Telegram Channel">
    </a>
    <a href="https://t.me/+b0BPbs7V1aE2NDFi">
      <img src="https://img.shields.io/badge/Telegram-Chat-blue?style=for-the-badge&logo=telegram" alt="Telegram Chat">
    </a>
  </p>
</div>
# Solver StarLabs

Free local solver for StarLabs soft

## Установка / Installation
1. Установить / Installation: 0g 
```bash
https://github.com/TellBip/api_for_hcaptcha-challenger
```
1. Установить / Installation: Monad or MegaETH
```bash
https://github.com/Theyka/Turnstile-Solver
```

2. В файле captcha.py изменить адрес сервера / Change server address in captcha.py file :
```python
self.base_url = "http://localhost:5000" → self.base_url = "ваш_адрес"
```

3. Заменить файл / Replace file:

Скопировать нужный файл в папку и переименовать / copy  file in folder and rename:
```
StarLabs-MegaETH/src/model/help/captcha.py
or
StarLabs-Monad/src/model/help/captcha.py
or
StarLabs-0G/src/model/help/captcha.py
```

## Запуск / Running
Запустить солвер / Start the solver: Monad or MegaETH
```bash
python3 api_solver.py --browser_type camoufox --headless True --host 0.0.0.0 --thread 2
```
Запустить солвер / Start the solver: 0g
```bash
python3 hcaptcha_api_server.py --headless True --useragent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" --thread=1 --api_key=апи-ключ
```
После этого можно использовать софт StarLabs / After that you can use StarLabs software.

## Поддержка / Support
Все вопросы в чат / All questions in chat:
[https://t.me/+b0BPbs7V1aE2NDFi](https://t.me/+b0BPbs7V1aE2NDFi)

