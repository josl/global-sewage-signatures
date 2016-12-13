

local function unsign(n)
    if n < 0 then
        n = 4294967296 + n
    end
    return n
end


local value_int = struct.unpack('i32', redis.call('GET', KEYS[1]))

-- Check if there is 1 in least significant byte
local tot = 0
while value_int ~= 0 do
    value_int = bit.band(value_int, bit.arshift(value_int, 1))
    tot = tot + 1
--
--     -- Right-Shift one bit
--     -- local shifted_array = bit.rshift(value_int, 1)
--     -- value_int = bit.rshift(value_int, 1)
--     -- -- Update temp key with shifted array
--     -- redis.call('SET', KEYS[1] .. '_temp', shifted_array)
--     -- return 1
end
return tot


--
-- other_ones = redis.call('BITFIELD', KEYS[1], 'GET', 'u1', i)
-- if other_ones[1] == 1 then
--
--
--
--
-- -- local value = redis.call('BITPOS', KEYS[1], 1, start_byte, end_byte)
--
-- -- We only inspect bytes
-- if value ~= -1 then
-- -- while value ~= -1 do
--     local first_one = start_byte * 8 + value
--     byte_table[total_count] = first_one
--     total_count = total_count + 1
--     local other_ones = 0
--     -- Inspecting all other bits in byte
--     for i=first_one + 1,7 do
--         other_ones = redis.call('BITFIELD', KEYS[1], 'GET', 'u1', i)
--         if other_ones[1] == 1 then
--             byte_table[total_count] = start_byte * 8 + i
--             total_count = total_count + 1
--         end
--     end
--     -- start_byte = start_byte + 1
--     -- local value = redis.call('BITPOS', KEYS[1], 1, start_byte, end_byte)
-- -- end
-- -- if value ~= -1 then
-- --     return byte_table
-- -- else
-- --     return -1
-- -- end
--
--     return byte_table
-- else
--     return -1
-- end
