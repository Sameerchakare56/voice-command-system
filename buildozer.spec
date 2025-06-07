[app]
title = Voice Command System
package.name = voicecommand
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Requirements for Android
requirements = python3,kivy==2.3.1,plyer,android,pyjnius,SpeechRecognition,pyttsx3

# Android specific
android.permissions = INTERNET, CALL_PHONE, READ_CONTACTS, RECORD_AUDIO
android.api = 33
android.minapi = 21
android.ndk = 23b
android.sdk = 33
android.arch = arm64-v8a
android.accept_sdk_license = True
android.gradle_dependencies = androidx.core:core:1.6.0
android.enable_androidx = True

# App settings
orientation = portrait
fullscreen = 0

# Build settings
android.allow_backup = True
android.archs = arm64-v8a
android.presplash_color = #FFFFFF
android.presplash_lottie = %(source.dir)s/data/logo.json
android.private_storage = True
android.wakelock = True

# Additional settings
android.add_aars = 
android.add_assets = 
android.add_jars = 
android.add_src = 
android.add_libs_arm64-v8a = 
android.add_libs_armeabi-v7a = 
android.add_libs_x86 = 
android.add_libs_mips = 

# Python version
android.python_version = 3

# Kivy version
android.kivy_version = 2.3.1

# Additional settings
osx.python_version = 3
osx.kivy_version = 2.3.1 