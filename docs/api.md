# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [discord_api.proto](#discord_api.proto)
    - [Channel](#discord_api.Channel)
    - [Embed](#discord_api.Embed)
    - [GetGuildChannelsRequest](#discord_api.GetGuildChannelsRequest)
    - [GetGuildChannelsResponse](#discord_api.GetGuildChannelsResponse)
    - [SendDirectMessageRequest](#discord_api.SendDirectMessageRequest)
    - [SendDirectMessageResponse](#discord_api.SendDirectMessageResponse)
    - [Thumbnail](#discord_api.Thumbnail)

    - [Channel.Type](#discord_api.Channel.Type)

    - [DiscordApi](#discord_api.DiscordApi)

- [Scalar Value Types](#scalar-value-types)



<a name="discord_api.proto"></a>
<p align="right"><a href="#top">Top</a></p>

## discord_api.proto
Discord API service

This file contains all messages and services currently supported by Discord Proxy


<a name="discord_api.Channel"></a>

### Channel



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



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| title | [string](#string) |  |  |
| description | [string](#string) |  |  |
| thumbnail | [Thumbnail](#discord_api.Thumbnail) |  |  |






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






<a name="discord_api.SendDirectMessageRequest"></a>

### SendDirectMessageRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| user_id | [uint64](#uint64) |  |  |
| content | [string](#string) |  |  |
| embed | [Embed](#discord_api.Embed) |  |  |






<a name="discord_api.SendDirectMessageResponse"></a>

### SendDirectMessageResponse







<a name="discord_api.Thumbnail"></a>

### Thumbnail



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| url | [string](#string) |  |  |
| proxy_url | [string](#string) |  |  |
| height | [int32](#int32) |  |  |
| width | [int32](#int32) |  |  |








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







<a name="discord_api.DiscordApi"></a>

### DiscordApi
Provides access to the Discord API

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
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
