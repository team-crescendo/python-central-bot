async def interact_with_reaction(bot,  target_user, initial_message, callback, emojis=["⭕", "❌"], timeout=60):
    Y, N, *_ = emojis

    o = await bot.reply(
        initial_message
    )

    await bot.add_reaction(o, Y)
    await bot.add_reaction(o, N)
    
    r = await bot.wait_for_reaction(emoji=[Y, N], timeout=timeout, message=o, user=target_user)

    await bot.delete_message(o)

    if r and str(r.reaction.emoji) == Y:
        await callback()
