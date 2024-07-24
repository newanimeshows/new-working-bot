[![Typing SVG](https://readme-typing-svg.demolab.com?font=Bold&size=50&duration=5051&pause=1000&color=F70202&width=1090&height=90&lines=This+is+a+File+Store+Bot+Repo;Made+With+Python+And+Html;Created+By+AniShin+and+Admin)](https://git.io/typing-svg)

 



<div align="center">
    <strong>Happy Coding!</strong>
</div>

### CONFIGS VARIABLES FOR DEPLOYMENT

* `API_HASH` Your API Hash from my.telegram.org
* `APP_ID` Your API ID from my.telegram.org
* `TG_BOT_TOKEN` Your bot token from @BotFather
* `OWNER_ID` Must enter Your Telegram Id
* `CHANNEL_ID` Your Channel ID eg:- -100xxxxxxxx
* `DB_URL` Your mongo db url
* `DB_NAME` Your mongo db session name
* `ADMINS` Optional: A space separated list of user_ids of Admins, they can only create links
* `START_MESSAGE` Optional: start message of bot
* `FORCE_SUB_MESSAGE`Optional:Force sub message of bot, use HTML and Fillings
* `FORCE_SUB_CHANNEL1` Optional: ForceSub Channel 1 ID, leave 0 if you want disable force sub
* `FORCE_SUB_CHANNEL2` Optional: ForceSub Channel 2 ID, leave 0 if you want disable force sub
* `PROTECT_CONTENT` Optional: True if you need to prevent files from forwarding



### EXTRA VARIABLES

* `CUSTOM_CAPTION` put your Custom caption text if you want Setup Custom Caption, you can use HTML and <a href='https://github.com/JishuDeveloper/File-Sharing-Premium-Bot/blob/main/README.md#custom_caption'>fillings</a> for formatting (only for documents)
* `DISABLE_CHANNEL_BUTTON` Put True to Disable Channel Share Button, Default if False
* `BOT_STATS_TEXT` put your custom text for stats command, use HTML and <a href='https://github.com/JishuDeveloper/File-Sharing-Premium-Bot/blob/main/README.md#custom_stats'>fillings</a>
* `USER_REPLY_TEXT` put your text to show when user sends any message, use HTML


### Getting Help

<summary>Support</summary>
<p>
If you need assistance or have any questions, you can contact the admin of this bot:

[![Contact Admin on Telegram](https://img.shields.io/badge/Contact%20Admin-on%20Telegram-blue?style=for-the-badge&logo=telegram)](https://t.me/DarkHumorHub_bot)

</p>


### DEPLOYEMENT SUPPORT

<summary>Deploy To Koyeb</summary>
<p>
<br>                 
<a target="/blank" href="https://app.koyeb.com/deploy?type=git&repository=github.com/JishuDeveloper/File-Sharing-Premium-Bot&branch=main&name=file-sharing-bot" >
  <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy">
</a>
</p>

<summary>Deploy To Heroku</summary>
<p>
<br>
<a href="https://heroku.com/deploy?template=https://github.com/JishuDeveloper/File-Sharing-Premium-Bot">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
</a>
</p>



### FEATURES
- Fully customisable.
- Auto Delete Added.
- main Branch Means 2 force subs.
- Customisable welcome & Forcesub messages.
- More than one Posts in One Link.
- Can be deployed on heroku directly.
- Deploy to Koyeb + Heroku + Railway + Render
- Developer Service 24x7.



### SETUP

- Add the bot to Database Channel with all permission
- Add bot to ForceSub channel as Admin with Invite Users via Link Permission if you enabled ForceSub


### FILLINGS
#### START_MESSAGE | FORCE_SUB_MESSAGE

* `{first}` - User first name
* `{last}` - User last name
* `{id}` - User ID
* `{mention}` - Mention the user
* `{username}` - Username

#### CUSTOM_CAPTION

* `{filename}` - file name of the Document
* `{previouscaption}` - Original Caption

#### CUSTOM_STATS

* `{uptime}` - Bot Uptime


### ALL COMMANDS

```
Bot Command Descriptions:
start - Start the bot or get posts.
batch - Create a link for more than one post.
genlink - Create a link for one post.
customBatch - Create a link for a custom batch of posts.
users - View bot statistics.
broadcast - Broadcast any message to bot users.
stats - Check the bot uptime.
```
