# @Time    : 2024/5/11 23:16
# @Author  : TwoOnefour
# @blog    : https://www.pursuecode.cn
# @Email   : twoonefour@pursuecode.cn
# @File    : srtgpt.py
import pysrt
import asyncio
import openai
import os
async def translate_text(client, text):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "你是一个翻译官，你只需要把我发给你的语言翻译成中文，不要带有其他词"
            },
            {
                "role": "user",
                "content": "Denaro? Violenza?",
            },
            {
                "role": "assistant",
                "content": "金钱？暴力？"
            },
            {
                "role": "user",
                "content": f"{text}"
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content

async def main():
    openai.proxy = "http://127.0.0.1:10809"
    client = openai.AsyncOpenAI(
        # This is the default and can be omitted
        api_key="",
    )
    for srt in os.listdir("srts/source"):
        subs = pysrt.open(f'srts/source/{srt}', encoding='utf-8')
        asyncio_task = [translate_text(client, sub.text) for sub in subs]
        res = await asyncio.gather(*asyncio_task)
        for i, sub in enumerate(subs):
            sub.text = res[i]
        subs.save(f'srts/output/{srt}', encoding='utf-8')
asyncio.run(main())
# 保存翻译后的字幕到新文件

