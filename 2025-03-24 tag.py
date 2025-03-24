import discord
import re
import os
from dotenv import load_dotenv

#env 파일 읽기
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

all_tags = []

@client.event
async def on_ready():
    print(f'✅ 봇이 로그인됨: {client.user}')

# 태그 추가 함수
async def handle_tag_add(message):
    # 1. 해시태그 추출(정규표현식 사용)
    tags = re.findall(r'#\w+', message.content)

    # 2. 태그 저장
    all_tags.extend(tags) # 새로운 태그 추가
    all_tags[:] = sorted(list(set(all_tags))) # 중복 제거 & 정렬

    # 3. 태그 출력
    if tags:
        tag_text = ', '.join(tags)
        await message.channel.send(f"등록된 태그: {tag_text}")
    else:
        await message.channel.send("태그가 없습니다. 예시: '!tag #공부 #감성'")

# 태그 목록 출력 함수        
async def handle_tag_list(message):
    if all_tags:
        await message.channel.send(f"현재 태그 목록: {', '.join(all_tags)}")
    else:
        await message.channel.send("등록된 태그가 없습니다.")

# 태그 삭제 함수        
async def handle_tag_remove(message):
    tags_remove = re.findall(r'#\w+', message.content)

    # 삭제할 태그가 있다면
    if tags_remove:
        removed = []
        for tag in tags_remove:
            if tag in all_tags:
                all_tags.remove(tag)
                removed.append(tag)
                        
        if removed:
            await message.channel.send(f"삭제된 태그: {', '.join(removed)}")
        # 입력한 태그가 tag-list에 없을 때
        else:
            await message.channel.send(f"입력한 태그는 등록된 태그 목록에 없습니다.")
    # !tag-remove는 입력했지만 태그 입력을 안했을 때 
    else:
        await message.channel.send(f"삭제할 태그를 입력해주세요. 예시: '!tag-remove #감성'")
    
# 디스코드에 메시지가 올라왔을 때 반응하는 이벤트 핸들러
@client.event
async def on_message(message):
    # 봇 자신이 보낸 메시지는 무시
    if message.author == client.user:
        return

    # 태그 추가 함수 호출
    if message.content.startswith('!tag') and not message.content.startswith('!tag-list') and not message.content.startswith('!tag-remove'):
        await handle_tag_add(message)

    # 태그 목록 함수 호출
    if message.content == '!tag-list':
        await handle_tag_list(message)

    # 태그 삭제 함수 호출
    if message.content.startswith('!tag-remove'):
        await handle_tag_remove(message)

# 여기에 팀원에게 받은 토큰 입력
client.run(TOKEN)
