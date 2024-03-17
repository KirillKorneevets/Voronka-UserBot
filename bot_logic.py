from db_config import async_session
from service import add_user, listen_for_message, user_status_finished, user_status_dead
from exceptions import BotBlocked, UserDeactivated

users_with_question = {}

async def setup_handlers(app):
    @app.on_message()
    async def handle_message(client, message):
        user_id = message.from_user.id
        async with async_session() as session:
            await add_user(user_id, session)
            await session.commit()
        
        if user_id not in users_with_question:
            users_with_question[user_id] = True
            await client.send_message(message.chat.id, "Приветствуем вас! Расскажите, чему вы хотели бы научиться на нашем вебинаре IT.\n"
                                                       "Выберите один из вариантов:\n"
                                                       "1. Python\n"
                                                       "2. Data Science\n"
                                                       "3. Web Development\n"
                                                       "Ответьте цифрой на интересующий вас вариант или напишите свой вопрос.")
            

        response = await listen_for_message(message)

        try:
            if response == "1":
                await client.send_message(message.chat.id, "Отличный выбор! Мы с удовольствием расскажем вам о Python на нашем вебинаре. Вы успешно записаны")
            elif response == "2":
                await client.send_message(message.chat.id, "Data Science - это интересная область. Мы готовы поделиться своими знаниями на нашем вебинаре. Вы успешно записаны")
            elif response == "3":
                await client.send_message(message.chat.id, "Web Development - отличный выбор для изучения. Давайте начнем с основ на нашем вебинаре. Вы успешно записаны")


            if any(word in response.lower() for word in ["прекрасно", "ожидать"]):
                async with async_session() as session:
                    await user_status_finished(user_id, session)
                users_with_question.pop(user_id)
                return await client.send_message(message.chat.id, " Воронка завершена.")

            if response.lower() == "отмена":
                users_with_question.pop(user_id)
                return await client.send_message(message.chat.id, "Отправка сообщения отменена. Можете задать другой вопрос.")

            elif response.lower() == "завершить":
                users_with_question.pop(user_id)
                return await client.send_message(message.chat.id, "Спасибо за участие в нашем вебинаре!")


        except BotBlocked:
            async with async_session() as session:
                await user_status_dead(user_id, session)
            users_with_question.pop(user_id)
            return await client.send_message(message.chat.id, "Произошла ошибка при отправке сообщения. Воронка завершена.")
        
        except UserDeactivated:
            async with async_session() as session:
                await user_status_dead(user_id, session)
            users_with_question.pop(user_id)
            return await client.send_message(message.chat.id, "Пользователь деактивировал свой аккаунт. Воронка завершена.")




