
local start_byte = ARGV[1]
local end_byte = ARGV[2]
local value = ARGV[3]
local total_count = 1
local byte_table = {}

-- local value = redis.call('BITPOS', KEYS[1], 1, start_byte, end_byte)

-- We only inspect bytes
if value ~= -1 then
-- while value ~= -1 do
    local first_one = start_byte * 8 + value
    byte_table[total_count] = first_one
    total_count = total_count + 1
    local other_ones = 0
    -- Inspecting all other bits in byte
    for i=first_one + 1,7 do
        other_ones = redis.call('BITFIELD', KEYS[1], 'GET', 'u1', i)
        if other_ones[1] == 1 then
            byte_table[total_count] = start_byte * 8 + i
            total_count = total_count + 1
        end
    end
    -- start_byte = start_byte + 1
    -- local value = redis.call('BITPOS', KEYS[1], 1, start_byte, end_byte)
-- end
-- if value ~= -1 then
--     return byte_table
-- else
--     return -1
-- end

    return byte_table
else
    return -1
end
