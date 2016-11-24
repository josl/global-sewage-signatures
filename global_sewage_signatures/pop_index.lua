local index = 0

local start_byte = 0
local end_byte = -1
local index_table = {}
local total_count = 1
local value = redis.call('BITPOS', KEYS[1], 1, start_byte, end_byte)

-- We start looping over bytes
while value ~= -1 do
    local first_one = start_byte * 8 + value
    index_table[total_count] = first_one
    total_count = total_count + 1
    local other_ones = 0
    -- Inspecting all other bits in byte
    for i=first_one + 1,7 do
        other_ones = redis.call('BITFIELD', KEYS[1], 'GET', 'u1', i)
        if other_ones[1] == 1 then
            index_table[total_count] = start_byte * 8 + i
            total_count = total_count + 1
        end
        -- index_table[i] = other_ones
    end
    start_byte = start_byte + 1
    value = redis.call('BITPOS', KEYS[1], 1, start_byte, end_byte)
end

return index_table
