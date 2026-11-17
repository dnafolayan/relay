local session_key = KEYS[1]
local used_tokens_key = KEYS[2]

local presented_hash = ARGV[1]
local new_hash = ARGV[2]
local ttl_seconds = tonumber(ARGV[3])

if not presented_hash or #presented_hash == 0 then
    return 'INVALID PRESENTED HASH'
end

if not new_hash or #new_hash == 0 then
    return 'INVALID NEW HASH'
end

if not ttl_seconds or ttl_seconds <= 0 or ttl_seconds % 1 ~= 0 then
    return 'INVALID TTL VAL'
end

if not session_key or #session_key == 0 then
    return 'INVALID_SESSION_KEY'
end

if not used_tokens_key or #used_tokens_key == 0 then
    return 'INVALID_USED_TOKENS_KEY'
end

--

local session_type = redis.call('TYPE', session_key).ok
local used_tokens_type = redis.call('TYPE', used_tokens_key).ok

if session_type ~= 'hash' and session_type ~= 'none' then
    return 'INVALID_SESSION_KEY_TYPE'
end

if used_tokens_type ~= 'set' and used_tokens_type ~= 'none' then
    return 'INVALID_USED_TOKENS_KEY_TYPE'
end

--

local session_exists = redis.call('EXISTS', session_key)

if session_exists == 0 then
    return 'SESSION_NOT_FOUND'
end

local session_status = redis.call('HGET', session_key, 'status')


if session_status == 'revoked' then
    return 'SESSION_REVOKED'
end

if session_status ~= 'active' then
    return 'INVALID SESSION'
end

local current_token_hash = redis.call('HGET', session_key, 'current_token_hash')

if not current_token_hash then
    return 'SESSION_TOKEN_HASH_MISSING'
end

if current_token_hash ~= presented_hash then
    local is_used_token = redis.call('SISMEMBER', used_tokens_key, presented_hash)
    if is_used_token == 0 then
        return 'INVALID TOKEN'
    elseif is_used_token == 1 then
        redis.call('HSET', session_key, 'status', 'revoked')
        return 'TOKEN REUSE'
    end
end

redis.call('SADD', used_tokens_key, presented_hash)
redis.call('HSET', session_key, 'current_token_hash', new_hash)
redis.call('EXPIRE', session_key, ttl_seconds)
redis.call('EXPIRE', used_tokens_key, ttl_seconds)

return 'ROTATION SUCCESS'
