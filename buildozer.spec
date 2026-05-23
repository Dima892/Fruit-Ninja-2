[app]
source.dir = .
title = Fruit Ninja 
package.name = myapp
package.domain = org.test
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy

# Используем API 33 для совместимости
android.api = 33
android.minapi = 21

# Главная настройка: запрещаем автоматическое скачивание и обновление
android.skip_sdk_update = True
android.accept_sdk_license = True

# Указываем архитектуру ARM64
android.archs = arm64-v8a

[buildozer]
log_level = 2

