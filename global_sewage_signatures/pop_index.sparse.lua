
function(s, bytes_read, step)

    require "global_sewage_signatures/struct"

    bytes_read = tonumber(bytes_read)
    step = tonumber(step)

    -- local s = redis.call('GET', KEYS[1])
    -- Start reading byte 1
    -- local bytes_read = 1
    local bytes_to_unpack = string.len(s)
    if bytes_to_unpack > 32 then
        bytes_to_unpack = 1
    end
    local max = (bytes_read + step)  / bytes_to_unpack
    -- local max = string.len(s) / bytes_to_unpack
    local tot = string.len(s) * 8
    local ones = 0
    local positions = {}
    local total_bytes = 1
    local negation = 2 ^ (bytes_to_unpack * 8) - 1
    local fmt = 'I'..bytes_to_unpack
    local overflow = 2 ^ 18
    while bytes_read <= max do
        local d = struct.unpack(fmt, s, bytes_read)
        while d ~= 0 do
            ones = ones + 1
            -- Calculate position of 1
            local d_ones = d
            local inner_ones = 0
            while bit.band(d_ones, 1) == 0 do
                inner_ones = inner_ones + 1
                d_ones = bit.rshift(d_ones, 1)
            end
            -- if ones > overflow then break end
            positions[#positions + 1] = ((bytes_read - 1) * 8) - 1 - inner_ones
            d = bit.band(d, d - 1)
            bytes_read = bytes_read + 1
        end
    end

    return positions
end
