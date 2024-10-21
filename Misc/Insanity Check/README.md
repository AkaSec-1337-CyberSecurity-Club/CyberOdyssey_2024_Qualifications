# [**Insanity Check**](#)

## Description:
* Can you find the flag without losing your sanity? I hope so! The flag is located within the [Discord server](https://discord.gg/wHksSaTa83) (It's plaintext in the server).

## Difficulty:
* Hard

## Objective:
The objective of this challenge is the find the hidden flag in the [Discord server](https://discord.gg/wHksSaTa83).

## Solution:
The flag was the name of a hidden role in the server, we can use the [Discord API](https://discord.com/developers/docs/resources/guild#get-guild-roles) to get a list of roles for the guild.

![](img/solution.png)

## Payload:
```sh
curl -H "Authorization: YOUR-DISCORD-TOKEN" https://discord.com/api/v10/guilds/1155843471899381811/roles
```