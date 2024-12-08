Для запуска приложения требуется сделать следующие шаги:

1. Активировать виртуальную среду командой `.venv-win/Scripts/activate` на Windows или `source .venv-nix/bin/activate` на Linux/macOS.
2. Запустить сервер командой `python -m flask --app server run`
3. Запустить тестовый скрипт командой `py.test -v test.py`

Если всё сделано верно, выведутся 9 тестов в статусе PASSED.