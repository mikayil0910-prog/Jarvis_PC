from google import genai
import api

# Инициализация нового клиента
client = genai.Client(api_key=api.API_KEY)

# Инструкция
system_instruction = (
    "Ты — Джарвис, продвинутый терминальный ИИ-ассистент. Твой создатель — Мика. "
    "Отвечай коротко, технически грамотно, с легким сарказмом. Отлично шаришь в Linux и коде."
)


chat = client.chats.create(
    model="gemini-3.5-flash",
    config={"system_instruction": system_instruction}
)

print("==== JARVIS CLI INITIALIZED (Gemini GenAI SDK) ====")
print("[Jarvis]: Системы онлайн. Готов к работе, Мика.\n")

while True:
    try:
        user_input = input("[User]: ")
        if user_input.strip().lower() in ['exit', 'quit']:
            break

        print("[Jarvis]: ", end="", flush=True)

        # В новой библиотеке stream передается внутри send_message,
        # но мы используем метод, который возвращает итератор
        response = chat.send_message_stream(user_input)

        for chunk in response:
            print(chunk.text, end="", flush=True)

        print("\n")

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\n[Jarvis] ОШИБКА: {e}\n")