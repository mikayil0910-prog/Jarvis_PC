import sys
import os
from openai import OpenAI
import api

# Инициализируем клиент, перенаправляя его на сервер OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api.API_KEY  # Подтянем ключ из переменной окружения
)

# Выбираем модель. На OpenRouter для Gemini формат названия такой:
# Для быстрой: "google/gemini-2.5-flash"
# Для мощной: "google/gemini-2.5-pro"
MODEL_NAME = "google/gemini-2.5-flash"

# Инструкция для твоего ИИ
system_instruction = (
    "Ты — Джарвис, продвинутый терминальный ИИ-ассистент. Твой создатель — Мика. "
    "Отвечай коротко, технически грамотно, с легким сарказмом. Отлично шаришь в Linux и коде."
)

# Будем хранить историю прямо в списке сообщений
messages = [
    {"role": "system", "content": system_instruction}
]

print("==== JARVIS CLI INITIALIZED (via OpenRouter) ====")
print("[Jarvis]: Системы онлайн. Готов к работе, Мика.\n")

while True:
    try:
        user_input = input("[User]: ")

        if user_input.strip().lower() in ['exit', 'quit']:
            print("\n[Jarvis]: Завершение сессии. До встречи.")
            break

        if not user_input.strip():
            continue

        # Добавляем реплику пользователя в историю
        messages.append({"role": "user", "content": user_input})

        print("[Jarvis]: ", end="", flush=True)

        # Делаем запрос с потоковой передачей текста (Stream)
        response_stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
            max_tokens = 1000
        )

        full_response = ""
        for chunk in response_stream:
            # Извлекаем пришедший кусочек текста
            token = chunk.choices[0].delta.content
            if token:
                sys.stdout.write(token)
                sys.stdout.flush()
                full_response += token

        print("\n")  # Перенос строки в конце ответа

        # Сохраняем ответ Джарвиса в историю, чтобы он помнил контекст
        messages.append({"role": "assistant", "content": full_response})

    except KeyboardInterrupt:
        print("\n[Jarvis]: Сессия экстренно прервана.")
        break
    except Exception as e:
        print(f"\n[Jarvis] ОШИБКА: {e}\n")