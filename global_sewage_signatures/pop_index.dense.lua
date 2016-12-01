
function(s, bytes_read, step, population)

    require "struct"
    -- local s = redis.call('GET', KEYS[1])
    -- Start reading byte 1
    bytes_read = tonumber(bytes_read)
    step = tonumber(step)
    -- local bytes_read = tonumber(ARGV[1])
    -- local step = tonumber(ARGV[2])


    local bytes_to_unpack = 1


    -- local bytes_to_unpack = string.len(s)
    -- if bytes_to_unpack > 32 then
    --     bytes_to_unpack = 1
    -- end
    local max = string.len(s) / bytes_to_unpack
    -- local max = (bytes_read + step)  / bytes_to_unpack
    local tot = string.len(s) * 8
    local zeroes = 0
    local positions = {}
    local total_bytes = 1
    local negation = 2 ^ (bytes_to_unpack * 8) - 1
    local fmt = 'I'..bytes_to_unpack
    local overflow = 2 ^ 26
    local out = {}
    local error = 0
    while bytes_read <= max do
        if bytes_read > string.len(s) then break end
        local d
        d, bytes_read = struct.unpack(fmt, s, bytes_read)
        d = negation - d
        local zeroes = {}
        while d ~= 0 do
            -- tot = tot - 1
            -- Calculate position of 1
            local d_ones = d
            local inner_zeroes = 0
            while bit.band(d_ones, 1) == 0 do
                inner_zeroes = inner_zeroes + 1
                d_ones = bit.rshift(d_ones, 1)
            end
            -- if #positions + 1 > overflow then
            --     print('error!')
            --     error = 1
            --     out[1] = 'overflow'
            --     out[2] = bytes_read - 1
            --     -- out[3] = positions
            --     break
            -- end
            zeroes[#zeroes + 1] = ((bytes_read - 1) * 8) - 1 - inner_zeroes
            -- coroutine.yield( ((bytes_read - 1) * 8) - 1 - inner_zeroes )
            -- positions[#positions + 1] = ((bytes_read - 1) * 8) - 1 - inner_zeroes
            d = bit.band(d, d - 1)
        end
        table.sort(zeroes)
        for i,zero in ipairs(zeroes) do coroutine.yield(zero) end
    end

end
