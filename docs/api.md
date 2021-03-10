# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [discord_api.proto](#discord_api.proto)
    - [Channel](#discord_api.Channel)
    - [Embed](#discord_api.Embed)
    - [Embed.Author](#discord_api.Embed.Author)
    - [Embed.Field](#discord_api.Embed.Field)
    - [Embed.Footer](#discord_api.Embed.Footer)
    - [Embed.Image](#discord_api.Embed.Image)
    - [Embed.Provider](#discord_api.Embed.Provider)
    - [Embed.Thumbnail](#discord_api.Embed.Thumbnail)
    - [Embed.Video](#discord_api.Embed.Video)
    - [Emoji](#discord_api.Emoji)
    - [GetGuildChannelsRequest](#discord_api.GetGuildChannelsRequest)
    - [GetGuildChannelsResponse](#discord_api.GetGuildChannelsResponse)
    - [GuildMember](#discord_api.GuildMember)
    - [Message](#discord_api.Message)
    - [Message.Activity](#discord_api.Message.Activity)
    - [Message.Application](#discord_api.Message.Application)
    - [Message.Attachment](#discord_api.Message.Attachment)
    - [Message.ChannelMention](#discord_api.Message.ChannelMention)
    - [Message.Reaction](#discord_api.Message.Reaction)
    - [Message.Reference](#discord_api.Message.Reference)
    - [Message.Sticker](#discord_api.Message.Sticker)
    - [Role](#discord_api.Role)
    - [Role.Tag](#discord_api.Role.Tag)
    - [SendChannelMessageRequest](#discord_api.SendChannelMessageRequest)
    - [SendChannelMessageResponse](#discord_api.SendChannelMessageResponse)
    - [SendDirectMessageRequest](#discord_api.SendDirectMessageRequest)
    - [SendDirectMessageResponse](#discord_api.SendDirectMessageResponse)
    - [User](#discord_api.User)

    - [Channel.Type](#discord_api.Channel.Type)
    - [Message.Activity.Type](#discord_api.Message.Activity.Type)
    - [Message.Sticker.Type](#discord_api.Message.Sticker.Type)
    - [Message.Type](#discord_api.Message.Type)

    - [DiscordApi](#discord_api.DiscordApi)

- [Scalar Value Types](#scalar-value-types)



<a name="discord_api.proto"></a>
<p align="right"><a href="#top">Top</a></p>

## discord_api.proto
Discord API service

This file contains all messages and services currently supported by Discord Proxy


<a name="discord_api.Channel"></a>

### Channel
Source: https://discord.com/developers/docs/resources/channel#channel-object


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| type | [Channel.Type](#discord_api.Channel.Type) |  |  |
| guild_id | [uint64](#uint64) |  |  |
| position | [int32](#int32) |  |  |
| name | [string](#string) |  | tbd // |
| topic | [string](#string) |  |  |






<a name="discord_api.Embed"></a>

### Embed
Source: https://discord.com/developers/docs/resources/channel#embed-object-embed-structure


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| title | [string](#string) |  |  |
| type | [string](#string) |  |  |
| description | [string](#string) |  |  |
| url | [string](#string) |  |  |
| timestamp | [string](#string) |  |  |
| color | [int32](#int32) |  |  |
| footer | [Embed.Footer](#discord_api.Embed.Footer) |  |  |
| image | [Embed.Image](#discord_api.Embed.Image) |  |  |
| thumbnail | [Embed.Thumbnail](#discord_api.Embed.Thumbnail) |  |  |
| video | [Embed.Video](#discord_api.Embed.Video) |  |  |
| provider | [Embed.Provider](#discord_api.Embed.Provider) |  |  |
| author | [Embed.Author](#discord_api.Embed.Author) |  |  |
| fields | [Embed.Field](#discord_api.Embed.Field) | repeated |  |






<a name="discord_api.Embed.Author"></a>

### Embed.Author



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  |  |
| url | [string](#string) |  |  |
| icon_url | [string](#string) |  |  |
| proxy_icon_url | [string](#string) |  |  |






<a name="discord_api.Embed.Field"></a>

### Embed.Field



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  |  |
| value | [string](#string) |  |  |
| inline | [bool](#bool) |  |  |






<a name="discord_api.Embed.Footer"></a>

### Embed.Footer



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  |  |
| icon_url | [string](#string) |  |  |
| proxy_icon_url | [string](#string) |  |  |






<a name="discord_api.Embed.Image"></a>

### Embed.Image



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| url | [string](#string) |  |  |
| proxy_icon_url | [string](#string) |  |  |
| height | [int32](#int32) |  |  |
| width | [int32](#int32) |  |  |






<a name="discord_api.Embed.Provider"></a>

### Embed.Provider



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  |  |
| url | [string](#string) |  |  |






<a name="discord_api.Embed.Thumbnail"></a>

### Embed.Thumbnail



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| url | [string](#string) |  |  |
| proxy_url | [string](#string) |  |  |
| height | [int32](#int32) |  |  |
| width | [int32](#int32) |  |  |






<a name="discord_api.Embed.Video"></a>

### Embed.Video



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| url | [string](#string) |  |  |
| proxy_icon_url | [string](#string) |  |  |
| height | [int32](#int32) |  |  |
| width | [int32](#int32) |  |  |






<a name="discord_api.Emoji"></a>

### Emoji
Source: https://discord.com/developers/docs/resources/emoji#emoji-object


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| name | [string](#string) |  |  |
| roles | [uint64](#uint64) | repeated |  |
| user | [User](#discord_api.User) |  |  |
| required_colons | [bool](#bool) |  |  |
| managed | [bool](#bool) |  |  |
| animated | [bool](#bool) |  |  |
| available | [bool](#bool) |  |  |






<a name="discord_api.GetGuildChannelsRequest"></a>

### GetGuildChannelsRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| guild_id | [uint64](#uint64) |  |  |






<a name="discord_api.GetGuildChannelsResponse"></a>

### GetGuildChannelsResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| channels | [Channel](#discord_api.Channel) | repeated |  |






<a name="discord_api.GuildMember"></a>

### GuildMember
Source: https://discord.com/developers/docs/resources/guild#guild-member-object


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| user | [User](#discord_api.User) |  |  |
| nick | [string](#string) |  |  |
| roles | [uint64](#uint64) | repeated |  |
| joined_at | [string](#string) |  |  |
| premium_since | [string](#string) |  |  |
| deaf | [bool](#bool) |  |  |
| mute | [bool](#bool) |  |  |
| pending | [bool](#bool) |  |  |
| permissions | [string](#string) |  |  |






<a name="discord_api.Message"></a>

### Message
Source: https://discord.com/developers/docs/resources/channel#message-object


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| channel_id | [uint64](#uint64) |  |  |
| guild_id | [uint64](#uint64) |  |  |
| author | [User](#discord_api.User) |  |  |
| member | [GuildMember](#discord_api.GuildMember) |  |  |
| content | [string](#string) |  |  |
| timestamp | [string](#string) |  |  |
| edited_timestamp | [string](#string) |  |  |
| tts | [bool](#bool) |  |  |
| mention_everyone | [bool](#bool) |  |  |
| mentions | [User](#discord_api.User) | repeated |  |
| mention_roles | [uint64](#uint64) | repeated |  |
| mention_channels | [uint64](#uint64) | repeated |  |
| attachments | [Message.Attachment](#discord_api.Message.Attachment) | repeated |  |
| embeds | [Embed](#discord_api.Embed) | repeated |  |
| reactions | [Message.Reaction](#discord_api.Message.Reaction) | repeated |  |
| nonce | [string](#string) |  |  |
| pinned | [bool](#bool) |  |  |
| webhook_id | [uint64](#uint64) |  |  |
| type | [Message.Type](#discord_api.Message.Type) |  |  |
| activity | [Message.Activity](#discord_api.Message.Activity) |  |  |
| application | [Message.Application](#discord_api.Message.Application) |  |  |
| message_reference | [Message.Reference](#discord_api.Message.Reference) |  |  |
| flags | [int32](#int32) |  |  |
| stickers | [Message.Sticker](#discord_api.Message.Sticker) | repeated |  |
| referenced_message | [Message](#discord_api.Message) |  | interaction: not implemented |






<a name="discord_api.Message.Activity"></a>

### Message.Activity



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [Message.Activity.Type](#discord_api.Message.Activity.Type) |  |  |
| party_id | [string](#string) |  |  |






<a name="discord_api.Message.Application"></a>

### Message.Application



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| cover_image | [string](#string) |  |  |
| description | [string](#string) |  |  |
| icon | [string](#string) |  |  |
| name | [string](#string) |  |  |






<a name="discord_api.Message.Attachment"></a>

### Message.Attachment



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| filename | [string](#string) |  |  |
| size | [int32](#int32) |  |  |
| url | [string](#string) |  |  |
| proxy_url | [string](#string) |  |  |
| height | [int32](#int32) |  |  |
| width | [int32](#int32) |  |  |






<a name="discord_api.Message.ChannelMention"></a>

### Message.ChannelMention



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| guild_id | [uint64](#uint64) |  |  |
| type | [Channel.Type](#discord_api.Channel.Type) |  |  |
| name | [string](#string) |  |  |






<a name="discord_api.Message.Reaction"></a>

### Message.Reaction



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| count | [int32](#int32) |  |  |
| me | [bool](#bool) |  |  |
| emoji | [Emoji](#discord_api.Emoji) |  |  |






<a name="discord_api.Message.Reference"></a>

### Message.Reference



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| message_id | [uint64](#uint64) |  |  |
| channel_id | [uint64](#uint64) |  |  |
| guild_id | [uint64](#uint64) |  |  |
| fail_if_not_exists | [bool](#bool) |  |  |






<a name="discord_api.Message.Sticker"></a>

### Message.Sticker



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| pack_id | [uint64](#uint64) |  |  |
| name | [string](#string) |  |  |
| description | [string](#string) |  |  |
| tags | [string](#string) |  |  |
| asset | [string](#string) |  |  |
| preview_asset | [string](#string) |  |  |
| format_type | [Message.Sticker.Type](#discord_api.Message.Sticker.Type) |  |  |






<a name="discord_api.Role"></a>

### Role
Source: https://discord.com/developers/docs/topics/permissions#role-object


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| name | [string](#string) |  |  |
| color | [int32](#int32) |  |  |
| hoist | [bool](#bool) |  |  |
| position | [int32](#int32) |  |  |
| permissions | [string](#string) |  |  |
| managed | [bool](#bool) |  |  |
| mentionable | [bool](#bool) |  |  |
| tags | [Role.Tag](#discord_api.Role.Tag) | repeated |  |






<a name="discord_api.Role.Tag"></a>

### Role.Tag



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| integration_id | [uint64](#uint64) |  |  |
| premium_subscriber | [bool](#bool) |  |  |






<a name="discord_api.SendChannelMessageRequest"></a>

### SendChannelMessageRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| channel_id | [uint64](#uint64) |  |  |
| content | [string](#string) |  |  |
| embed | [Embed](#discord_api.Embed) |  |  |






<a name="discord_api.SendChannelMessageResponse"></a>

### SendChannelMessageResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| message | [Message](#discord_api.Message) |  |  |






<a name="discord_api.SendDirectMessageRequest"></a>

### SendDirectMessageRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| user_id | [uint64](#uint64) |  |  |
| content | [string](#string) |  |  |
| embed | [Embed](#discord_api.Embed) |  |  |






<a name="discord_api.SendDirectMessageResponse"></a>

### SendDirectMessageResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| message | [Message](#discord_api.Message) |  |  |






<a name="discord_api.User"></a>

### User
Source: https://discord.com/developers/docs/resources/user#user-object


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [uint64](#uint64) |  |  |
| username | [string](#string) |  |  |
| discriminator | [string](#string) |  |  |
| avatar | [string](#string) |  |  |
| bot | [bool](#bool) |  |  |
| system | [bool](#bool) |  |  |
| mfa_enabled | [bool](#bool) |  |  |
| locale | [string](#string) |  |  |
| verified | [bool](#bool) |  |  |
| email | [string](#string) |  |  |
| flags | [int32](#int32) |  |  |
| premium_type | [int32](#int32) |  |  |
| public_flags | [int32](#int32) |  |  |








<a name="discord_api.Channel.Type"></a>

### Channel.Type


| Name | Number | Description |
| ---- | ------ | ----------- |
| GUILD_TEXT | 0 |  |
| GUILD_VOICE | 1 |  |
| GROUP_DM | 2 |  |
| GUILD_CATEGORY | 3 |  |
| GUILD_NEWS | 4 |  |
| PRODUCTS | 5 |  |
| GUILD_STORE | 6 |  |



<a name="discord_api.Message.Activity.Type"></a>

### Message.Activity.Type


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNDEFINED | 0 |  |
| JOIN | 1 |  |
| SPECTATE | 2 |  |
| LISTEN | 3 |  |
| JOIN_REQUESTS | 4 |  |



<a name="discord_api.Message.Sticker.Type"></a>

### Message.Sticker.Type


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNDEFINED | 0 |  |
| PNG | 1 |  |
| APNG | 2 |  |
| LOTTIE | 3 |  |



<a name="discord_api.Message.Type"></a>

### Message.Type


| Name | Number | Description |
| ---- | ------ | ----------- |
| DEFAULT | 0 |  |
| RECIPIENT_ADD | 1 |  |
| RECIPIENT_REMOVE | 2 |  |
| CALL | 3 |  |
| CHANNEL_NAME_CHANGE | 4 |  |
| CHANNEL_ICON_CHANGE | 5 |  |
| CHANNEL_PINNED_MESSAGE | 6 |  |
| GUILD_MEMBER_JOIN | 7 |  |
| USER_PREMIUM_GUILD_SUBSCRIPTION | 8 |  |
| USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 | 9 |  |
| USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 | 10 |  |
| USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 | 11 |  |
| CHANNEL_FOLLOW_ADD | 12 |  |
| GUILD_DISCOVERY_DISQUALIFIED | 14 |  |
| GUILD_DISCOVERY_REQUALIFIED | 15 |  |
| REPLY | 19 |  |
| APPLICATION_COMMAND | 20 |  |







<a name="discord_api.DiscordApi"></a>

### DiscordApi
Provides access to the Discord API

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| SendChannelMessage | [SendChannelMessageRequest](#discord_api.SendChannelMessageRequest) | [SendChannelMessageResponse](#discord_api.SendChannelMessageResponse) | Send a message to a guild channel |
| SendDirectMessage | [SendDirectMessageRequest](#discord_api.SendDirectMessageRequest) | [SendDirectMessageResponse](#discord_api.SendDirectMessageResponse) | Send a direct message to a user |
| GetGuildChannels | [GetGuildChannelsRequest](#discord_api.GetGuildChannelsRequest) | [GetGuildChannelsResponse](#discord_api.GetGuildChannelsResponse) | Get the list of channel for a guild |





## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |
